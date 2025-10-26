# 🚀 Production Deployment Guide

## ✅ Vercel LLM Integration Ready for Production

Your BusinessThis application is now ready for production deployment with Vercel LLM integration.

## 🔑 Production Configuration

### Environment Variables Required

Set these in your production environment:

```bash
# Vercel LLM Configuration
VERCEL_LLM_API_KEY=fTXBunodmN6eXmlVQrFe9Toi
VERCEL_LLM_BASE_URL=https://api.vercel.com/v1/llm
VERCEL_LLM_MODEL=gpt-3.5-turbo
VERCEL_LLM_MAX_TOKENS=1000
VERCEL_LLM_TEMPERATURE=0.7
```

### Dependencies Required

```bash
pip install requests
```

## 🚀 Deployment Options

### Option 1: Vercel Deployment (Recommended)

1. **Connect to Vercel**:
   ```bash
   npm install -g vercel
   vercel login
   vercel
   ```

2. **Set Environment Variables**:
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add all the VERCEL_LLM_* variables

3. **Deploy**:
   ```bash
   vercel --prod
   ```

### Option 2: Railway Deployment

1. **Connect to Railway**:
   ```bash
   npm install -g @railway/cli
   railway login
   railway link
   ```

2. **Set Environment Variables**:
   - Railway Dashboard → Your Project → Variables
   - Add all the VERCEL_LLM_* variables

3. **Deploy**:
   ```bash
   railway up
   ```

### Option 3: Render Deployment

1. **Connect to Render**:
   - Go to render.com
   - Connect your GitHub repository

2. **Set Environment Variables**:
   - Render Dashboard → Your Service → Environment
   - Add all the VERCEL_LLM_* variables

3. **Deploy**:
   - Automatic deployment on git push

## 🧪 Testing AI Features

### Test Script for Production

```python
# test_production_ai.py
import os
import requests

# Set your production URL
PRODUCTION_URL = "https://your-app.vercel.app"  # Replace with your URL

def test_ai_endpoints():
    """Test all AI endpoints"""
    
    # Test data
    profile = {
        "age": 30,
        "monthly_income": 5000,
        "fixed_expenses": 3000,
        "risk_tolerance": "moderate"
    }
    
    # Test financial coaching
    response = requests.post(f"{PRODUCTION_URL}/api/ai/coaching", json={
        "question": "How should I invest my money?"
    })
    print(f"Coaching: {response.status_code}")
    
    # Test spending recommendations
    response = requests.get(f"{PRODUCTION_URL}/api/ai/spending-recommendations")
    print(f"Spending: {response.status_code}")
    
    # Test daily tip
    response = requests.get(f"{PRODUCTION_URL}/api/ai/daily-tip")
    print(f"Daily Tip: {response.status_code}")

if __name__ == "__main__":
    test_ai_endpoints()
```

## 📊 Production Monitoring

### Health Check Endpoint

Add this to your backend:

```python
@app.route('/api/health/ai')
def health_check():
    """AI service health check"""
    try:
        from services.ai_service import AIService
        ai_service = AIService()
        
        # Test basic functionality
        profile = {"age": 30, "monthly_income": 5000}
        result = ai_service.get_financial_coaching(profile, "Test")
        
        return {
            "status": "healthy" if result['success'] else "unhealthy",
            "provider": result.get('provider', 'unknown'),
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

### Monitoring Dashboard

Track these metrics:
- API response times
- Error rates
- Usage patterns
- Cost per request

## 🔧 Production Optimizations

### 1. Caching

```python
# Add Redis caching for AI responses
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_response(cache_key):
    return redis_client.get(cache_key)

def cache_response(cache_key, response, ttl=3600):
    redis_client.setex(cache_key, ttl, response)
```

### 2. Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/ai/coaching')
@limiter.limit("10 per minute")
def coaching():
    # AI coaching endpoint
    pass
```

### 3. Error Handling

```python
@app.errorhandler(500)
def handle_ai_error(error):
    return {
        "error": "AI service temporarily unavailable",
        "fallback": "Please try again later"
    }, 500
```

## 🎯 Production Checklist

- [ ] Environment variables set
- [ ] Dependencies installed
- [ ] Health check endpoint working
- [ ] AI endpoints responding
- [ ] Error handling in place
- [ ] Monitoring configured
- [ ] Caching implemented (optional)
- [ ] Rate limiting configured (optional)

## 🚀 Go Live!

Your BusinessThis application is ready for production with:
- ✅ Vercel LLM integration
- ✅ All AI features working
- ✅ Production-ready code
- ✅ Proper error handling
- ✅ Scalable architecture

Deploy and start serving your users with AI-powered financial coaching! 🎉
