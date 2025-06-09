from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
from datetime import datetime

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