from rest_framework import serializers
from .models import MedicalRecord, AIConsultation

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

class AIConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIConsultation
        fields = '__all__'
        read_only_fields = ('id', 'created_at')