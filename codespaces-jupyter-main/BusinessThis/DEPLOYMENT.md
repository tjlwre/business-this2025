# BusinessThis Deployment Guide

This guide covers deploying BusinessThis to production environments.

## Prerequisites

### Required Accounts
- **Supabase**: Database and authentication
- **Stripe**: Payment processing
- **OpenAI**: AI features
- **SendGrid**: Email services
- **Domain**: Custom domain (optional)

### Required Credentials
- Supabase project URL and keys
- Stripe API keys
- OpenAI API key
- SendGrid API key
- Custom domain (if using)

## Deployment Options

### Option 1: Railway (Recommended for Backend)

Railway provides easy deployment with automatic scaling and database integration.

#### Backend Deployment to Railway

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy Backend**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login to Railway
   railway login
   
   # Initialize project
   railway init
   
   # Set environment variables
   railway variables set SUPABASE_URL=your_supabase_url
   railway variables set SUPABASE_ANON_KEY=your_supabase_anon_key
   railway variables set SUPABASE_SERVICE_KEY=your_supabase_service_key
   railway variables set STRIPE_SECRET_KEY=your_stripe_secret_key
   railway variables set STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
   railway variables set OPENAI_API_KEY=your_openai_key
   railway variables set SECRET_KEY=your_secret_key
   
   # Deploy
   railway up
   ```

3. **Configure Domain**
   - In Railway dashboard, go to Settings
   - Add custom domain
   - Update CORS settings in backend

### Option 2: Render (Alternative for Backend)

#### Backend Deployment to Render

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Deploy Backend**
   - Connect GitHub repository
   - Select "Web Service"
   - Configure:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python run_backend.py`
     - Environment: Python 3

3. **Set Environment Variables**
   - Go to Environment tab
   - Add all required variables

### Option 3: Heroku (Legacy)

#### Backend Deployment to Heroku

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Windows
   # Download from heroku.com
   ```

2. **Deploy to Heroku**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create app
   heroku create businessthis-backend
   
   # Set environment variables
   heroku config:set SUPABASE_URL=your_supabase_url
   heroku config:set SUPABASE_ANON_KEY=your_supabase_anon_key
   # ... add all other variables
   
   # Deploy
   git push heroku main
   ```

## Frontend Deployment

### Option 1: Streamlit Cloud (Recommended)

1. **Prepare Repository**
   - Push code to GitHub
   - Ensure requirements.txt is in root

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect GitHub
   - Select repository
   - Configure:
     - Main file: `frontend/app.py`
     - Python version: 3.8+

3. **Update API URL**
   - In `frontend/app.py`, update `API_BASE_URL`
   - Set to your deployed backend URL

### Option 2: Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy Frontend**
   ```bash
   # Create vercel.json
   {
     "builds": [
       {
         "src": "frontend/app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "frontend/app.py"
       }
     ]
   }
   
   # Deploy
   vercel --prod
   ```

### Option 3: Netlify

1. **Create netlify.toml**
   ```toml
   [build]
   command = "pip install -r requirements.txt && streamlit run frontend/app.py"
   publish = "frontend/"
   
   [[redirects]]
   from = "/*"
   to = "/frontend/app.py"
   status = 200
   ```

2. **Deploy**
   - Connect GitHub repository
   - Configure build settings
   - Deploy

## Database Setup

### Supabase Configuration

1. **Create Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Note project URL and API keys

2. **Run Database Schema**
   - Go to SQL Editor in Supabase dashboard
   - Copy contents of `database/schema.sql`
   - Run the SQL script

3. **Configure Authentication**
   - Go to Authentication > Settings
   - Enable email authentication
   - Configure email templates

4. **Set up Row Level Security**
   - The schema includes RLS policies
   - Verify they're active in Supabase dashboard

## Payment Integration

### Stripe Setup

