# Check if Ollama is installed
if (-not (Get-Command "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "Ollama is not installed. Please install it from https://ollama.ai/"
    exit 1
}

# Pull the medllama2 model
Write-Host "Pulling medllama2 model..."
ollama pull medllama2

# Install frontend dependencies
Write-Host "`nInstalling frontend dependencies..."
Set-Location -Path "frontend"
npm install --legacy-peer-deps

# Install backend dependencies
Write-Host "`nInstalling backend dependencies..."
Set-Location -Path "../backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database and create superuser
Write-Host "`nInitializing database..."
python manage.py makemigrations
python manage.py migrate
Write-Host "`nCreating default superuser..."
python manage.py create_superuser

# Start Ollama in the background
Write-Host "`nStarting Ollama with medllama2 model..."
Start-Process -FilePath "powershell" -ArgumentList "-NoExit -Command `"ollama run medllama2`""

# Start frontend development server
Write-Host "`nStarting frontend development server..."
Start-Process -FilePath "powershell" -ArgumentList "-NoExit -Command `"cd frontend; npm start`""

# Start backend development server
Write-Host "`nStarting backend development server..."
Start-Process -FilePath "powershell" -ArgumentList "-NoExit -Command `"cd backend; .\venv\Scripts\Activate.ps1; python manage.py runserver`""

Write-Host "`nDevelopment environment is ready!"
Write-Host "Frontend: http://localhost:3000"
Write-Host "Backend: http://localhost:8000"
Write-Host "Admin Interface: http://localhost:8000/admin"
Write-Host "Default superuser credentials:"
Write-Host "Username: admin"
Write-Host "Password: admin123"
