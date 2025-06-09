import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with default config
const axiosInstance = axios.create({
    baseURL: API_BASE_URL
});

// Add token to requests
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Auth API
export const auth = {
    register: async (userData: { username: string; password: string; email: string }) => {
        const response = await axiosInstance.post('/auth/register/', userData);
        return response.data;
    },
    
    login: async (credentials: { username: string; password: string }) => {
        const response = await axiosInstance.post('/auth/login/', credentials);
        return response.data;
    },
    
    logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }
};

// Medical Records API
const API_URL = 'http://localhost:8000/api';

export const medicalRecords = {
    getMedicalRecord: async () => {
        const response = await axiosInstance.get('/medical/record/');
        return response.data;
    },

    createMedicalRecord: async (data: any) => {
        const response = await axiosInstance.post('/medical/record/', data);
        return response.data;
    },    getPublicRecord: async (nfcId: string) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/medical/record/${nfcId}/`);
            return response.data;
        } catch (error) {
            console.error('Error fetching public record:', error);
            throw error;
        }
    },

    getMedicalRecordPDF: (nfcId: string) => 
        `${API_BASE_URL}/medical/record/${nfcId}/pdf/`,

    submitAIConsultation: async (nfcId: string, question: string) => {
        try {
            const response = await fetch(`${API_URL}/medical/consultation/${nfcId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question }),
            });
            if (!response.ok) {
                throw new Error('Failed to get AI consultation');
            }
            return response.json();
        } catch (error) {
            console.error('AI Consultation Error:', error);
            throw error;
        }
    },

    getConsultationPDF: (consultationId: string) => 
        `${API_BASE_URL}/medical/consultation/${consultationId}/pdf/`,
        
    getMedicalRecordByNFC: async (nfcId: string) => {
        try {
            const response = await fetch(`${API_BASE_URL}/medical/record/${nfcId}/`);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to fetch medical record');
            }
            
            return response.json();
        } catch (error) {
            console.error('Error fetching medical record:', error);
            throw error;
        }
    }
};
