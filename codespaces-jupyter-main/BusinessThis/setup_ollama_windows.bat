@echo off
echo 🚀 BusinessThis Ollama Setup for Windows
echo ========================================

echo.
echo Step 1: Downloading Ollama...
powershell -Command "Invoke-WebRequest -Uri https://ollama.com/download/windows -OutFile ollama-windows-amd64.exe"

if not exist "ollama-windows-amd64.exe" (
    echo ❌ Failed to download Ollama installer
    echo Please download manually from: https://ollama.com/download/windows
    pause
    exit /b 1
)

echo ✅ Ollama installer downloaded successfully!
echo.
echo Step 2: Installing Ollama...
echo Please follow the installation wizard that will open...
ollama-windows-amd64.exe

echo.
echo Step 3: Starting Ollama service...
echo This will open a new window. Keep it open!
start "Ollama Service" cmd /k "ollama serve"

echo.
echo Step 4: Waiting for Ollama to start...
timeout /t 5 /nobreak > nul

echo.
echo Step 5: Pulling Mistral model...
echo This may take 5-10 minutes depending on your internet speed...
ollama pull mistral

if %errorlevel% neq 0 (
    echo ❌ Failed to pull Mistral model
    echo Please run manually: ollama pull mistral
    pause
    exit /b 1
)

echo.
echo Step 6: Testing Ollama...
ollama list

echo.
echo Step 7: Testing API...
curl -s http://localhost:11434/api/tags > nul
if %errorlevel% equ 0 (
    echo ✅ Ollama is working correctly!
) else (
    echo ⚠️  Ollama API test failed, but service might still be starting...
)

echo.
echo 🎉 Setup Complete!
echo.
echo Next steps:
echo 1. Make sure the "Ollama Service" window is still open
echo 2. Run: python test_ollama_integration.py
echo 3. Start your backend: python run_backend.py
echo 4. Start your frontend: python run_frontend.py
echo.
echo For detailed instructions, see: WINDOWS_OLLAMA_SETUP.md
echo.
pause
