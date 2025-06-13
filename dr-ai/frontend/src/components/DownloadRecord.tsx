import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { medicalRecords } from '../services/api';
import { generateMedicalPDF } from '../utils/pdfGenerator';
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

export default function DownloadRecord() {
  const { id } = useParams<{ id: string }>();
  const [record, setRecord] = useState<MedicalRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
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

    fetchData();
  }, [id]);

  const handleDownload = () => {
    if (!record) return setError('No data to generate PDF');

    const success = generateMedicalPDF({
      patientName: record.full_name,
      dateOfBirth: record.date_of_birth,
      bloodType: record.blood_type,
      allergies: record.allergies,
      chronicConditions: record.chronic_conditions,
      medications: record.medications,
      medicalHistory: record.medical_history
    });

    if (!success) {
      setError('PDF generation failed');
    }
  };

  if (loading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;
  if (!record) return <div className="p-4">No medical record found</div>;

  return (
    <div className="max-w-xl mx-auto p-6 bg-white shadow-lg rounded-xl border border-green-100 mt-10">
      <div className="flex items-center gap-3 mb-6">
        <img src={logo} alt="DR AI Logo" className="h-10 w-auto" />
        <h1 className="text-2xl font-bold text-green-800">Download Medical Record</h1>
      </div>
      <div className="mb-4 text-sm">
        <p><strong>Full Name:</strong> {record.full_name}</p>
        <p><strong>Date of Birth:</strong> {new Date(record.date_of_birth).toLocaleDateString()}</p>
        <p><strong>Blood Type:</strong> {record.blood_type}</p>
      </div>
      <button
        onClick={handleDownload}
        className="bg-green-600 hover:bg-green-700 text-white py-2 px-6 rounded-full w-full font-medium"
      >
        📄 Download Medical Record PDF
      </button>
    </div>
  );
}
