# Dr AI - Medical Record System with AI Integration

A modern medical record system that uses NFC technology for patient identification and AI-powered medical consultations using the Medllama2 model.

## Features

- User Authentication System
- Medical Record Management
- NFC Integration for Patient Identification
- AI-Powered Medical Consultations
- PDF Report Generation
- Modern React Frontend with Tailwind CSS
- RESTful Django Backend

## Prerequisites

- Python 3.8+
- Node.js 14+
- Ollama with medllama2 model
- NFC-enabled device for testing

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd dr-ai
```

2. Install Ollama and the medllama2 model:
```bash
# Install Ollama from: https://ollama.ai/
ollama pull medllama2
```

3. Run the development setup script:
```powershell
.\start-dev.ps1
```

This script will:
- Install frontend dependencies
- Set up Python virtual environment
- Install backend dependencies
- Initialize the database
- Create a superuser account
- Start the development servers
- Start the Ollama model

## Usage

1. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Interface: http://localhost:8000/admin

2. Login with your credentials

3. Create a medical record and link it to an NFC tag

4. Access patient records by scanning NFC tags

5. Use the AI consultation feature to get medical advice

## Project Structure

```
dr-ai/
├── backend/
│   ├── apps/
│   │   ├── ai_service/       # AI integration with Ollama
│   │   ├── authentication/   # User authentication
│   │   └── medical_records/  # Medical record management
│   └── drai/                 # Django project settings
└── frontend/
    └── src/
        ├── components/       # React components
        └── services/        # API integration
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security Notice

This application handles sensitive medical data. In a production environment, ensure:

- Proper SSL/TLS encryption
- Secure database configuration
- Regular security audits
- HIPAA compliance (if used in the US)
- GDPR compliance (if used in the EU)
