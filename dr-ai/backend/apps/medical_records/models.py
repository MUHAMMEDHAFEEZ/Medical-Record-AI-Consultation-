# apps/medical_records/models.py
from django.db import models
from django.conf import settings
import uuid

class MedicalRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Change to match your actual usage (8-character uppercase IDs)
    nfc_id = models.CharField(
        max_length=8,
        unique=True,
        help_text='Short ID for NFC tag',
        db_index=True
    )
    
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    blood_type = models.CharField(max_length=5, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    chronic_conditions = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)
    
    medical_history = models.JSONField(
        default=list,
        blank=True,
        help_text="List of medical history entries"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'medical_records'
        verbose_name = "Medical Record"
        verbose_name_plural = "Medical Records"

    def __str__(self):
        return f"{self.full_name}'s Medical Record"

class AIConsultation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medical_record = models.ForeignKey(
        MedicalRecord, 
        on_delete=models.CASCADE,
        related_name='consultations'
    )
    question = models.TextField()
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_consultations'
        verbose_name = "AI Consultation"
        verbose_name_plural = "AI Consultations"
        ordering = ['-created_at']

    def __str__(self):
        return f"Consultation for {self.medical_record.full_name} at {self.created_at}"