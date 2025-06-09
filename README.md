# 🏥 Medical Record AI Consultation System

![Medical AI](dr-ai/frontend/src/assets/logo%20(2).png)

A sophisticated healthcare platform that combines medical record management with AI-powered medical consultation services.

## ✨ Features

- 🔐 **Secure Authentication System**
- 📋 **Medical Records Management**
- 🤖 **AI-Powered Medical Consultation**
- 📱 **Modern React Frontend**
- 🔒 **Django Backend with REST API**
- 📄 **PDF Report Generation**
- 🎯 **Real-time AI Responses**

## 🏗️ System Architecture

### Frontend Technologies
- **React** with TypeScript
- **Tailwind CSS** for styling
- **Vite** for build tooling
- **PDF Generation** capabilities

### Backend Technologies
- **Django** REST Framework
- **SQLite** Database
- **Ollama** for AI integration
- **Custom Authentication** system

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Node.js and npm/yarn
- Ollama (for AI features)

### Backend Setup
1. Navigate to the backend directory:
```bash
cd dr-ai/backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Unix/macOS
.\venv\Scripts\activate   # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the Django server:
```bash
python manage.py runserver
```

### Frontend Setup
1. Navigate to the frontend directory:
```bash
cd dr-ai/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## 🌐 Project Structure

### Backend Structure
```
backend/
├── apps/
│   ├── ai_service/        # AI consultation service
│   ├── authentication/    # User authentication
│   ├── medical_records/   # Medical records management
│   └── utils/            # Utility functions
└── drai/                 # Main Django project
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/       # React components
│   ├── services/        # API services
│   └── utils/           # Utility functions
```

## 🔑 Key Features Explained

### 1. Authentication System
- Secure user registration and login
- Token-based authentication
- Role-based access control

### 2. Medical Records Management
- Create and manage patient records
- View medical history
- Generate PDF reports

### 3. AI Consultation
- Real-time medical consultations
- Integration with Ollama
- Comprehensive response logging

## 🛠️ Development

### Running Tests
```bash
# Backend tests
python manage.py test

# Frontend tests
npm test
```

### API Documentation
The API endpoints are organized as follows:

- `/api/auth/` - Authentication endpoints
- `/api/medical-records/` - Medical records management
- `/api/ai-consultation/` - AI consultation services

## 📝 Logging

The system maintains comprehensive logs:
- AI response logs in `logs/ai_responses_*.log`
- System logs for debugging and monitoring

## 🔐 Security Features

- Secure password hashing
- Token-based authentication
- CORS protection
- Environment variable configuration

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Mohammed hafeez
- Contact: mohamedhafeez.dev@gmail.com

## 🙏 Acknowledgments

- Thanks to all contributors
- Built with Django and React
- Powered by Ollama AI

---

<div align="center">
Made with ❤️ for better healthcare management
</div>
