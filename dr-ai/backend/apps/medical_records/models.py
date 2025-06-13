from django.db import models
from django.conf import settings
import uuid
import random
import string

class MedicalRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def generate_short_id():
        # Generate 6-character alphanumeric ID
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=6))
      # Short ID for NFC tag
    nfc_id = models.CharField(
        max_length=6,
        default=generate_short_id,
        unique=True,
        help_text='Short ID for NFC tag',
        db_index=True
    )
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    blood_type = models.CharField(max_length=5)
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'medical_records'

    def __str__(self):
        return f"{self.full_name}'s Medical Record"

class AIConsultation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    question = models.TextField()
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_consultations'

    def __str__(self):
        return f"Consultation for {self.medical_record.full_name} at {self.created_at}"