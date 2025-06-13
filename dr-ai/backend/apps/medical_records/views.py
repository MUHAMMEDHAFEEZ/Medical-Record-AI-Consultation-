from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MedicalRecord, AIConsultation
from .serializers import MedicalRecordSerializer, AIConsultationSerializer
from ..ai_service.ollama_client import OllamaClient
from django.shortcuts import get_object_or_404
from uuid import UUID
import json

ollama_client = OllamaClient()

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def medical_record(request):
    if request.method == 'GET':
        try:
            record = MedicalRecord.objects.get(user=request.user)
            serializer = MedicalRecordSerializer(record)
            return Response(serializer.data)
        except MedicalRecord.DoesNotExist:
            return Response({'error': 'Medical record not found'}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'POST':
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def public_medical_record(request, nfc_id):
    """
    Public endpoint for retrieving medical record by NFC ID
    """
    try:
        # Get record using the NFC ID string
        record = get_object_or_404(MedicalRecord, nfc_id=nfc_id)
        data = MedicalRecordSerializer(record).data
        
        # Add NFC URL to response
        data['nfc_url'] = f"http://localhost:5174/record/{record.nfc_id}"
        
        return Response(data)
    except MedicalRecord.DoesNotExist:
        return Response(
            {'error': 'Medical record not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Server error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def ai_consultation(request, nfc_id):
    """
    Public endpoint for AI consultations accessed via NFC
    """
    try:
        # Get medical record
        record = get_object_or_404(MedicalRecord, nfc_id=nfc_id)
        question = request.data.get('question')
        
        if not question:
            return Response(
                {'error': 'Question is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Serialize medical record
        medical_record_data = MedicalRecordSerializer(record).data
        
        try:
            # Get AI response with error catching
            response = ollama_client.generate_medical_response(
                medical_record=medical_record_data,
                question=question
            )
            
            if not isinstance(response, dict) or 'diagnosis' not in response or 'treatment_plan' not in response:
                raise ValueError(f"Invalid AI response format: {response}")
            
            # Create consultation record
            consultation = AIConsultation.objects.create(
                medical_record=record,
                question=question,
                diagnosis=response['diagnosis'],
                treatment_plan=response['treatment_plan']
            )
            
            return Response(AIConsultationSerializer(consultation).data)
            
        except Exception as ai_error:
            print(f"AI Service Error: {str(ai_error)}")
            print(f"Medical Record: {medical_record_data}")
            print(f"Question: {question}")
            return Response(
                {'error': 'AI service error, please try again'}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
            
    except Exception as e:
        print(f"General Error: {str(e)}")
        return Response(
            {'error': 'Internal server error'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_nfc_url(request, patient_id):
    """
    Get NFC URL for a specific patient
    """
    try:
        record = get_object_or_404(MedicalRecord, id=patient_id)
        return Response({
            'nfc_id': str(record.nfc_id),
            'nfc_url': f"http://localhost:5174/record/{record.nfc_id}",
            'patient_name': record.full_name
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )