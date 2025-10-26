# Vercel LLM Setup Guide

This guide will help you set up Vercel LLM integration for your BusinessThis application.

## Quick Start

### 1. Get Vercel LLM API Key

1. Visit [Vercel Dashboard](https://vercel.com/dashboard)
2. Go to Settings → API Keys
3. Create a new API key with LLM access
4. Copy the API key

### 2. Configure Environment Variables

Add these variables to your `.env` file:

```bash
# Enable Vercel LLM
USE_VERCEL_LLM=true

# Vercel LLM Configuration
VERCEL_LLM_API_KEY=your_api_key_here
VERCEL_LLM_MODEL=gpt-3.5-turbo
VERCEL_LLM_MAX_TOKENS=1000
VERCEL_LLM_TEMPERATURE=0.7
```

### 3. Test the Integration

Run the test script to verify everything works:

```bash
python scripts/test_vercel_llm.py
```

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_VERCEL_LLM` | `false` | Enable Vercel LLM (true/false) |
| `VERCEL_LLM_API_KEY` | None | Your Vercel API key |
| `VERCEL_LLM_MODEL` | `gpt-3.5-turbo` | AI model to use |
| `VERCEL_LLM_MAX_TOKENS` | `1000` | Max response length |
| `VERCEL_LLM_TEMPERATURE` | `0.7` | Response creativity |

## Switching Between AI Providers

### Use Vercel LLM (Cloud-based)
```bash
USE_VERCEL_LLM=true
```

### Use Ollama (Local)
```bash
USE_VERCEL_LLM=false
```

## Troubleshooting

### Common Issues

1. **"API key not configured"**
   - Check that `VERCEL_LLM_API_KEY` is set
   - Verify the API key is valid

2. **"Health check failed"**
   - Check internet connection
   - Verify API key permissions
   - Check Vercel service status

3. **"Rate limit exceeded"**
   - Wait a few minutes before retrying
   - Consider upgrading your Vercel plan

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Cost Management

- Monitor your API usage in the Vercel dashboard
- Set up usage alerts
- Consider caching responses for common queries
- Use appropriate models for different use cases

## Support

- Check the [Vercel LLM Documentation](https://vercel.com/docs/ai)
- Review the integration logs
- Test with the provided test script
