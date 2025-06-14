import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { medicalRecords } from '../services/api';
import { generateConsultationPDF } from '../utils/pdfGenerator';
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
   id: string;
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
         id: result.id,
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
      const pdfUrl = medicalRecords.getMedicalRecordPDF(record.nfc_id);

      const link = document.createElement('a');
      link.href = pdfUrl;
      link.download = `medical-record-${record.full_name.replace(/\s+/g, '-')}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err) {
      console.error('PDF Download Error:', err);
      setError('Failed to download PDF. Please try again.');
    }
  };

  // const handleDownloadConsultationPDF = () => {
  //   if (!record || !consultationResult) return setError('No consultation data available');
  //   try {
  //     const success = generateConsultationPDF({
  //       patientName: record.full_name,
  //       dateOfBirth: record.date_of_birth,
  //       question: aiConsult.question,
  //       diagnosis: consultationResult.diagnosis,
  //       treatment_plan: consultationResult.treatment_plan,
  //       timestamp: consultationResult.timestamp
  //     });
  //     if (!success) throw new Error('Failed to generate consultation PDF');
  //   } catch (err) {
  //     console.error('Consultation PDF Generation Error:', err);
  //     setError('Failed to generate consultation PDF. Please try again.');
  //   }
  // };
  const handleDownloadConsultationPDF = () => {
  if (!record || !consultationResult) return setError('No consultation data available');
  
  try {
    // إنشاء رابط تنزيل PDF نتيجة الاستشارة
    const pdfUrl = `https://rj8vq174-8000.uks1.devtunnels.ms/api/medical-records/consultation/${consultationResult.id}/pdf/`;

    const link = document.createElement('a');
    link.href = pdfUrl;
    link.download = `consultation-${record.full_name.replace(/\s+/g, '-')}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (err) {
    console.error('Consultation PDF Download Error:', err);
    setError('Failed to download consultation PDF. Please try again.');
  }
};
  
  
  if (loading) return (
    <div className="fixed inset-0 bg-white z-50 flex flex-col items-center justify-center">
      <div className="text-center">
        <img
          src={logo}
          alt="DR AI Logo"
          className="h-12 sm:h-16 w-auto mx-auto mb-4"
        />
        <div className="flex items-center justify-center gap-2 mb-3">
          <div className="w-2 h-2 bg-green-600 rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-green-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-2 h-2 bg-green-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>
        <p className="text-green-600 font-medium text-sm sm:text-base">Loading medical record...</p>
      </div>
    </div>
  );

  if (error) return (
    <div className="fixed inset-0 bg-gray-50 z-50 flex flex-col items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-lg p-6 sm:p-8 text-center max-w-sm sm:max-w-md w-full">
        <div className="w-12 h-12 sm:w-16 sm:h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-6 h-6 sm:w-8 sm:h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.314 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
        <h2 className="text-base sm:text-lg font-semibold text-green-600 mb-2">Unable to Load Record</h2>
        <p className="text-green-600 mb-4 text-sm sm:text-base">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="bg-green-600 text-white px-4 sm:px-6 py-2 rounded-lg hover:bg-green-700 transition text-sm sm:text-base w-full sm:w-auto"
        >
          Try Again
        </button>
      </div>
    </div>
  );

  if (!record) return (
    <div className="fixed inset-0 bg-white z-50 flex flex-col items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-lg p-6 sm:p-8 text-center max-w-sm sm:max-w-md w-full">
        <div className="w-12 h-12 sm:w-16 sm:h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-6 h-6 sm:w-8 sm:h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h2 className="text-base sm:text-lg font-semibold text-green-600 mb-2">No Medical Record Found</h2>
        <p className="text-green-600 text-sm sm:text-base">The requested medical record could not be found.</p>
      </div>
    </div>
  ); return (
    <div className="min-h-screen bg-white rounded-[] border">
      <div className="w-full max-w-4xl mx-auto p-4 sm:p-6 lg:p-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 sm:gap-4 mb-4 sm:mb-6 bg-green-50 p-3 sm:p-4 rounded-lg">
          <div className="flex items-center gap-2 sm:gap-3">
            <img src={logo} alt="DR AI Logo" className="h-8 sm:h-10 w-auto" />
            <h1 className="text-lg sm:text-xl lg:text-2xl font-bold text-gray-800">Medical Record</h1>
          </div><button
            onClick={handleDownloadPDF}
            className="bg-green-600 text-white px-3 sm:px-4 h-[45px] rounded-lg flex items-center gap-2 hover:bg-green-700 text-xs sm:text-sm lg:text-base w-full sm:w-auto justify-center"
          >
            📄 Download PDF
          </button>
        </div>        <div className=" grid grid-cols-1 lg:grid-cols-2 gap-3 sm:gap-4 lg:gap-6 mb-4 sm:mb-6">
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
          </div>        </div>        <div className="mb-4 sm:mb-6 bg-gray-50 p-3 sm:p-4 rounded-lg sm:rounded-xl">
          <h2 className="text-base sm:text-lg font-semibold mb-2">💊 Current Medications</h2>
          <p className="whitespace-pre-wrap break-words text-sm sm:text-base">{record.medications}</p>
        </div>

        <div className="mb-4 sm:mb-6 bg-gray-50 p-3 sm:p-4 rounded-lg sm:rounded-xl">
          <h2 className="text-base sm:text-lg font-semibold mb-2">📖 Medical History</h2>
          <p className="whitespace-pre-wrap break-words text-sm sm:text-base">{record.medical_history}</p>
        </div>        <div className="bg-green-50 p-3 sm:p-4 lg:p-6 rounded-lg sm:rounded-xl">
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
                  <p><strong>💊 Treatment:</strong> <span className="break-words">{consultationResult.treatment_plan}</span></p>                  <p className="text-xs sm:text-sm text-gray-500 mt-2">🕒 {consultationResult.timestamp}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}


// grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 mb-6
