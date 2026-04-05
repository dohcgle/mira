from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse # MUHIM: PDF response qaytarish uchun
from django.template.loader import render_to_string # MUHIM: HTML shablon o'qish uchun
from weasyprint import HTML # MUHIM: PDF generatsiya uchun
from django.contrib.auth.models import User
from .models import LoanApplication, UserProfile
from .serializers import LoanApplicationSerializer, MyTokenObtainPairSerializer, UserProfileSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            # Response bodyga birinchi guruh nomini role sifatida qo'shish
            group = user.groups.first()
            response.data['role'] = group.name if group else 'unknown'
            response.data['username'] = user.username
        return response

class UserProfileView(APIView):
    def get(self, request):
        profile = getattr(request.user, 'profile', None)
        if not profile:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

class LoanApplicationAPIView(APIView):
    # Barcha guruhlar barcha arizalarni ko'radi
    def get(self, request):
        loans = LoanApplication.objects.all().order_by('-created_at')
        serializer = LoanApplicationSerializer(loans, many=True)
        return Response(serializer.data)

    # Yangi ariza saqlash (POST)
    def post(self, request):
        serializer = LoanApplicationSerializer(data={'data': request.data})
        if serializer.is_valid():
            profile = getattr(request.user, 'profile', None)
            branch = profile.filial if profile else "No Branch"
            operator_name = profile.filial_fish if profile else request.user.username
            serializer.save(
                created_by=request.user,
                updated_by=request.user,
                branch=branch,
                operator_fish=operator_name
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveLoanAPIView(APIView):
    # Alohida ariza ma'lumotlarini olish
    def get(self, request, loan_id):
        try:
            loan = LoanApplication.objects.get(id=loan_id)
            serializer = LoanApplicationSerializer(loan)
            return Response(serializer.data)
        except LoanApplication.DoesNotExist:
            return Response({"error": "Ariza topilmadi"}, status=status.HTTP_404_NOT_FOUND)

class LoanStatusUpdateView(APIView):
    """Moderator va Direktor tomonidan status o'zgartirish"""
    def patch(self, request, loan_id):
        try:
            loan = LoanApplication.objects.get(id=loan_id)
        except LoanApplication.DoesNotExist:
            return Response({"error": "Ariza topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        user_group = request.user.groups.first()
        group_name = user_group.name if user_group else None
        action = request.data.get('action')  # 'approve' yoki 'reject'

        # Moderator: new → moderation
        if group_name == 'moderator':
            if loan.status != 'new':
                return Response({"error": "Bu ariza allaqachon moderatsiya qilingan"}, status=status.HTTP_400_BAD_REQUEST)
            if action == 'approve':
                loan.status = 'moderation'
            elif action == 'reject':
                loan.status = 'rejected'

        # Direktor: moderation → approved
        elif group_name == 'direktor':
            if loan.status != 'moderation':
                return Response({"error": "Bu ariza direktor tasdiqlashiga tayyor emas"}, status=status.HTTP_400_BAD_REQUEST)
            if action == 'approve':
                loan.status = 'approved'
            elif action == 'reject':
                loan.status = 'rejected'
        else:
            return Response({"error": "Sizda bu amalni bajarish huquqi yo'q"}, status=status.HTTP_403_FORBIDDEN)

        loan.updated_by = request.user
        loan.save()
        serializer = LoanApplicationSerializer(loan)
        return Response(serializer.data)

from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views import View
from rest_framework_simplejwt.tokens import AccessToken
from weasyprint import HTML
import io, base64, qrcode, tempfile


def generate_qr_base64(url: str) -> str:
    """URL dan QR kod yaratib, base64 data URI qaytaradi"""
    qr_img = qrcode.make(url)
    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"


def build_loan_context(data, loan_obj=None):
    """LoanWizard JSON ma'lumotlarini RAW holatda contextga yuklash va grafikni tahlil qilish"""
    context = data.copy()
    
    # created_at ni alohida qo'shib qo'yamiz
    if loan_obj:
        context['created_at'] = loan_obj.created_at

    # Grafik matnini (textarea'dan kelgan) tahlil qilish (Parser)
    loan_details = context.get('loan_details', {})
    grafik_matni = loan_details.get('grafik_matni', '')
    schedule_data = []

    if grafik_matni:
        import re
        lines = grafik_matni.strip().split('\n')
        for line in lines:
            if not line.strip(): continue
            # Tablar yoki 2+ bo'shliqlar bo'yicha bo'lish (Excel dan nusxalanganda tab bo'ladi)
            parts = re.split(r'\t+|\s{2,}', line.strip())
            # Kamida 5-6 ustun bo'lsa (№, Sana, Qoldiq, Asosiy, Foiz, Jami)
            if len(parts) >= 6:
                # Agar barcha asosiy qiymatlar bo'sh, 0 yoki '-' bo'lsa, qatorni chetlab o'tamiz
                vals = [p.strip().replace(' ', '').replace(',', '.') for p in parts[2:6]]
                
                def is_val_empty(v):
                    # Tozalangan qiymatni tekshirish
                    v_clean = v.replace('-', '').replace('0.00', '').replace('0', '').strip()
                    return not v_clean or v == '-' or v == '-0.00'

                is_all_zero = all(is_val_empty(v) for v in vals)
                
                if not is_all_zero:
                    schedule_data.append({
                        'num': parts[0],
                        'date': parts[1],
                        'balance': parts[2],
                        'principal': parts[3],
                        'interest': parts[4],
                        'total': parts[5]
                    })
    
    context['schedule_list'] = schedule_data
    return context


class LoanDocumentHTMLView(View):
    """Hujjat sahifasi - hamma uchun ochiq (QR kod orqali kirish uchun), PDF formatida"""
    def get(self, request, loan_id, template_name):
        try:
            loan_obj = LoanApplication.objects.get(id=loan_id)
        except LoanApplication.DoesNotExist:
            return HttpResponse('<h2 style="font-family:sans-serif;color:red">Ariza topilmadi</h2>', status=404)

        context = build_loan_context(loan_obj.data, loan_obj)

        # QR kod: aynan shu sahifaning URL'iga, lekin domenini https://epl.pullol.uz/ ga almashtiramiz
        doc_url = request.build_absolute_uri()
        if 'localhost' in doc_url or '127.0.0.1' in doc_url:
            doc_url = doc_url.replace(request.get_host(), 'epl.pullol.uz').replace('http://', 'https://')
        else:
            # Agar boshqa domen bo'lsa ham https ekanligiga ishonch hosil qilamiz
            doc_url = doc_url.replace('http://', 'https://')
            
        context['qr_manager'] = generate_qr_base64(doc_url)

        try:
            html_string = render_to_string(f"{template_name}.html", context)

            # PDF generatsiyasi (to'g'ridan-to'g'ri baytlarni qaytarish)
            html = HTML(string=html_string, base_url="http://localhost:8000/")
            doc = html.render()  # render() alohida qilgan ma'qul
            pdf_bytes = doc.write_pdf()

            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{template_name}_{loan_id}.pdf"'
            return response
        except Exception as e:
            return HttpResponse(f'<h2 style="font-family:sans-serif;color:red">Xatolik: {e}</h2>', status=500)

class GeneratePDFView(APIView):
    def get(self, request, loan_id, template_name):
        import traceback
        try:
            loan_obj = LoanApplication.objects.get(id=loan_id)
            context = build_loan_context(loan_obj.data, loan_obj)
            
            # QR kod: aynan shu sahifaning URL'iga, lekin domenini https://epl.pullol.uz/ ga almashtiramiz
            doc_url = request.build_absolute_uri()
            if 'localhost' in doc_url or '127.0.0.1' in doc_url:
                doc_url = doc_url.replace(request.get_host(), 'epl.pullol.uz').replace('http://', 'https://')
            else:
                doc_url = doc_url.replace('http://', 'https://')
            
            context['qr_manager'] = generate_qr_base64(doc_url)
            
            # 2. HTML renders
            html_string = render_to_string(f"{template_name}.html", context)
            
            # 3. PDF generation
            html = HTML(string=html_string, base_url="http://localhost:8000/")
            result = html.write_pdf()

            # 4. Response qaytarish
            response = HttpResponse(result, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{template_name}_{loan_id}.pdf"'
            return response
        except Exception:
            traceback.print_exc()
            raise

@api_view(['GET'])
def test_api(request):
    return Response({"message": "Mira API is working!"})
