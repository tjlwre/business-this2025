# BusinessThis Deployment Guide

## 🚀 Quick Start (5 Minutes)

### 1. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Database
```bash
python scripts/setup_environment.py
```

### 4. Run Application
```bash
# Terminal 1: Backend
python run_backend.py

# Terminal 2: Frontend  
python run_frontend.py
```

### 5. Test Everything
```bash
python test_implementation.py
```

## 🔧 Detailed Setup

### Prerequisites
- Python 3.8+
- Supabase account
- Stripe account
- OpenAI account
- SendGrid account (optional)

### Step 1: Supabase Setup

1. **Create Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Note your URL and API keys

2. **Run Database Schema**
   ```sql
   -- Copy and paste the contents of database/schema.sql
   -- into your Supabase SQL editor
   ```

3. **Configure Environment**
   ```bash
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your-anon-key
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
   ```

### Step 2: Stripe Setup

1. **Create Stripe Account**
   - Go to [stripe.com](https://stripe.com)
   - Get your API keys from dashboard

2. **Create Products**
   - Create "Premium" product ($9.99/month)
   - Create "Pro" product ($19.99/month)
   - Note the price IDs

3. **Configure Environment**
   ```bash
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_PUBLISHABLE_KEY=pk_test_...
   STRIPE_PREMIUM_PRICE_ID=price_...
   STRIPE_PRO_PRICE_ID=price_...
   ```

### Step 3: OpenAI Setup

1. **Get OpenAI API Key**
   - Go to [platform.openai.com](https://platform.openai.com)
   - Create API key

2. **Configure Environment**
   ```bash
   OPENAI_API_KEY=sk-...
   ```

### Step 4: Optional Integrations

**SendGrid (Email)**
```bash
SENDGRID_API_KEY=SG...
FROM_EMAIL=noreply@yourdomain.com
```

**PayPal (Alternative Payments)**
```bash
PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...
```

**Plaid (Bank Integration)**
```bash
PLAID_CLIENT_ID=...
PLAID_SECRET=...
```

## 🚀 Production Deployment

### Option 1: Railway (Recommended)

1. **Connect GitHub**
   - Push code to GitHub
   - Connect Railway to your repo

2. **Configure Environment**
   - Add all environment variables in Railway dashboard

3. **Deploy**
   - Railway auto-deploys on push
   - Get your production URL

### Option 2: Heroku

1. **Install Heroku CLI**
   ```bash
   # Install Heroku CLI
   heroku login
   ```

2. **Create App**
   ```bash
   heroku create businessthis-app
   ```

3. **Configure Environment**
   ```bash
   heroku config:set SUPABASE_URL=...
   heroku config:set STRIPE_SECRET_KEY=...
   # ... add all other variables
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Option 3: DigitalOcean App Platform

1. **Create App**
   - Go to DigitalOcean App Platform
   - Connect GitHub repo
   - Configure environment variables

2. **Deploy**
   - App Platform handles deployment automatically

## 📊 Monitoring & Analytics

### Health Checks
```bash
# Test API health
curl https://your-app.railway.app/api/health

# Test frontend
curl https://your-app.railway.app
```

### Database Monitoring
- Use Supabase dashboard for database metrics
- Monitor query performance
- Set up alerts for high usage

### Error Tracking
- Consider adding Sentry for error tracking
- Monitor API response times
- Track user engagement

## 🔒 Security Checklist

### Environment Security
- [ ] Never commit .env file
- [ ] Use strong SECRET_KEY
- [ ] Rotate API keys regularly
- [ ] Enable 2FA on all accounts

### Application Security
- [ ] Enable HTTPS in production
- [ ] Configure CORS properly
- [ ] Validate all inputs
- [ ] Use rate limiting
- [ ] Enable RLS policies

### Database Security
- [ ] Enable RLS on all tables
- [ ] Use service role key only for admin operations
- [ ] Regular backups
- [ ] Monitor access logs

## 🚨 Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check Supabase credentials
python -c "from config.supabase_config import test_supabase_connection; print(test_supabase_connection())"
```

**Stripe Webhook Issues**
```bash
# Test webhook endpoint
curl -X POST https://your-app.railway.app/api/stripe/webhook \
  -H "Content-Type: application/json" \
  -d '{"type": "test"}'
```

**Frontend Not Loading**
```bash
# Check if backend is running
curl http://localhost:5000/api/health

# Check frontend
curl http://localhost:8501
```

### Performance Issues

**Slow API Responses**
- Check database query performance
- Enable Redis caching
- Optimize database indexes

**Frontend Loading Issues**
- Check network requests in browser dev tools
- Verify API endpoints are accessible
- Check for CORS issues

## 📈 Scaling Considerations

### Database Scaling
- Monitor Supabase usage
- Consider upgrading plan if needed
- Implement database connection pooling

### API Scaling
- Use load balancer for multiple instances
- Implement caching layer
- Monitor response times

### Frontend Scaling
- Use CDN for static assets
- Implement caching strategies
- Monitor user experience metrics

## 🎯 Go-Live Checklist

### Pre-Launch
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database schema deployed
- [ ] SSL certificates installed
- [ ] Domain configured
- [ ] Analytics tracking setup

### Post-Launch
- [ ] Monitor error rates
- [ ] Track user registrations
- [ ] Monitor payment processing
- [ ] Check email delivery
- [ ] Monitor performance metrics

## 📞 Support

### Getting Help
- Check logs for error messages
- Use test suite to identify issues
- Review API documentation
- Check Supabase dashboard for database issues

### Common Solutions
- Restart services if stuck
- Check environment variables
- Verify API keys are correct
- Ensure database is accessible

---

**🎉 Congratulations! Your BusinessThis application is ready for production!**

For additional support, refer to the individual service documentation or contact the development team.
