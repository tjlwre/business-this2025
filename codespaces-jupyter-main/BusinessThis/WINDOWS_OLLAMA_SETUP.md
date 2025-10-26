# Windows Ollama Setup Guide

## 🚀 Quick Setup for BusinessThis

### Step 1: Download Ollama

1. **Download the installer:**
   - Go to: https://ollama.com/download/windows
   - Or run this PowerShell command:
   ```powershell
   Invoke-WebRequest -Uri https://ollama.com/download/windows -OutFile ollama-windows-amd64.exe
   ```

2. **Run the installer:**
   ```cmd
   ollama-windows-amd64.exe
   ```
   - Follow the installation wizard
   - Ollama will be installed to your system

### Step 2: Start Ollama Service

1. **Open Command Prompt or PowerShell as Administrator**

2. **Start Ollama service:**
   ```cmd
   ollama serve
   ```
   - This will start Ollama on `localhost:11434`
   - Keep this terminal window open

### Step 3: Pull Mistral Model

1. **Open a new Command Prompt/PowerShell window**

2. **Pull the Mistral 7B model:**
   ```cmd
   ollama pull mistral
   ```
   - This downloads ~4GB model (takes 5-10 minutes)
   - You'll see progress indicators

3. **Verify installation:**
   ```cmd
   ollama list
   ```
   - Should show `mistral` in the list

### Step 4: Test Ollama

1. **Test basic functionality:**
   ```cmd
   ollama run mistral "Hello, are you working?"
   ```

2. **Test API endpoint:**
   ```powershell
   curl http://localhost:11434/api/tags
   ```

### Step 5: Configure BusinessThis

1. **Add to your `.env` file:**
   ```env
   OLLAMA_URL=http://localhost:11434
   OLLAMA_MODEL=mistral
   ```

2. **Test the integration:**
   ```cmd
   python test_ollama_integration.py
   ```

## 🔧 Troubleshooting

### Common Issues

1. **"ollama is not recognized"**
   - Restart your terminal after installation
   - Add Ollama to your PATH manually if needed

2. **"Connection refused"**
   - Make sure `ollama serve` is running
   - Check if port 11434 is available

3. **"Model not found"**
   - Run `ollama pull mistral` again
   - Check with `ollama list`

4. **Out of memory**
   - Close other applications
   - Ensure 6GB+ RAM available

### Performance Tips

1. **Keep Ollama running:**
   - Don't close the `ollama serve` window
   - Ollama keeps models in memory for faster responses

2. **Monitor resources:**
   ```cmd
   ollama ps
   ```

3. **Stop unused models:**
   ```cmd
   ollama stop mistral
   ```

## 🎯 Next Steps

Once Ollama is running:

1. **Start your backend:**
   ```cmd
   python run_backend.py
   ```

2. **Test the health endpoint:**
   ```cmd
   curl http://localhost:5000/api/health/ollama
   ```

3. **Start your frontend:**
   ```cmd
   python run_frontend.py
   ```

4. **Test AI features in the web interface**

## 📊 System Requirements

- **RAM**: 6GB minimum (8GB recommended)
- **Storage**: 4GB for Mistral model
- **CPU**: Modern multi-core processor
- **OS**: Windows 10/11

## 🎉 Success!

Once everything is working, you'll have:
- ✅ Zero AI API costs
- ✅ Unlimited AI features
- ✅ Local privacy
- ✅ Fast responses

Your BusinessThis app is now powered by free, local AI! 🚀
