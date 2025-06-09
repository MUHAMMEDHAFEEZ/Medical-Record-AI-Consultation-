import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';

// Existing MedicalPDFData interface
interface MedicalPDFData {
  patientName: string;
  dateOfBirth: string;
  bloodType: string;
  allergies: string;
  chronicConditions: string;
  medications: string;
  medicalHistory: string;
  consultation?: {
    question: string;
    diagnosis: string;
    treatment_plan: string;
    timestamp?: string;
  };
}

// New ConsultationPDFData interface
interface ConsultationPDFData {
  patientName: string;
  dateOfBirth: string;
  question: string;
  diagnosis: string;
  treatment_plan: string;
  timestamp?: string;
}

// Existing generateMedicalPDF function
export const generateMedicalPDF = (data: MedicalPDFData): boolean => {
  try {
    // Create new document
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const margin = 20;

    // Add title
    doc.setFontSize(24);
    doc.setTextColor(0, 82, 164); // Professional blue color
    doc.text('Medical Record', pageWidth / 2, margin, { align: 'center' });

    // Patient Information Table
    autoTable(doc, {
      startY: margin + 15,
      theme: 'grid',
      headStyles: { 
        fillColor: [0, 82, 164],
        textColor: 255,
        fontSize: 12,
        fontStyle: 'bold'
      },
      head: [['Patient Information', '']],
      body: [
        ['Patient Name', data.patientName || 'N/A'],
        ['Date of Birth', data.dateOfBirth ? new Date(data.dateOfBirth).toLocaleDateString() : 'N/A'],
        ['Blood Type', data.bloodType || 'N/A']
      ],
      columnStyles: {
        0: { 
          cellWidth: 80,
          fontStyle: 'bold'
        },
        1: { 
          cellWidth: 100
        }
      },
      margin: { left: margin }
    });

    // Medical Details Table
    autoTable(doc, {
      startY: (doc as any).lastAutoTable.finalY + 10,
      theme: 'grid',
      headStyles: { 
        fillColor: [0, 82, 164],
        textColor: 255
      },
      head: [['Medical Information', '']],
      body: [
        ['Allergies', data.allergies || 'None'],
        ['Chronic Conditions', data.chronicConditions || 'None'],
        ['Current Medications', data.medications || 'None']
      ],
      columnStyles: {
        0: { 
          cellWidth: 80,
          fontStyle: 'bold'
        },
        1: { 
          cellWidth: 100
        }
      },
      margin: { left: margin }
    });

    // Medical History
    autoTable(doc, {
      startY: (doc as any).lastAutoTable.finalY + 10,
      theme: 'grid',
      headStyles: { 
        fillColor: [0, 82, 164],
        textColor: 255
      },
      head: [['Medical History']],
      body: [[data.medicalHistory || 'No medical history available']],
      margin: { left: margin }
    });

    // Add AI Consultation section if available
    if (data.consultation) {
      doc.addPage();
      
      // AI Consultation Header
      doc.setFontSize(24);
      doc.setTextColor(0, 82, 164);
      doc.text('AI Consultation Report', pageWidth / 2, margin, { align: 'center' });

      // AI Consultation Table
      autoTable(doc, {
        startY: margin + 15,
        theme: 'grid',
        headStyles: { 
          fillColor: [0, 82, 164],
          textColor: 255,
          fontSize: 12,
          fontStyle: 'bold'
        },
        head: [['AI Consultation Details', '']],
        body: [
          ['Question', data.consultation.question],
          ['Diagnosis', data.consultation.diagnosis],
          ['Treatment Plan', data.consultation.treatment_plan],
          ['Consultation Time', data.consultation.timestamp || new Date().toLocaleString()]
        ],
        columnStyles: {
          0: { cellWidth: 80, fontStyle: 'bold' },
          1: { cellWidth: 100 }
        },
        margin: { left: margin }
      });
    }

    // Add footer
    doc.setFontSize(10);
    doc.setTextColor(128);
    doc.text(
      `Generated on ${new Date().toLocaleString()}`,
      pageWidth / 2,
      doc.internal.pageSize.getHeight() - 10,
      { align: 'center' }
    );

    // Save PDF
    const filename = `medical_record_${data.patientName?.replace(/\s+/g, '_') || 'unnamed'}_${new Date().toISOString().split('T')[0]}.pdf`;
    doc.save(filename);
    console.log('PDF generated successfully:', filename);
    return true;

  } catch (error) {
    console.error('PDF Generation Error:', error);
    return false;
  }
};

// New generateConsultationPDF function
export const generateConsultationPDF = (data: ConsultationPDFData): boolean => {
  try {
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const margin = 20;

    // Header
    doc.setFontSize(24);
    doc.setTextColor(0, 82, 164);
    doc.text('AI Consultation Report', pageWidth / 2, margin, { align: 'center' });

    // Patient Info
    autoTable(doc, {
      startY: margin + 15,
      theme: 'grid',
      headStyles: { 
        fillColor: [0, 82, 164],
        textColor: 255,
        fontSize: 12
      },
      head: [['Patient Information', '']],
      body: [
        ['Patient Name', data.patientName],
        ['Date of Birth', new Date(data.dateOfBirth).toLocaleDateString()]
      ],
      columnStyles: {
        0: { cellWidth: 80, fontStyle: 'bold' },
        1: { cellWidth: 100 }
      },
      margin: { left: margin }
    });

    // Question
    autoTable(doc, {
      startY: (doc as any).lastAutoTable.finalY + 10,
      theme: 'grid',
      headStyles: { fillColor: [0, 82, 164], textColor: 255 },
      head: [['Patient Question']],
      body: [[data.question]],
      margin: { left: margin }
    });

    // Diagnosis
    autoTable(doc, {
      startY: (doc as any).lastAutoTable.finalY + 10,
      theme: 'grid',
      headStyles: { fillColor: [0, 82, 164], textColor: 255 },
      head: [['AI Diagnosis']],
      body: [[data.diagnosis]],
      margin: { left: margin }
    });

    // Treatment Plan
    autoTable(doc, {
      startY: (doc as any).lastAutoTable.finalY + 10,
      theme: 'grid',
      headStyles: { fillColor: [0, 82, 164], textColor: 255 },
      head: [['Treatment Plan']],
      body: [[data.treatment_plan]],
      margin: { left: margin }
    });

    // Footer
    const timestamp = data.timestamp || new Date().toLocaleString();
    doc.setFontSize(10);
    doc.setTextColor(128);
    doc.text(
      `Generated on: ${timestamp}`,
      pageWidth / 2,
      doc.internal.pageSize.getHeight() - 10,
      { align: 'center' }
    );

    // Save PDF
    const filename = `consultation_report_${data.patientName.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;
    doc.save(filename);
    return true;

  } catch (error) {
    console.error('PDF Generation Error:', error);
    return false;
  }
};