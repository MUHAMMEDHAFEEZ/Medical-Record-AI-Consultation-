import React, { useState, useEffect } from 'react';
import { generateMedicalPDF } from '../utils/pdfGenerator';

interface AIConsultationProps {
  nfcId: string;
  patientName: string;
  medicalRecord: any;
}

const AIConsultation: React.FC<AIConsultationProps> = ({ nfcId, medicalRecord }) => {
  const [question, setQuestion] = useState('');
  const [consultation, setConsultation] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleConsultation = async () => {
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      const response = await fetch(`http://localhost:8000/api/medical/consultation/${nfcId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error('Failed to get consultation');
      }

      const data = await response.json();
      
      // Clean up response data
      const cleanedData = {
        ...data,
        diagnosis: data.diagnosis?.replace(/\(DIAGNOSIS\)|\(TREATMENT PLAN\)/g, '').trim(),
        treatment_plan: data.treatment_plan?.replace(/\(DIAGNOSIS\)|\(TREATMENT PLAN\)/g, '').trim()
      };
      
      setConsultation(cleanedData);
      setError('');
      
    } catch (err) {
      console.error('AI Consultation Error:', err);
      setError('Failed to get AI consultation. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = () => {
    if (!medicalRecord || !consultation) return;

    try {
      const success = generateMedicalPDF({
        patientName: medicalRecord.full_name,
        dateOfBirth: medicalRecord.date_of_birth,
        bloodType: medicalRecord.blood_type,
        allergies: medicalRecord.allergies,
        chronicConditions: medicalRecord.chronic_conditions,
        medications: medicalRecord.medications,
        medicalHistory: medicalRecord.medical_history,
        consultation: {
          question,
          diagnosis: consultation.diagnosis,
          treatment_plan: consultation.treatment_plan,
          timestamp: new Date().toLocaleString()
        }
      });

      if (!success) {
        setError('Failed to generate PDF. Please try again.');
      }
    } catch (err) {
      console.error('PDF Generation Error:', err);
      setError('Failed to generate PDF. Please try again.');
    }
  };

  // Add new function for medical record download
  const handleDownloadMedicalRecord = async () => {
    if (!medicalRecord) {
      setError('No medical record data available');
      return;
    }

    try {
      setError('');
      console.log('Starting PDF generation...');

      const success = await generateMedicalPDF({
        patientName: medicalRecord.full_name,
        dateOfBirth: medicalRecord.date_of_birth,
        bloodType: medicalRecord.blood_type,
        allergies: medicalRecord.allergies || 'None',
        chronicConditions: medicalRecord.chronic_conditions || 'None',
        medications: medicalRecord.medications || 'No current medications',
        medicalHistory: medicalRecord.medical_history || 'No medical history'
      });

      if (!success) {
        throw new Error('PDF generation failed');
      }

    } catch (err) {
      console.error('PDF Generation Error:', err);
      setError('Failed to generate PDF. Please try again.');
    }
  };

  // Add a timeout warning if response takes too long
  useEffect(() => {
    let timeoutId: NodeJS.Timeout;
    
    if (loading) {
      timeoutId = setTimeout(() => {
        setError('Response is taking longer than expected. Please wait...');
      }, 10000); // Show message after 10 seconds
    }
    
    return () => {
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, [loading]);

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mt-8">
      {/* Header with Download Button */}
      <div className="flex justify-between items-center mb-6 border-b pb-4">
        <h2 className="text-2xl font-bold text-gray-800">AI Medical Consultation</h2>
        <button
          onClick={handleDownloadMedicalRecord}
          className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-md transition-colors flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Download Medical Record
        </button>
      </div>

      {/* Question Input Section */}
      <div className="bg-gray-50 p-4 rounded-lg mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Your Medical Question
        </label>
        <textarea
          className="w-full p-3 border rounded-md focus:ring-2 focus:ring-blue-500 bg-white"
          rows={4}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Enter your medical question here..."
        />
        <button
          onClick={handleConsultation}
          disabled={loading}
          className="mt-4 bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 disabled:bg-gray-400 w-full md:w-auto"
        >
          {loading ? (
            <div className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Getting Response...
            </div>
          ) : (
            'Get AI Consultation'
          )}
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {/* AI Response Section */}
      {consultation && (
        <div className="mt-6">
          {/* Consultation Header */}
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-bold text-gray-800">AI Consultation Response</h3>
            <button
              onClick={handleDownloadPDF}
              className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md transition-colors flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download Consultation
            </button>
          </div>

          {/* Diagnosis Section */}
          <div className="bg-gray-50 p-4 rounded-lg mb-4">
            <h4 className="text-lg font-semibold text-gray-800 mb-2">Diagnosis:</h4>
            <p className="text-gray-700 whitespace-pre-wrap">{consultation.diagnosis}</p>
        
          </div>

          {/* Treatment Plan Section */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="text-lg font-semibold text-gray-800 mb-2">Treatment Plan:</h4>
            <p className="text-gray-700 whitespace-pre-wrap">{consultation.treatment_plan}</p>
          </div>

          {/* Timestamp */}
          <div className="mt-4 text-sm text-gray-500">
            Generated on: {new Date().toLocaleString()}
          </div>
        </div>
      )}
    </div>
  );
};

export default AIConsultation;