import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { medicalRecords } from '../services/api';

interface MedicalRecordData {
  full_name: string;
  date_of_birth: string;
  blood_type: string;
  allergies: string;
  chronic_conditions: string;
  medications: string;
  medical_history: string;
}

export default function PublicRecord() {
  const { nfcId } = useParams();
  const [record, setRecord] = useState<MedicalRecordData | null>(null);
  const [question, setQuestion] = useState('');
  const [consultation, setConsultation] = useState<{ diagnosis: string; treatment_plan: string } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadMedicalRecord();
  }, [nfcId]);

  const loadMedicalRecord = async () => {
    try {
      const data = await medicalRecords.getPublicRecord(nfcId || '');
      setRecord(data);
    } catch (err) {
      setError('Failed to load medical record');
    } finally {
      setLoading(false);
    }
  };

  const handleConsultation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!nfcId || !question) return;

    try {
      const result = await medicalRecords.submitAIConsultation(nfcId, question);
      setConsultation(result);
    } catch (err) {
      setError('Failed to get AI consultation');
    }
  };

  const downloadPDF = () => {
    if (!nfcId) return;
    window.open(medicalRecords.getMedicalRecordPDF(nfcId));
  };

  if (loading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;
  if (!record) return <div className="p-4">No medical record found</div>;

  return (
    <div className="container mx-auto p-4">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">{record.full_name}'s Medical Record</h2>
        
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">Date of Birth</label>
            <p className="mt-1 text-gray-900">{record.date_of_birth}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Blood Type</label>
            <p className="mt-1 text-gray-900">{record.blood_type}</p>
          </div>
        </div>

        <div className="space-y-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">Allergies</label>
            <p className="mt-1 text-gray-900">{record.allergies || 'None'}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Chronic Conditions</label>
            <p className="mt-1 text-gray-900">{record.chronic_conditions || 'None'}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Current Medications</label>
            <p className="mt-1 whitespace-pre-wrap text-gray-900">{record.medications || 'None'}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Medical History</label>
            <p className="mt-1 whitespace-pre-wrap text-gray-900">{record.medical_history}</p>
          </div>
        </div>

        <button
          onClick={downloadPDF}
          className="mb-6 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
        >
          Download PDF Report
        </button>

        <div className="border-t pt-6">
          <h3 className="text-xl font-bold mb-4 text-gray-800">AI Consultation</h3>
          <form onSubmit={handleConsultation} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Ask a medical question
              </label>
              <textarea
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                rows={3}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Type your medical question here..."
              />
            </div>
            <button
              type="submit"
              className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition-colors"
            >
              Get AI Consultation
            </button>
          </form>

          {consultation && (
            <div className="mt-4 space-y-4">
              <div>
                <h4 className="text-lg font-medium mb-2">Diagnosis:</h4>
                <div className="bg-gray-50 p-4 rounded">
                  {consultation.diagnosis}
                </div>
              </div>
              <div>
                <h4 className="text-lg font-medium mb-2">Treatment Plan:</h4>
                <div className="bg-gray-50 p-4 rounded">
                  {consultation.treatment_plan}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
