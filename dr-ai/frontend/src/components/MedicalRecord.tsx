import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { medicalRecords } from '../services/api';
import { generateMedicalPDF, generateConsultationPDF } from '../utils/pdfGenerator';

interface MedicalRecord {
  id: string;
  nfc_id: string;
  full_name: string;  
  date_of_birth: string;
  medical_history: string;
  created_at: string;
  blood_type: string;
  allergies: string;
  chronic_conditions: string;
  medications: string;
}

interface ConsultationResult {
  diagnosis: string;
  treatment_plan: string;
  timestamp?: string;
}

export default function MedicalRecord() {
  const { id } = useParams<{ id: string }>();  // Get NFC ID from URL
  const [record, setRecord] = useState<MedicalRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [aiConsult, setAiConsult] = useState({ question: '' });
  const [consultationResult, setConsultationResult] = useState<ConsultationResult | null>(null);
  const [isLoading, setIsLoading] = useState(false); // New loading state for AI consultation

  useEffect(() => {
    loadMedicalRecord();
  }, [id]); // Add id as dependency

  const loadMedicalRecord = async () => {
    try {
      if (!id) {
        throw new Error('No NFC ID provided');
      }
      // Use public endpoint
      const data = await medicalRecords.getMedicalRecordByNFC(id);
      setRecord(data);
    } catch (err) {
      console.error('Error loading medical record:', err);
      setError('Failed to load medical record');
    } finally {
      setLoading(false);
    }
  };

  const handleAIConsultation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!record || isLoading) return; // Prevent multiple submissions

    try {
      setIsLoading(true);
      setError('');
      const result = await medicalRecords.submitAIConsultation(record.nfc_id, aiConsult.question);
      
      // Parse the AI response into structured format
      setConsultationResult({
        diagnosis: result.diagnosis,
        treatment_plan: result.treatment_plan,
        timestamp: new Date().toLocaleString()
      });
    } catch (err) {
      console.error('AI Consultation Error:', err);
      setError('Failed to get AI consultation');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadPDF = () => {
    if (!record) {
      setError('No medical record data available');
      return;
    }

    console.log('Generating PDF with data:', record); // Add logging

    try {
      const success = generateMedicalPDF({
        patientName: record.full_name || 'N/A',
        dateOfBirth: record.date_of_birth || 'N/A',
        bloodType: record.blood_type || 'N/A',
        allergies: record.allergies || 'None',
        chronicConditions: record.chronic_conditions || 'None',
        medications: record.medications || 'None',
        medicalHistory: record.medical_history || 'No history available'
      });

      if (!success) {
        throw new Error('Failed to generate PDF');
      }
    } catch (err) {
      console.error('PDF Generation Error:', err);
      setError('Failed to generate PDF. Please try again.');
    }
  };

  const handleDownloadConsultationPDF = () => {
    if (!record || !consultationResult) {
      setError('No consultation data available');
      return;
    }

    try {
      const success = generateConsultationPDF({
        patientName: record.full_name,
        dateOfBirth: record.date_of_birth,
        question: aiConsult.question,
        diagnosis: consultationResult.diagnosis,
        treatment_plan: consultationResult.treatment_plan,
        timestamp: consultationResult.timestamp
      });

      if (!success) {
        throw new Error('Failed to generate consultation PDF');
      }
    } catch (err) {
      console.error('Consultation PDF Generation Error:', err);
      setError('Failed to generate consultation PDF. Please try again.');
    }
  };

  if (loading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;
  if (!record) return <div className="p-4">No medical record found</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        {/* Header Section */}
        <div className="flex justify-between items-center mb-8 border-b pb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Medical Record</h1>
            <p className="text-gray-600 mt-1">Patient ID: {record.nfc_id}</p>
          </div>
          <button
            onClick={handleDownloadPDF}
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-md transition-colors flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Download PDF
          </button>
        </div>

        {/* Patient Information Grid */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="bg-gray-50 p-4 rounded-lg">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Patient Information</h2>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700">Full Name</label>
                <p className="text-lg font-medium">{record.full_name}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Date of Birth</label>
                <p className="text-lg">{new Date(record.date_of_birth).toLocaleDateString()}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Blood Type</label>
                <p className="text-lg font-medium">{record.blood_type}</p>
              </div>
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Medical Information</h2>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700">Allergies</label>
                <p className="text-lg">{record.allergies || 'None'}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Chronic Conditions</label>
                <p className="text-lg">{record.chronic_conditions || 'None'}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Medications Section */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Current Medications</h2>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="whitespace-pre-wrap">{record.medications || 'No current medications'}</p>
          </div>
        </div>

        {/* Medical History Section */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Medical History</h2>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="whitespace-pre-wrap">{record.medical_history}</p>
          </div>
        </div>

        {/* AI Consultation Section */}
        <div className="border-t pt-8">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">AI Consultation</h2>
          <form onSubmit={handleAIConsultation} className="space-y-4">
            <div>
              <label className="block text-lg font-medium text-gray-700 mb-2">
                Ask a Medical Question
              </label>
              <textarea
                className="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 min-h-[120px]"
                value={aiConsult.question}
                onChange={(e) => setAiConsult({ question: e.target.value })}
                placeholder="Type your medical question here..."
              />
            </div>
            <div className="flex justify-center mt-4">
              <button
                type="submit"
                disabled={isLoading}
                className={`flex items-center justify-center gap-2 ${
                  isLoading 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-green-600 hover:bg-green-700'
                } text-white px-6 py-3 rounded-lg transition-colors w-full md:w-auto`}
              >
                {isLoading ? (
                  <>
                    <svg 
                      className="animate-spin h-5 w-5 text-white" 
                      xmlns="http://www.w3.org/2000/svg" 
                      fill="none" 
                      viewBox="0 0 24 24"
                    >
                      <circle 
                        className="opacity-25" 
                        cx="12" 
                        cy="12" 
                        r="10" 
                        stroke="currentColor" 
                        strokeWidth="4"
                      />
                      <path 
                        className="opacity-75" 
                        fill="currentColor" 
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      />
                    </svg>
                    Processing...
                  </>
                ) : (
                  'Get AI Consultation'
                )}
              </button>
            </div>
          </form>

          {consultationResult && (
            <div className="mt-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-semibold">AI Consultation Results</h3>
                <button
                  onClick={handleDownloadConsultationPDF}
                  className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md transition-colors flex items-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Download Consultation PDF
                </button>
              </div>

              <div className="space-y-4">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-semibold mb-2">Diagnosis:</h4>
                  <p className="whitespace-pre-wrap">{consultationResult.diagnosis}</p>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-semibold mb-2">Treatment Plan:</h4>
                  <p className="whitespace-pre-wrap">{consultationResult.treatment_plan}</p>
                </div>

                <div className="text-sm text-gray-500">
                  Generated on: {consultationResult.timestamp}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
