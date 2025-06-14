from django.urls import path
from . import views
from django.http import FileResponse
from . import utils

urlpatterns = [
    path('record/', views.medical_record, name='medical_record'),
    path('record/<str:nfc_id>/', views.public_medical_record, name='public_medical_record'),
    path('consultation/<str:nfc_id>/', views.ai_consultation, name='ai_consultation'),
    path('record/<str:nfc_id>/pdf/', lambda request, nfc_id: FileResponse(
        utils.generate_medical_record_pdf(views.get_object_or_404(views.MedicalRecord, nfc_id=nfc_id)),
        filename=f'medical_record_{nfc_id}.pdf'
    ), name='medical_record_pdf'),
    path('consultation/<int:consultation_id>/pdf/', lambda request, consultation_id: FileResponse(
        utils.generate_consultation_pdf(views.get_object_or_404(views.AIConsultation, id=consultation_id)),
        filename=f'consultation_{consultation_id}.pdf'
    ), name='consultation_pdf'),
    # path('record/<str:nfc_id>/generate-pdf/', views.download_medical_record_pdf, name='generate_pdf'),
    path('record/<str:nfc_id>/generate-pdf/', views.download_medical_record_pdf, name='generate_pdf'),
    path('consultation/<uuid:consultation_id>/pdf/', views.download_consultation_pdf, name='consultation_pdf'),


]
