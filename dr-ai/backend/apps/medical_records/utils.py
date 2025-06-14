from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
from datetime import datetime

from fpdf import FPDF
import os
from django.conf import settings

def generate_medical_record_pdf(medical_record):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Add title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    story.append(Paragraph("Medical Record", title_style))
    
    # Patient information
    story.append(Paragraph(f"Patient: {medical_record.full_name}", styles["Heading2"]))
    story.append(Paragraph(f"Date of Birth: {medical_record.date_of_birth}", styles["Normal"]))
    story.append(Paragraph(f"Blood Type: {medical_record.blood_type}", styles["Normal"]))
    story.append(Spacer(1, 12))
    
    # Medical details
    sections = [
        ("Allergies", medical_record.allergies),
        ("Chronic Conditions", medical_record.chronic_conditions),
        ("Current Medications", medical_record.medications),
        ("Medical History", medical_record.medical_history)
    ]
    
    for title, content in sections:
        story.append(Paragraph(title, styles["Heading3"]))
        story.append(Paragraph(content or "None", styles["Normal"]))
        story.append(Spacer(1, 12))
    
    # Metadata
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Italic"]))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_consultation_pdf(consultation):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Add title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    story.append(Paragraph("AI Medical Consultation", title_style))
    
    # Patient information
    story.append(Paragraph(f"Patient: {consultation.medical_record.full_name}", styles["Heading2"]))
    story.append(Paragraph(f"Date: {consultation.created_at.strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1, 12))
    
    # Question
    story.append(Paragraph("Question", styles["Heading3"]))
    story.append(Paragraph(consultation.question, styles["Normal"]))
    story.append(Spacer(1, 12))
    
    # Diagnosis
    story.append(Paragraph("Diagnosis", styles["Heading3"]))
    story.append(Paragraph(consultation.diagnosis, styles["Normal"]))
    story.append(Spacer(1, 12))
    
    # Treatment Plan
    story.append(Paragraph("Treatment Plan", styles["Heading3"]))
    story.append(Paragraph(consultation.treatment_plan, styles["Normal"]))
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_medical_record_pdf(record):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Medical Record", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Name: {record.full_name}", ln=True)
    pdf.cell(200, 10, txt=f"Blood Type: {record.blood_type}", ln=True)
    pdf.cell(200, 10, txt=f"Allergies: {record.allergies}", ln=True)
    pdf.cell(200, 10, txt=f"Chronic Conditions: {record.chronic_conditions}", ln=True)
    pdf.cell(200, 10, txt=f"Medications: {record.medications}", ln=True)

    folder = os.path.join(settings.MEDIA_ROOT, "pdfs")
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, f"medical_record_{record.nfc_id}.pdf")
    pdf.output(file_path)
    return file_path
