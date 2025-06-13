import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { medicalRecords } from '../services/api';
import { generateMedicalPDF, generateConsultationPDF } from '../utils/pdfGenerator';
import logo from '../assets/logo (2).png';

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
  const { id } = useParams<{ id: string }>();
  const [record, setRecord] = useState<MedicalRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [aiConsult, setAiConsult] = useState({ question: '' });
  const [consultationResult, setConsultationResult] = useState<ConsultationResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadMedicalRecord();
  }, [id]);

  const loadMedicalRecord = async () => {
    try {
      if (!id) throw new Error('No NFC ID provided');
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
    if (!record || isLoading) return;

    try {
      setIsLoading(true);
      setError('');
      const result = await medicalRecords.submitAIConsultation(record.nfc_id, aiConsult.question);
      setConsultationResult({
        diagnosis: result.diagnosis,
        treatment_plan: result.treatment_plan,
        timestamp: new Date().toLocaleString(),
      });
    } catch (err) {
      console.error('AI Consultation Error:', err);
      setError('Failed to get AI consultation');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadPDF = () => {
    if (!record) return setError('No medical record data available');
    try {
      const success = generateMedicalPDF({
        patientName: record.full_name,
        dateOfBirth: record.date_of_birth,
        bloodType: record.blood_type,
        allergies: record.allergies,
        chronicConditions: record.chronic_conditions,
        medications: record.medications,
        medicalHistory: record.medical_history
      });
      if (!success) throw new Error('Failed to generate PDF');
    } catch (err) {
      console.error('PDF Generation Error:', err);
      setError('Failed to generate PDF. Please try again.');
    }
  };

  const handleDownloadConsultationPDF = () => {
    if (!record || !consultationResult) return setError('No consultation data available');
    try {
      const success = generateConsultationPDF({
        patientName: record.full_name,
        dateOfBirth: record.date_of_birth,
        question: aiConsult.question,
        diagnosis: consultationResult.diagnosis,
        treatment_plan: consultationResult.treatment_plan,
        timestamp: consultationResult.timestamp
      });
      if (!success) throw new Error('Failed to generate consultation PDF');
    } catch (err) {
      console.error('Consultation PDF Generation Error:', err);
      setError('Failed to generate consultation PDF. Please try again.');
    }
  };

  if (loading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;
  if (!record) return <div className="p-4">No medical record found</div>;
  return (
    <div className="min-h-screen bg-gray-50 px-2 py-4 sm:px-4 sm:py-6">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-xl sm:rounded-2xl shadow-lg border border-green-100 overflow-hidden">

          <div className="bg-green-50 p-3 sm:p-4 border-b border-green-100">
            <div className="flex flex-col space-y-3 sm:space-y-0 sm:flex-row sm:justify-between sm:items-center">
              <div className="flex items-center gap-2 sm:gap-3">
                <img src={logo} alt="DR AI Logo" className="h-8 sm:h-10 w-auto flex-shrink-0" />
                <h1 className="text-lg sm:text-xl md:text-2xl font-bold text-gray-800">Medical Record</h1>
              </div>
              <button
                onClick={handleDownloadPDF}
                className="bg-green-600 text-white px-3 py-2 sm:px-4 sm:py-2 rounded-lg sm:rounded-full flex items-center justify-center gap-2 hover:bg-green-700 transition-colors text-sm font-medium w-full sm:w-auto"
              >
                📄 Download PDF
              </button>
            </div>
          </div>          <div className="p-3 sm:p-4 md:p-6 space-y-4 sm:space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 sm:gap-4 md:gap-6">
              <div className="bg-gray-50 p-3 sm:p-4 rounded-lg">
                <h2 className="text-base sm:text-lg font-semibold mb-3 text-gray-800 flex items-center gap-2">
                  👤 Patient Information
                </h2>
                <div className="space-y-2 text-sm sm:text-base">
                  <p className="flex flex-col sm:flex-row sm:items-center gap-1">
                    <strong className="text-gray-700 min-w-fit">Full Name:</strong> 
                    <span className="text-gray-900">{record.full_name}</span>
                  </p>
                  <p className="flex flex-col sm:flex-row sm:items-center gap-1">
                    <strong className="text-gray-700 min-w-fit">🎂 DOB:</strong> 
                    <span className="text-gray-900">{new Date(record.date_of_birth).toLocaleDateString()}</span>
                  </p>
                  <p className="flex flex-col sm:flex-row sm:items-center gap-1">
                    <strong className="text-gray-700 min-w-fit">🩸 Blood Type:</strong> 
                    <span className="text-gray-900">{record.blood_type}</span>
                  </p>
                </div>
              </div>

              <div className="bg-gray-50 p-3 sm:p-4 rounded-lg">
                <h2 className="text-base sm:text-lg font-semibold mb-3 text-gray-800 flex items-center gap-2">
                  📋 Medical Info
                </h2>
                <div className="space-y-2 text-sm sm:text-base">
                  <p className="flex flex-col gap-1">
                    <strong className="text-gray-700">🌿 Allergies:</strong> 
                    <span className="text-gray-900 break-words">{record.allergies}</span>
                  </p>
                  <p className="flex flex-col gap-1">
                    <strong className="text-gray-700">🦴 Chronic Conditions:</strong> 
                    <span className="text-gray-900 break-words">{record.chronic_conditions}</span>
                  </p>
                </div>
              </div>
            </div>            <div className="bg-gray-50 p-3 sm:p-4 rounded-lg">
              <h2 className="text-base sm:text-lg font-semibold mb-3 text-gray-800 flex items-center gap-2">
                💊 Current Medications
              </h2>
              <div className="text-sm sm:text-base text-gray-900 whitespace-pre-wrap break-words leading-relaxed">
                {record.medications}
              </div>
            </div>

            <div className="bg-gray-50 p-3 sm:p-4 rounded-lg">
              <h2 className="text-base sm:text-lg font-semibold mb-3 text-gray-800 flex items-center gap-2">
                📖 Medical History
              </h2>
              <div className="text-sm sm:text-base text-gray-900 whitespace-pre-wrap break-words leading-relaxed">
                {record.medical_history}
              </div>
            </div>            <div className="bg-green-50 p-3 sm:p-4 md:p-6 rounded-lg border border-green-200">
              <h2 className="text-lg sm:text-xl font-bold mb-4 text-gray-800 flex items-center gap-2">
                🤖 AI Consultation
              </h2>
              <form onSubmit={handleAIConsultation} className="space-y-4">
                <div>
                  <textarea
                    className="w-full rounded-lg border border-gray-300 p-3 sm:p-4 focus:ring-2 focus:ring-green-400 focus:border-green-400 text-sm sm:text-base resize-none transition-all duration-200"
                    rows={4}
                    placeholder="🧠 Ask your medical question..."
                    value={aiConsult.question}
                    onChange={(e) => setAiConsult({ question: e.target.value })}
                  />
                </div>
                <button
                  type="submit"
                  disabled={isLoading}
                  className={`w-full bg-green-600 text-white px-4 py-3 rounded-lg hover:bg-green-700 transition-all duration-200 flex items-center justify-center gap-2 text-sm sm:text-base font-medium ${isLoading ? 'opacity-50 cursor-not-allowed' : 'active:scale-95'}`}
                >
                  {isLoading ? '⏳ Processing...' : '📩 Get AI Consultation'}
                </button>
              </form>

          {consultationResult && (
            <div className="mt-6 space-y-4">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                <h3 className="text-lg font-semibold">🧬 AI Results</h3>
                <button
                  onClick={handleDownloadConsultationPDF}
                  className="bg-green-500 text-white px-4 py-2 rounded-full hover:bg-green-600 flex items-center gap-2 text-sm sm:text-base"
                >
                  📄 Download
                </button>
              </div>
              <div className="bg-white p-4 rounded-lg shadow-sm">
                <p><strong>🩻 Diagnosis:</strong> {consultationResult.diagnosis}</p>
                <p><strong>💊 Treatment:</strong> {consultationResult.treatment_plan}</p>
                <p className="text-sm text-gray-500 mt-2">🕒 {consultationResult.timestamp}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
