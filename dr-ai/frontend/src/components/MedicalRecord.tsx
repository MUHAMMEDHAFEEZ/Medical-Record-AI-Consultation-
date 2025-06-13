import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { medicalRecords } from '../services/api';
import { generateMedicalPDF, generateConsultationPDF } from '../utils/pdfGenerator';
import logo from '../assets/logo (2).png';
import { Link } from 'react-router-dom';

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
  if (!record) return <div className="p-4">No medical record found</div>;  return (
    <div className="w-full sm:max-w-4xl sm:mx-auto p-0 sm:p-4 lg:p-6 text-gray-800 min-h-screen">
      <div className="bg-white rounded-none sm:rounded-2xl shadow-none sm:shadow-lg p-0 sm:p-4 lg:p-6 border-0 sm:border border-green-100">        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 sm:gap-4 mb-4 sm:mb-6 bg-green-50 p-3 sm:p-4 rounded-lg mx-3 sm:mx-0 mt-3 sm:mt-0">
          <div className="flex items-center gap-2 sm:gap-3">
            <img src={logo} alt="DR AI Logo" className="h-8 sm:h-10 w-auto" />
            <h1 className="text-lg sm:text-xl lg:text-2xl font-bold">Medical Record</h1>
          </div>          <button
            onClick={handleDownloadPDF}
            className="bg-green-600 text-white px-3 sm:px-4 h-[45px] rounded-lg flex items-center gap-2 hover:bg-green-700 text-xs sm:text-sm lg:text-base w-full sm:w-auto justify-center"
          >
            📄 Download PDF
          </button>
        </div>        <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 sm:gap-4 lg:gap-6 mb-4 sm:mb-6 mx-3 sm:mx-0">
          <div className="bg-gray-50 p-3 sm:p-4 rounded-lg sm:rounded-xl">
            <h2 className="text-base sm:text-lg font-semibold mb-2">👤 Patient Information</h2>
            <div className="space-y-1 text-sm sm:text-base">
              <p><strong>Full Name:</strong> <span className="break-words">{record.full_name}</span></p>
              <p><strong>🎂 DOB:</strong> {new Date(record.date_of_birth).toLocaleDateString()}</p>
              <p><strong>🩸 Blood Type:</strong> {record.blood_type}</p>
            </div>
          </div>

          <div className="bg-gray-50 p-3 sm:p-4 rounded-lg sm:rounded-xl">
            <h2 className="text-base sm:text-lg font-semibold mb-2">📋 Medical Info</h2>
            <div className="space-y-1 text-sm sm:text-base">
              <p><strong>🌿 Allergies:</strong> <span className="break-words">{record.allergies}</span></p>
              <p><strong>🦴 Chronic Conditions:</strong> <span className="break-words">{record.chronic_conditions}</span></p>
            </div>
          </div>        </div>        <div className="mb-4 sm:mb-6 bg-gray-50 p-3 sm:p-4 rounded-lg sm:rounded-xl mx-3 sm:mx-0">
          <h2 className="text-base sm:text-lg font-semibold mb-2">💊 Current Medications</h2>
          <p className="whitespace-pre-wrap break-words text-sm sm:text-base">{record.medications}</p>
        </div>

        <div className="mb-4 sm:mb-6 bg-gray-50 p-3 sm:p-4 rounded-lg sm:rounded-xl mx-3 sm:mx-0">
          <h2 className="text-base sm:text-lg font-semibold mb-2">📖 Medical History</h2>
          <p className="whitespace-pre-wrap break-words text-sm sm:text-base">{record.medical_history}</p>
        </div>        <div className="bg-green-50 p-3 sm:p-4 lg:p-6 rounded-lg sm:rounded-xl mx-3 sm:mx-0">
          <h2 className="text-lg sm:text-xl font-bold mb-3 sm:mb-4">🤖 AI Consultation</h2>
          <form onSubmit={handleAIConsultation} className="space-y-3 sm:space-y-4">
            <textarea
              className="w-full rounded-lg sm:rounded-xl border border-gray-300 p-3 sm:p-4 focus:ring-2 focus:ring-green-400 text-sm sm:text-base resize-none"
              rows={3}
              placeholder="🧠 Ask your medical question..."
              value={aiConsult.question}
              onChange={(e) => setAiConsult({ question: e.target.value })}
            />            <button
              type="submit"
              disabled={isLoading}
              className={`w-full sm:w-auto bg-green-600 text-white px-4 sm:px-6 h-[45px] rounded-lg hover:bg-green-700 transition flex items-center justify-center gap-2 text-sm sm:text-base font-medium ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {isLoading ? '⏳ Processing...' : '📩 Get AI Consultation'}
            </button>
          </form>          {consultationResult && (
            <div className="mt-4 sm:mt-6 space-y-3 sm:space-y-4">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 sm:gap-4">
                <h3 className="text-base sm:text-lg font-semibold">🧬 AI Results</h3>                <button
                  onClick={handleDownloadConsultationPDF}
                  className="bg-green-500 text-white px-3 sm:px-4 h-[45px] rounded-lg hover:bg-green-600 flex items-center gap-2 text-xs sm:text-sm lg:text-base w-full sm:w-auto justify-center"
                >
                  📄 Download
                </button>
              </div>
              <div className="bg-white p-3 sm:p-4 rounded-lg shadow-sm">
                <div className="space-y-2 text-sm sm:text-base">
                  <p><strong>🩻 Diagnosis:</strong> <span className="break-words">{consultationResult.diagnosis}</span></p>
                  <p><strong>💊 Treatment:</strong> <span className="break-words">{consultationResult.treatment_plan}</span></p>
                  <p className="text-xs sm:text-sm text-gray-500 mt-2">🕒 {consultationResult.timestamp}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
  
}
