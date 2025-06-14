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
        data['nfc_url'] = f"http://localhost:5173/record/{record.nfc_id}"
        
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

from django.http import FileResponse, Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MedicalRecord
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
import tempfile
from datetime import datetime
import qrcode
from io import BytesIO

@api_view(['GET'])
def download_medical_record_pdf(request, nfc_id):
    try:
        record = MedicalRecord.objects.get(nfc_id=nfc_id)
        
        # ===== START: MEDICAL HISTORY CONVERSION =====
        # Handle different medical history formats
        if record.medical_history:
            if isinstance(record.medical_history, str):
                # Convert text to list of entries
                history_list = [line.strip() for line in record.medical_history.split('\n') if line.strip()]
            elif isinstance(record.medical_history, list):
                history_list = record.medical_history
            else:
                history_list = ["Invalid medical history format"]
        else:
            history_list = ["No significant medical history recorded."]
        # ===== END: MEDICAL HISTORY CONVERSION =====
        
        # إعداد PDF مؤقت
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        c = canvas.Canvas(temp_file.name, pagesize=A4)
        width, height = A4
        
        # الألوان الرئيسية
        primary_color = colors.HexColor("#1bb76e")  # الأخضر العصري
        secondary_color = colors.HexColor("#2c3e50")  # الأزرق الداكن
        light_gray = colors.HexColor("#f5f7fa")     # الخلفية الرمادية الفاتحة
        
        # إنشاء أنماط النص
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='Header1',
            fontName='Helvetica-Bold',
            fontSize=22,
            textColor=secondary_color,
            spaceAfter=6,
            alignment=TA_CENTER
        ))
        styles.add(ParagraphStyle(
            name='Header2',
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=primary_color,
            spaceAfter=4
        ))
        styles.add(ParagraphStyle(
            name='Body',
            fontName='Helvetica',
            fontSize=11,
            textColor=secondary_color,
            leading=13,
            spaceAfter=4
        ))
        styles.add(ParagraphStyle(
            name='Label',
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=secondary_color,
            leading=11
        ))
        styles.add(ParagraphStyle(
            name='Value',
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.black,
            leading=11
        ))
        styles.add(ParagraphStyle(
            name='History',
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.black,
            leading=12,
            alignment=TA_JUSTIFY
        ))
        # نمط جديد للمعلومات الطبية المدمجة
        styles.add(ParagraphStyle(
            name='MedicalInfo',
            fontName='Helvetica',
            fontSize=11,
            textColor=colors.black,
            leading=14,
            spaceAfter=4,
            leftIndent=10
        ))
        
        # رسم الخلفية التصميمية
        c.setFillColor(light_gray)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        # الرأس - الجزء العلوي
        header_height = 70
        c.setFillColor(primary_color)
        c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
        
        # شعار الرأس
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, height - header_height + 25, "DR.AI Medical Record")
        
        # التاريخ
        c.setFont("Helvetica", 9)
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        c.drawRightString(width - 15, height - 15, f"Generated: {current_date}")
        
        # محتوى الصفحة
        y_position = height - header_height - 25
        content_width = width - 30
        
        # قسم معلومات المريض
        patient_info = [
            ["Full Name:", record.full_name],
            ["Date of Birth:", record.date_of_birth.strftime("%Y-%m-%d")],
            ["NFC ID:", record.nfc_id],
            ["Blood Type:", record.blood_type or "N/A"]
        ]
        
        # رسم بطاقة معلومات المريض
        card_height = len(patient_info) * 18 + 30
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.lightgrey)
        c.setLineWidth(0.3)
        c.roundRect(15, y_position - card_height, content_width, card_height, 8, fill=1, stroke=1)
        
        # عنوان البطاقة
        p = Paragraph("<b>Patient Information</b>", styles["Header2"])
        p.wrapOn(c, content_width, 25)
        p.drawOn(c, 25, y_position - 25)
        
        # محتوى البطاقة
        current_y = y_position - 45
        for label, value in patient_info:
            p_label = Paragraph(label, styles["Label"])
            p_label.wrapOn(c, 100, 15)
            p_label.drawOn(c, 30, current_y)
            
            p_value = Paragraph(value, styles["Value"])
            p_value.wrapOn(c, content_width - 130, 15)
            p_value.drawOn(c, 130, current_y)
            
            current_y -= 18
        
        # تحديث موضع المؤشر بعد البطاقة
        y_position = current_y - 10
        
        # ===== UPDATED MEDICAL SECTIONS =====
        medical_sections = [
            {
                "title": "Medical Info",
                "icon": "",
                "content": [
                    ["", f"Allergies: {record.allergies or 'None'}"],
                    ["", f"Chronic Conditions: {record.chronic_conditions or 'None'}"]
                ]
            },
            {
                "title": "Current Medications",
                "icon": "",
                "content": [
                    ["", record.medications or "No current medications"]
                ]
            },
            # Dynamic Medical History Section
            {
                "title": "Medical History",
                "icon": "",
                "content": [
                    ["", entry] for entry in history_list
                ]
            }
        ]
        # ===== END UPDATED SECTION =====
        
        # رسم الأقسام الطبية
        for section in medical_sections:
            # حساب ارتفاع القسم
            section_height = len(section["content"]) * 20 + 30
            
            # التحقق من المساحة المتبقية في الصفحة
            if y_position - section_height < 120:
                c.showPage()
                y_position = height - 30
                c.setFillColor(light_gray)
                c.rect(0, 0, width, height, fill=1, stroke=0)
            
            # رسم البطاقة
            c.setFillColor(colors.white)
            c.setStrokeColor(colors.lightgrey)
            c.setLineWidth(0.3)
            c.roundRect(15, y_position - section_height, content_width, section_height, 8, fill=1, stroke=1)
            
            # عنوان القسم
            p = Paragraph(f"<b>{section['icon']} {section['title']}</b>", styles["Header2"])
            p.wrapOn(c, content_width, 25)
            p.drawOn(c, 25, y_position - 25)
            
            # محتوى القسم
            current_y = y_position - 45
            for item in section["content"]:
                if item[0]:  # إذا كان هناك تسمية
                    p_label = Paragraph(item[0], styles["Label"])
                    p_label.wrapOn(c, 100, 15)
                    p_label.drawOn(c, 30, current_y)
                    
                    p_value = Paragraph(item[1], styles["Value"])
                    p_value.wrapOn(c, content_width - 130, 15)
                    p_value.drawOn(c, 130, current_y)
                else:
                    # استخدام نمط خاص للمعلومات الطبية
                    style = styles["MedicalInfo"] if section["title"] == "Medical Info" else styles["Body"]
                    p_value = Paragraph(item[1], style)
                    p_value.wrapOn(c, content_width - 50, 20)
                    p_value.drawOn(c, 30, current_y)
                
                current_y -= 20
            
            # تحديث موضع المؤشر بعد البطاقة
            y_position = current_y - 10
        
        # إنشاء رمز الاستجابة السريعة (QR Code) مع رابط URL
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=4,
        )
        
        # إنشاء رابط URL مع nfc_id
        frontend_url = f"https://rj8vq174-5173.uks1.devtunnels.ms/record/{record.nfc_id}"
        qr.add_data(frontend_url)
        qr.make(fit=True)
        
        # إنشاء صورة QR Code في الذاكرة
        # تحويل كائن اللون إلى تنسيق HEX
        secondary_hex = f"#{int(secondary_color.red * 255):02x}{int(secondary_color.green * 255):02x}{int(secondary_color.blue * 255):02x}"
        qr_img = qr.make_image(fill_color=secondary_hex, back_color="white")
        qr_img_bytes = BytesIO()
        qr_img.save(qr_img_bytes, format='PNG')
        qr_img_bytes.seek(0)  # العودة إلى بداية الـ stream
        
        # إضافة QR Code إلى PDF باستخدام ImageReader
        qr_size = 50  # حجم الصورة
        qr_x = 30
        qr_y = 50
        
        # استخدام ImageReader لتحويل BytesIO إلى كائن صورة مناسب
        img_reader = ImageReader(qr_img_bytes)
        c.drawImage(img_reader, qr_x, qr_y, width=qr_size, height=qr_size)
        
        # إضافة نص تحت QR Code
        c.setFillColor(primary_color)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(qr_x, qr_y - 15, "Scan to view digital record")
        
        # التذييل
        footer_height = 25
        c.setFillColor(secondary_color)
        c.rect(0, 0, width, footer_height, fill=1, stroke=0)
        c.setFillColor(colors.whitesmoke)
        c.setFont("Helvetica", 8)
        c.drawCentredString(width/2, 8, "Confidential Medical Record • Generated by DR.AI System • © 2025 DR.AI")
        
        c.save()
        return FileResponse(
            open(temp_file.name, 'rb'), 
            as_attachment=True, 
            filename=f"medical_record_{nfc_id}.pdf"
        )

    except MedicalRecord.DoesNotExist:
        raise Http404("Medical record not found")
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def download_consultation_pdf(request, consultation_id):
    try:
        consultation = get_object_or_404(AIConsultation, id=consultation_id)
        record = consultation.medical_record
        
        # إعداد PDF مؤقت
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        c = canvas.Canvas(temp_file.name, pagesize=A4)
        width, height = A4
        
        # الألوان الرئيسية (نفس ألوان السجل الطبي)
        primary_color = colors.HexColor("#1bb76e")  # الأخضر العصري
        secondary_color = colors.HexColor("#2c3e50")  # الأزرق الداكن
        light_gray = colors.HexColor("#f5f7fa")     # الخلفية الرمادية الفاتحة
        
        # إنشاء أنماط النص (نفس أنماط السجل الطبي)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='Header1',
            fontName='Helvetica-Bold',
            fontSize=22,
            textColor=secondary_color,
            spaceAfter=6,
            alignment=TA_CENTER
        ))
        styles.add(ParagraphStyle(
            name='Header2',
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=primary_color,
            spaceAfter=4
        ))
        styles.add(ParagraphStyle(
            name='Body',
            fontName='Helvetica',
            fontSize=11,
            textColor=secondary_color,
            leading=13,
            spaceAfter=4
        ))
        styles.add(ParagraphStyle(
            name='Label',
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=secondary_color,
            leading=11
        ))
        styles.add(ParagraphStyle(
            name='Value',
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.black,
            leading=11
        ))
        styles.add(ParagraphStyle(
            name='Content',
            fontName='Helvetica',
            fontSize=11,
            textColor=colors.black,
            leading=14,
            spaceAfter=4,
            leftIndent=10
        ))
        
        # رسم الخلفية التصميمية (نفس السجل الطبي)
        c.setFillColor(light_gray)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        # الرأس - الجزء العلوي (نفس التصميم)
        header_height = 70
        c.setFillColor(primary_color)
        c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
        
        # شعار الرأس (معدل ليتناسب مع الاستشارة)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, height - header_height + 25, "DR.AI Consultation Report")
        
        # التاريخ (نفس التصميم)
        c.setFont("Helvetica", 9)
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        c.drawRightString(width - 15, height - 15, f"Generated: {current_date}")
        
        # محتوى الصفحة
        y_position = height - header_height - 25
        content_width = width - 30
        
        # قسم معلومات المريض (بطاقة مماثلة للسجل الطبي)
        patient_info = [
            ["Full Name:", record.full_name],
            ["Date of Birth:", record.date_of_birth.strftime("%Y-%m-%d")],
            ["NFC ID:", record.nfc_id],
            ["Consultation ID:", str(consultation.id)],
            ["Consultation Date:", consultation.created_at.strftime("%Y-%m-%d %H:%M")]
        ]
        
        # رسم بطاقة معلومات المريض
        card_height = len(patient_info) * 18 + 30
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.lightgrey)
        c.setLineWidth(0.3)
        c.roundRect(15, y_position - card_height, content_width, card_height, 8, fill=1, stroke=1)
        
        # عنوان البطاقة
        p = Paragraph("<b>Patient & Consultation Information</b>", styles["Header2"])
        p.wrapOn(c, content_width, 25)
        p.drawOn(c, 25, y_position - 25)
        
        # محتوى البطاقة
        current_y = y_position - 45
        for label, value in patient_info:
            p_label = Paragraph(label, styles["Label"])
            p_label.wrapOn(c, 100, 15)
            p_label.drawOn(c, 30, current_y)
            
            p_value = Paragraph(value, styles["Value"])
            p_value.wrapOn(c, content_width - 130, 15)
            p_value.drawOn(c, 130, current_y)
            
            current_y -= 18
        
        # تحديث موضع المؤشر بعد البطاقة
        y_position = current_y - 10
        
        # ===== SECTIONS USING SAME STYLE AS MEDICAL RECORD =====
        consultation_sections = [
            {
                "title": "Question",
                "content": consultation.question
            },
            {
                "title": "Diagnosis",
                "content": consultation.diagnosis
            },
            {
                "title": "Treatment Plan",
                "content": consultation.treatment_plan
            }
        ]
        
        # دالة مساعدة لرسم المحتوى مع التفاف النص
        def draw_content_section(title, content):
            nonlocal y_position
            
            # حساب ارتفاع العنوان
            title_height = 30
            
            # إنشاء فقرة للمحتوى
            p_content = Paragraph(content, styles["Content"])
            content_width_available = content_width - 40  # هامش 20 لكل جانب
            w, h = p_content.wrap(content_width_available, 1000)  # ارتفاع كبير للسماح بالتفاف
            
            # ارتفاع القسم الكلي
            section_height = title_height + h + 20  # هامش إضافي
            
            # التحقق من المساحة المتبقية في الصفحة
            if y_position - section_height < 100:
                c.showPage()
                y_position = height - 30
                c.setFillColor(light_gray)
                c.rect(0, 0, width, height, fill=1, stroke=0)
            
            # رسم البطاقة
            c.setFillColor(colors.white)
            c.setStrokeColor(colors.lightgrey)
            c.setLineWidth(0.3)
            c.roundRect(15, y_position - section_height, content_width, section_height, 8, fill=1, stroke=1)
            
            # عنوان القسم
            p_title = Paragraph(f"<b>{title}</b>", styles["Header2"])
            p_title.wrapOn(c, content_width, 25)
            p_title.drawOn(c, 25, y_position - 25)
            
            # محتوى القسم
            p_content.drawOn(c, 30, y_position - section_height + 10)
            
            # تحديث موضع المؤشر بعد البطاقة
            return section_height + 15
        
        # رسم أقسام الاستشارة
        for section in consultation_sections:
            section_height = draw_content_section(section["title"], section["content"])
            y_position -= section_height
        
        # إنشاء رمز الاستجابة السريعة (QR Code) بنفس أسلوب السجل الطبي
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=4,
        )
        
        # إنشاء رابط URL مع nfc_id
        frontend_url = f"https://rj8vq174-5173.uks1.devtunnels.ms/record/{record.nfc_id}"
        qr.add_data(frontend_url)
        qr.make(fit=True)
        
        # إنشاء صورة QR Code في الذاكرة
        secondary_hex = f"#{int(secondary_color.red * 255):02x}{int(secondary_color.green * 255):02x}{int(secondary_color.blue * 255):02x}"
        qr_img = qr.make_image(fill_color=secondary_hex, back_color="white")
        qr_img_bytes = BytesIO()
        qr_img.save(qr_img_bytes, format='PNG')
        qr_img_bytes.seek(0)
        
        # إضافة QR Code إلى PDF
        qr_size = 50
        qr_x = 30
        qr_y = 50
        
        # التحقق من المساحة قبل إضافة QR
        if y_position - qr_size < 100:
            c.showPage()
            y_position = height - 30
            c.setFillColor(light_gray)
            c.rect(0, 0, width, height, fill=1, stroke=0)
            qr_y = height - 100
        
        img_reader = ImageReader(qr_img_bytes)
        c.drawImage(img_reader, qr_x, qr_y, width=qr_size, height=qr_size)
        
        # إضافة نص تحت QR Code
        c.setFillColor(primary_color)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(qr_x, qr_y - 15, "Scan to view digital record")
        
        # التذييل (نفس تذييل السجل الطبي)
        footer_height = 25
        c.setFillColor(secondary_color)
        c.rect(0, 0, width, footer_height, fill=1, stroke=0)
        c.setFillColor(colors.whitesmoke)
        c.setFont("Helvetica", 8)
        c.drawCentredString(width/2, 8, "Confidential Medical Consultation • Generated by DR.AI System • © 2025 DR.AI")
        
        c.save()
        return FileResponse(
            open(temp_file.name, 'rb'), 
            as_attachment=True, 
            filename=f"consultation_{consultation.id}.pdf"
        )

    except AIConsultation.DoesNotExist:
        raise Http404("Consultation not found")
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

