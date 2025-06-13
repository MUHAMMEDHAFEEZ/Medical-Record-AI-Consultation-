from django.contrib import admin
from .models import MedicalRecord, AIConsultation

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'nfc_id', 'blood_type', 'date_of_birth', 'created_at')
    search_fields = ('full_name', 'nfc_id', 'blood_type')
    readonly_fields = ('nfc_id', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'full_name', 'date_of_birth', 'nfc_id')
        }),
        ('Medical Information', {
            'fields': ('blood_type', 'allergies', 'chronic_conditions', 'medications', 'medical_history')
        }),
        ('Record Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AIConsultation)
class AIConsultationAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('medical_record__full_name', 'question', 'diagnosis')