1. **Create Stripe Account**
   - Go to [stripe.com](https://stripe.com)
   - Complete account setup
   - Get API keys from dashboard

2. **Create Products and Prices**
   ```bash
   # Using Stripe CLI
   stripe products create --name "BusinessThis Premium" --description "Premium subscription"
   stripe prices create --product prod_xxx --unit-amount 999 --currency usd --recurring interval=month
   stripe products create --name "BusinessThis Pro" --description "Pro subscription"
   stripe prices create --product prod_yyy --unit-amount 1999 --currency usd --recurring interval=month
   ```

3. **Configure Webhooks**
   - Go to Stripe Dashboard > Webhooks
   - Add endpoint: `https://your-backend-url.com/api/webhooks/stripe`
   - Select events: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`

4. **Update Environment Variables**
   - Add Stripe price IDs to environment variables
   - Set webhook secret

## Email Setup

### SendGrid Configuration

1. **Create SendGrid Account**
   - Go to [sendgrid.com](https://sendgrid.com)
   - Complete account verification
   - Get API key

2. **Configure Sender**
   - Go to Settings > Sender Authentication
   - Verify domain or single sender
   - Update FROM_EMAIL in environment variables

3. **Create Email Templates**
   - Welcome email
   - Password reset
   - Subscription confirmation
   - Financial tips

## Domain and SSL

### Custom Domain Setup

1. **Purchase Domain**
   - Use any domain registrar
   - Point DNS to your hosting provider

2. **Configure SSL**
   - Most hosting providers offer free SSL
   - Enable HTTPS redirect
   - Update CORS settings

3. **Update Application URLs**
   - Update frontend API_BASE_URL
   - Update Stripe success/cancel URLs
   - Update email templates

## Monitoring and Analytics

### Application Monitoring

1. **Error Tracking**
   - Set up Sentry (free tier available)
   - Add to requirements.txt
   - Configure in backend

2. **Performance Monitoring**
   - Use hosting provider metrics
   - Set up uptime monitoring
   - Monitor database performance

3. **Analytics**
   - Google Analytics for frontend
   - Custom analytics for user behavior
   - Financial metrics tracking

## Security Considerations

### Production Security

1. **Environment Variables**
   - Never commit .env files
   - Use secure secret management
   - Rotate keys regularly

2. **Database Security**
   - Enable RLS in Supabase
   - Use connection pooling
   - Monitor database access

3. **API Security**
   - Rate limiting
   - Input validation
   - CORS configuration
   - JWT token expiration

4. **Payment Security**
   - PCI compliance via Stripe
   - Secure webhook handling
   - Fraud detection

## Scaling Considerations

### Performance Optimization

1. **Database Optimization**
   - Add database indexes
   - Use connection pooling
   - Monitor query performance

2. **Caching**
   - Redis for session storage
   - CDN for static assets
   - API response caching

3. **Load Balancing**
   - Multiple backend instances
   - Database read replicas
   - CDN for global distribution

## Backup and Recovery

### Data Backup

1. **Database Backups**
   - Supabase automatic backups
   - Manual backup scripts
   - Point-in-time recovery

2. **Application Backups**
   - Code repository backups
   - Environment variable backups
   - Configuration backups

3. **Disaster Recovery**
   - Multi-region deployment
   - Database replication
   - Automated failover

## Maintenance

### Regular Maintenance

1. **Security Updates**
   - Update dependencies monthly
   - Monitor security advisories
   - Apply patches promptly

2. **Performance Monitoring**
   - Monitor response times
   - Track error rates
   - Optimize slow queries

3. **User Support**
   - Monitor support tickets
   - Update documentation
   - Gather user feedback

## Troubleshooting

### Common Issues

1. **Backend Won't Start**
   - Check environment variables
   - Verify database connection
   - Check port availability

2. **Frontend Connection Issues**
   - Verify API_BASE_URL
   - Check CORS settings
   - Test API endpoints

3. **Payment Issues**
   - Verify Stripe keys
   - Check webhook configuration
   - Test payment flow

4. **Database Issues**
   - Check Supabase connection
   - Verify RLS policies
   - Monitor query performance

### Support Resources

- **Documentation**: README.md
- **Issues**: GitHub Issues
- **Community**: Discord/Slack
- **Support**: support@businessthis.com

## Cost Estimation

### Monthly Costs (Estimated)

- **Supabase**: $0-25 (free tier up to 500MB)
- **Railway/Render**: $0-20 (free tier available)
- **Stripe**: 2.9% + $0.30 per transaction
- **OpenAI**: $20-50 (usage-based)
- **SendGrid**: $0-15 (free tier: 100 emails/day)
- **Domain**: $12/year
- **Total**: $50-100/month (scales with usage)

### Scaling Costs

- **1K users**: $100-200/month
- **10K users**: $500-1000/month
- **100K users**: $2000-5000/month

## Next Steps

After successful deployment:

1. **Test All Features**
   - User registration/login
   - Financial calculations
   - Payment processing
   - Email notifications

2. **Monitor Performance**
   - Set up monitoring
   - Track key metrics
   - Optimize bottlenecks

3. **Gather Feedback**
   - Beta user testing
   - Feature requests
   - Bug reports

4. **Scale Gradually**
   - Monitor usage patterns
   - Optimize performance
   - Add features incrementally
