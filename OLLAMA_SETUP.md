# Ollama Setup Guide for BusinessThis

## Overview

BusinessThis uses Ollama with Mistral 7B model for AI-powered financial coaching. This eliminates OpenAI API costs while providing unlimited AI features.

## System Requirements

- **RAM**: Minimum 6GB (8GB recommended with Flask backend)
- **CPU**: Modern multi-core processor (inference runs on CPU)
- **Storage**: ~4GB for Mistral 7B model
- **OS**: Windows, macOS, or Linux

## Installation

### Windows

1. **Download Ollama**
   ```powershell
   # Download from https://ollama.com/download/windows
   # Or use PowerShell:
   Invoke-WebRequest -Uri https://ollama.com/download/windows -OutFile ollama-windows-amd64.exe
   ```

2. **Install and Run**
   ```cmd
   # Run the installer
   ollama-windows-amd64.exe
   
   # Start Ollama service
   ollama serve
   ```

3. **Pull Mistral Model**
   ```cmd
   ollama pull mistral
   ```

### macOS

1. **Install via Homebrew**
   ```bash
   brew install ollama
   ```

2. **Start Service and Pull Model**
   ```bash
   ollama serve &
   ollama pull mistral
   ```

### Linux

1. **Install Ollama**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Start Service and Pull Model**
   ```bash
   ollama serve &
   ollama pull mistral
   ```

## Configuration

### Environment Variables

Add to your `.env` file:

```env
# Ollama Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

### Verify Installation

Test Ollama is working:

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Test a simple query
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral",
    "prompt": "Hello, how are you?",
    "stream": false
  }'
```

## BusinessThis Integration

### Health Check

The backend provides a health check endpoint:

```bash
curl http://localhost:5000/api/health/ollama
```

Response:
```json
{
  "ollama_status": "healthy",
  "available_models": ["mistral"],
  "current_model": "mistral",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### AI Features

With Ollama running, all AI features work:

- **Financial Coaching**: `/api/ai/coaching`
- **Spending Analysis**: `/api/ai/spending-recommendations`
- **Daily Tips**: `/api/ai/daily-tip`
- **Goal Analysis**: `/api/ai/goal-analysis`
- **Investment Advice**: `/api/ai/investment-advice`

## Performance Optimization

### Model Selection

- **Mistral 7B** (Default): Good balance of speed and quality
- **Llama 3.1 8B**: Better quality, requires more RAM
- **Llama 3.1 70B**: Best quality, requires 40GB+ RAM

### Speed Optimization

1. **Keep Ollama Running**: Don't restart between requests
2. **Use GPU**: If available, Ollama can use GPU acceleration
3. **Model Caching**: Ollama keeps models in memory after first use

### Memory Management

```bash
# Check memory usage
ollama ps

# Stop unused models
ollama stop mistral
```

## Troubleshooting

### Common Issues

1. **"Connection refused" error**
   - Ensure Ollama service is running: `ollama serve`
   - Check if port 11434 is available

2. **Model not found**
   - Pull the model: `ollama pull mistral`
   - List available models: `ollama list`

3. **Out of memory**
   - Reduce model size or upgrade RAM
   - Use smaller model like `mistral:7b-instruct-q4_0`

4. **Slow responses**
   - Check CPU usage during inference
   - Consider GPU acceleration if available

### Logs

Check Ollama logs:

```bash
# Windows
ollama logs

# macOS/Linux
journalctl -u ollama
```

## Production Deployment

### Docker Deployment

```dockerfile
FROM ollama/ollama:latest

# Copy your model
COPY mistral /root/.ollama/models/

# Start Ollama
CMD ["ollama", "serve"]
```

### Systemd Service (Linux)

Create `/etc/systemd/system/ollama.service`:

```ini
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=ollama
Group=ollama
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable ollama
sudo systemctl start ollama
```

## Cost Comparison

### Before (OpenAI API)
- **Cost**: $20-50/month for typical usage
- **Limitations**: Per-query pricing, API rate limits
- **Dependencies**: Internet connection required

### After (Ollama)
- **Cost**: $0/month (only server compute)
- **Benefits**: Unlimited queries, no API limits
- **Privacy**: All data stays on your server

## Monitoring

### Health Monitoring

Set up monitoring for:

1. **Ollama Service**: Check if running on port 11434
2. **Model Availability**: Verify Mistral model is loaded
3. **Response Times**: Monitor AI query performance
4. **Memory Usage**: Track RAM consumption

### Example Monitoring Script

```python
import requests
import time

def check_ollama_health():
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        return response.status_code == 200
    except:
        return False

def monitor_ollama():
    while True:
        if not check_ollama_health():
            print("Ollama is down! Restarting...")
            # Add restart logic here
        time.sleep(60)  # Check every minute
```

## Support

- **Ollama Documentation**: https://ollama.com/docs
- **Model Library**: https://ollama.com/library
- **Community**: https://github.com/ollama/ollama/discussions
