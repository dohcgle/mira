from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoanApplicationAPIView, test_api, MyTokenObtainPairView, GeneratePDFView, LoanStatusUpdateView, LoanDocumentHTMLView, RetrieveLoanAPIView

urlpatterns = [
    # Auth yo'llari
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API yo'llari
    path('loans/', LoanApplicationAPIView.as_view(), name='loan-api'),
    path('loans/<int:loan_id>/', RetrieveLoanAPIView.as_view(), name='loan-detail'),
    path('loans/<int:loan_id>/status/', LoanStatusUpdateView.as_view(), name='loan-status-update'),
    path('loans/<int:loan_id>/doc/<str:template_name>/', LoanDocumentHTMLView.as_view(), name='loan-doc-html'),
    path('loans/<int:loan_id>/pdf/<str:template_name>/', GeneratePDFView.as_view(), name='generate-pdf'),
    path('test/', test_api),

    # Dokumentatsiya (Swagger)
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
