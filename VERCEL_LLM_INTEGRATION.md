# Vercel LLM Integration for BusinessThis

This document explains how to integrate and use Vercel's LLM API with the BusinessThis financial planning platform.

## Overview

The Vercel LLM integration provides an alternative AI backend to the existing Ollama integration, offering cloud-based AI capabilities for financial coaching, spending analysis, and investment advice.

## Features

- **Financial Coaching**: Personalized financial advice based on user profiles
- **Spending Analysis**: AI-powered analysis of spending patterns and recommendations
- **Daily Tips**: Personalized daily financial tips
- **Goal Analysis**: Analysis and recommendations for financial goals
- **Investment Advice**: Portfolio analysis and investment recommendations

## Setup

### 1. Environment Configuration

Add the following environment variables to your `.env` file:

```bash
# Vercel LLM Configuration
VERCEL_LLM_API_KEY=your_vercel_llm_api_key
VERCEL_LLM_BASE_URL=https://api.vercel.com/v1/llm
VERCEL_LLM_MODEL=gpt-3.5-turbo
VERCEL_LLM_MAX_TOKENS=1000
VERCEL_LLM_TEMPERATURE=0.7
USE_VERCEL_LLM=true  # Set to 'true' to use Vercel LLM instead of Ollama
```

### 2. API Key Setup

1. Sign up for a Vercel account at [vercel.com](https://vercel.com)
2. Navigate to your account settings
3. Generate an API key for LLM access
4. Add the API key to your environment variables

### 3. Installation

The integration uses the existing `requests` library for HTTP calls. No additional Python packages are required beyond what's already in `requirements/integrations.txt`.

## Usage

### Basic Usage

The AI service automatically detects the `USE_VERCEL_LLM` environment variable and switches between Ollama and Vercel LLM accordingly.

```python
from services.ai_service import AIService

# Initialize AI service (automatically uses Vercel LLM if configured)
ai_service = AIService()

# Get financial coaching
profile = {"age": 30, "monthly_income": 5000, "risk_tolerance": "moderate"}
advice = ai_service.get_financial_coaching(profile, "How should I invest my money?")
```

### API Endpoints

The integration works through the existing AI routes:

- `POST /api/ai/coaching` - Get personalized financial coaching
- `GET /api/ai/spending-recommendations` - Analyze spending patterns
- `GET /api/ai/daily-tip` - Get daily financial tips
- `GET /api/ai/goal-analysis` - Analyze financial goals
- `POST /api/ai/investment-advice` - Get investment recommendations

### Configuration Options

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `VERCEL_LLM_API_KEY` | None | Your Vercel LLM API key |
| `VERCEL_LLM_BASE_URL` | `https://api.vercel.com/v1/llm` | Vercel LLM API base URL |
| `VERCEL_LLM_MODEL` | `gpt-3.5-turbo` | Model to use for AI requests |
| `VERCEL_LLM_MAX_TOKENS` | `1000` | Maximum tokens per response |
| `VERCEL_LLM_TEMPERATURE` | `0.7` | Response creativity (0.0-1.0) |
| `USE_VERCEL_LLM` | `false` | Enable Vercel LLM (true/false) |

## Fallback Mechanism

The integration includes robust fallback mechanisms:

1. **Primary**: Vercel LLM (if `USE_VERCEL_LLM=true` and API key is valid)
2. **Fallback**: Ollama (if Vercel LLM fails or is disabled)
3. **Final Fallback**: Static recommendations (if both AI services fail)

## Error Handling

The integration handles various error scenarios:

- **API Key Missing**: Falls back to Ollama
- **API Rate Limits**: Retries with exponential backoff
- **Network Issues**: Falls back to Ollama
- **Invalid Responses**: Uses fallback recommendations

## Monitoring

### Health Checks

```python
from integrations.vercel_llm_integration import VercelLLMIntegration

vercel_llm = VercelLLMIntegration()
if vercel_llm.health_check():
    print("Vercel LLM is available")
else:
    print("Vercel LLM is not available")
```

### Available Models

```python
models = vercel_llm.get_available_models()
print(f"Available models: {models}")
```

## Performance Considerations

- **Response Time**: Vercel LLM typically responds in 1-3 seconds
- **Rate Limits**: Respects Vercel's API rate limits
- **Caching**: Consider implementing response caching for frequently asked questions
- **Cost**: Monitor API usage to manage costs

## Security

- **API Keys**: Store securely in environment variables
- **Data Privacy**: User data is sent to Vercel's servers for processing
- **Compliance**: Ensure compliance with your data privacy requirements

## Troubleshooting

### Common Issues

1. **"API key not configured"**
   - Check that `VERCEL_LLM_API_KEY` is set correctly
   - Verify the API key is valid

2. **"Unable to generate financial advice"**
   - Check network connectivity
   - Verify API key permissions
   - Check rate limits

3. **Slow responses**
   - Consider reducing `VERCEL_LLM_MAX_TOKENS`
   - Check network latency to Vercel servers

### Debug Mode

Enable debug logging by setting the log level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Migration from Ollama

To migrate from Ollama to Vercel LLM:

1. Set up Vercel LLM API key
2. Set `USE_VERCEL_LLM=true` in environment
3. Test the integration
4. Monitor performance and costs
5. Optionally disable Ollama service

## Cost Optimization

- **Token Usage**: Monitor token consumption per request
- **Caching**: Implement response caching for common queries
- **Model Selection**: Choose appropriate models for different use cases
- **Batch Processing**: Group similar requests when possible

## Support

For issues with the Vercel LLM integration:

1. Check the logs for error messages
2. Verify API key and configuration
3. Test with the health check endpoint
4. Review Vercel's API documentation
5. Contact support if issues persist

## Example Implementation

```python
# Example: Using Vercel LLM for financial coaching
from services.ai_service import AIService

ai_service = AIService()

# User profile
profile = {
    "age": 28,
    "monthly_income": 6000,
    "fixed_expenses": 3000,
    "variable_expenses": 1500,
    "emergency_fund_current": 2000,
    "risk_tolerance": "moderate"
}

# Get coaching advice
result = ai_service.get_financial_coaching(
    profile, 
    "I want to buy a house in 3 years. How should I save?"
)

if result['success']:
    print(f"Advice: {result['advice']}")
    print(f"Provider: {result['provider']}")
else:
    print(f"Error: {result['error']}")
    print(f"Fallback: {result['fallback_advice']}")
```
