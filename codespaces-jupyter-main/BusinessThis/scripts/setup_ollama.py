#!/usr/bin/env python3
"""
Ollama Setup Script for BusinessThis
Automates the installation and configuration of Ollama
"""
import subprocess
import requests
import time
import os
import sys
from pathlib import Path

def run_command(command, shell=True):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_ollama_installed():
    """Check if Ollama is already installed"""
    success, _, _ = run_command("ollama --version")
    return success

def install_ollama_windows():
    """Install Ollama on Windows"""
    print("Installing Ollama on Windows...")
    
    # Download Ollama
    download_cmd = 'powershell -Command "Invoke-WebRequest -Uri https://ollama.com/download/windows -OutFile ollama-windows-amd64.exe"'
    success, stdout, stderr = run_command(download_cmd)
    
    if not success:
        print(f"Failed to download Ollama: {stderr}")
        return False
    
    print("Downloaded Ollama installer. Please run 'ollama-windows-amd64.exe' to install.")
    return True

def install_ollama_linux():
    """Install Ollama on Linux"""
    print("Installing Ollama on Linux...")
    
    install_cmd = "curl -fsSL https://ollama.com/install.sh | sh"
    success, stdout, stderr = run_command(install_cmd)
    
    if not success:
        print(f"Failed to install Ollama: {stderr}")
        return False
    
    print("Ollama installed successfully!")
    return True

def start_ollama_service():
    """Start Ollama service"""
    print("Starting Ollama service...")
    
    # Try to start Ollama in background
    success, stdout, stderr = run_command("ollama serve")
    
    if not success:
        print(f"Failed to start Ollama service: {stderr}")
        return False
    
    print("Ollama service started!")
    return True

def pull_mistral_model():
    """Pull Mistral 7B model"""
    print("Pulling Mistral 7B model (this may take a few minutes)...")
    
    success, stdout, stderr = run_command("ollama pull mistral")
    
    if not success:
        print(f"Failed to pull Mistral model: {stderr}")
        return False
    
    print("Mistral model pulled successfully!")
    return True

def test_ollama_connection():
    """Test Ollama API connection"""
    print("Testing Ollama connection...")
    
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama is running and accessible!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"Retrying connection... ({i+1}/{max_retries})")
        time.sleep(2)
    
    print("❌ Failed to connect to Ollama after multiple attempts")
    return False

def test_mistral_model():
    """Test Mistral model with a simple query"""
    print("Testing Mistral model...")
    
    try:
        payload = {
            "model": "mistral",
            "prompt": "Hello, are you working?",
            "stream": False
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Mistral model is working!")
            print(f"Response: {result.get('response', '')[:100]}...")
            return True
        else:
            print(f"❌ Mistral model test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Mistral model test failed: {e}")
        return False

def create_env_file():
    """Create or update .env file with Ollama configuration"""
    env_file = Path(".env")
    
    ollama_config = """
# Ollama Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral
"""
    
    if env_file.exists():
        # Read existing content
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Add Ollama config if not present
        if "OLLAMA_URL" not in content:
            with open(env_file, 'a') as f:
                f.write(ollama_config)
            print("✅ Added Ollama configuration to .env file")
        else:
            print("✅ Ollama configuration already exists in .env file")
    else:
        # Create new .env file
        with open(env_file, 'w') as f:
            f.write(ollama_config)
        print("✅ Created .env file with Ollama configuration")

def main():
    """Main setup function"""
    print("🚀 BusinessThis Ollama Setup Script")
    print("=" * 50)
    
    # Check if Ollama is already installed
    if check_ollama_installed():
        print("✅ Ollama is already installed!")
    else:
        print("Installing Ollama...")
        
        # Detect OS and install accordingly
        if sys.platform.startswith('win'):
            if not install_ollama_windows():
                print("❌ Failed to download Ollama for Windows")
                print("Please download manually from: https://ollama.com/download/windows")
                return False
        elif sys.platform.startswith('linux'):
            if not install_ollama_linux():
                print("❌ Failed to install Ollama on Linux")
                return False
        else:
            print("❌ Unsupported operating system")
            print("Please install Ollama manually from: https://ollama.com")
            return False
    
    # Start Ollama service
    print("\nStarting Ollama service...")
    if not start_ollama_service():
        print("❌ Failed to start Ollama service")
        print("Please start Ollama manually: ollama serve")
        return False
    
    # Wait a moment for service to start
    time.sleep(3)
    
    # Test connection
    if not test_ollama_connection():
        print("❌ Ollama service is not accessible")
        return False
    
    # Pull Mistral model
    if not pull_mistral_model():
        print("❌ Failed to pull Mistral model")
        return False
    
    # Test Mistral model
    if not test_mistral_model():
        print("❌ Mistral model is not working")
        return False
    
    # Create/update .env file
    create_env_file()
    
    print("\n🎉 Ollama setup completed successfully!")
    print("\nNext steps:")
    print("1. Start your Flask backend: python run_backend.py")
    print("2. Test the health endpoint: curl http://localhost:5000/api/health/ollama")
    print("3. Start using AI features in your BusinessThis app!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
