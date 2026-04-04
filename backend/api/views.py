from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import LoanApplication
from .serializers import LoanApplicationSerializer, MyTokenObtainPairSerializer

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
            operator_name = profile.fish if profile else request.user.username
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


def build_loan_context(data):
    """LoanWizard JSON → Shablon context (umumiy funksiya)"""
    collateral = data.get('collateral') or {}
    # 'types' ni list yoki dict shaklida qabul qilamiz
    col_types = collateral.get('types', {}) if isinstance(collateral, dict) else {}

    if isinstance(col_types, list):
        is_avto        = 'avto' in col_types
        is_kochmas     = 'mulk' in col_types
        is_sugurta     = 'sugurta' in col_types
    elif isinstance(col_types, dict):
        is_avto        = bool(col_types.get('avto', False))
        is_kochmas     = bool(col_types.get('mulk', False))
        is_sugurta     = bool(col_types.get('sugurta', False))
    else:
        is_avto = is_kochmas = is_sugurta = False

    avto    = collateral.get('avto', {})    if isinstance(collateral, dict) else {}
    mulk    = collateral.get('mulk', {})    if isinstance(collateral, dict) else {}
    sugurta = collateral.get('sugurta', {}) if isinstance(collateral, dict) else {}

    return {
        'loan': {
            'client': data.get('client_info', {}),
            'details': {
                'shartnoma_raqami': data.get('loan_details', {}).get('shartnoma_raqami'),
                'shartnoma_sanasi': data.get('loan_details', {}).get('shartnoma_sana'),
                'miqdori':     data.get('loan_details', {}).get('kredit_summasi'),
                'miqdori_soz': data.get('loan_details', {}).get('kredit_summasi_soz'),
                'muddat_oy':   data.get('loan_details', {}).get('kredit_muddati'),
                'foiz':        data.get('loan_details', {}).get('foiz_stavkasi'),
                'foiz_soz':    data.get('loan_details', {}).get('foiz_stavkasi_soz'),
            },
            'financial_info': data.get('financial', {})
        },
        'avto':              avto,
        'mulk':              mulk,
        'sugurta':           sugurta,
        'is_avto':           is_avto,
        'is_kochmas':        is_kochmas,
        'is_sugurta_mavjud': is_sugurta,
        # collateral egasi uchun (shablon {{ collateral.owner_client.fish }} ishlatadi)
        'collateral': {
            'owner_client': data.get('client_info', {}),
        }
    }


class LoanDocumentHTMLView(View):
    """Hujjat sahifasi - hamma uchun ochiq (QR kod orqali kirish uchun), PDF formatida"""
    def get(self, request, loan_id, template_name):
        try:
            loan_obj = LoanApplication.objects.get(id=loan_id)
        except LoanApplication.DoesNotExist:
            return HttpResponse('<h2 style="font-family:sans-serif;color:red">Ariza topilmadi</h2>', status=404)

        context = build_loan_context(loan_obj.data)

        # QR kod: aynan shu sahifaning URL'iga
        doc_url = request.build_absolute_uri()
        context['qr_manager'] = generate_qr_base64(doc_url)

        try:
            html_string = render_to_string(f"{template_name}.html", context)

            # PDF generatsiyasi (to'g'ridan-to'g'ri baytlarni qaytarish)
            html = HTML(string=html_string, base_url=request.build_absolute_uri())
            doc = html.render()  # render() alohida qilgan ma'qul
            pdf_bytes = doc.write_pdf()

            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{template_name}_{loan_id}.pdf"'
            return response
        except Exception as e:
            return HttpResponse(f'<h2 style="font-family:sans-serif;color:red">Xatolik: {e}</h2>', status=500)

class GeneratePDFView(APIView):
    def get(self, request, loan_id, template_name):
        try:
            loan_obj = LoanApplication.objects.get(id=loan_id)
            data = loan_obj.data
            
            # 1. Shablon kutayotgan formatga ma'lumotlarni o'tkazamiz (Mapping)
            # LoanWizard JSON strukturasi -> Shablon strukturasi
            context = {
                'loan': {
                    'client': data.get('client_info', {}),
                    'details': {
                        'shartnoma_raqami': data.get('loan_details', {}).get('shartnoma_raqami'),
                        'shartnoma_sanasi': data.get('loan_details', {}).get('shartnoma_sana'),
                        'miqdori': data.get('loan_details', {}).get('kredit_summasi'),
                        'miqdori_soz': data.get('loan_details', {}).get('kredit_summasi_soz'),
                        'muddat_oy': data.get('loan_details', {}).get('kredit_muddati'),
                        'foiz': data.get('loan_details', {}).get('foiz_stavkasi'),
                        'foiz_soz': data.get('loan_details', {}).get('foiz_stavkasi_soz'),
                    },
                    'financial_info': data.get('financial', {})
                },
                'avto': data.get('collateral', {}).get('avto', {}),
                'mulk': data.get('collateral', {}).get('mulk', {}),
                'sugurta': data.get('collateral', {}).get('sugurta', {}),
                'is_avto': data.get('collateral', {}).get('types', {}).get('avto', False),
                'is_kochmas': data.get('collateral', {}).get('types', {}).get('mulk', False),
                'is_sugurta_mavjud': data.get('collateral', {}).get('types', {}).get('sugurta', False),
            }

            # 2. HTML renders
            html_string = render_to_string(f"{template_name}.html", context)
            
            # 3. PDF generation
            html = HTML(string=html_string, base_url=request.build_absolute_uri())
            result = html.write_pdf()

            # 4. Response qaytarish
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{template_name}_{loan_id}.pdf"'
            response.write(result)
            return response

        except LoanApplication.DoesNotExist:
            return Response({"error": "Ariza topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def test_api(request):
    return Response({"message": "Mira API is working!"})
