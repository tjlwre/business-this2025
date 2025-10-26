# BusinessThis Deployment Guide

## 🚀 Quick Start (5 Minutes)

### 1. Environment Setup
```bash
# Copy environment template
cp config/env.example .env

# Edit .env with your API keys
nano .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Database
```bash
python scripts/setup_database.py
```

### 4. Run Application
```bash
# Terminal 1: Backend
python run_backend.py

# Terminal 2: Frontend (Node.js)
node server.js

# Terminal 3: Streamlit (Optional)
streamlit run frontend/streamlit/app.py
```

## 🔧 Detailed Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- Supabase account
- Stripe account (for payments)
- OpenAI account (for AI features)
- SendGrid account (for emails)

### Step 1: Supabase Setup

1. **Create Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Note your project URL and anon key

2. **Setup Database Schema**
   ```bash
   # Run the database setup script
   python scripts/setup_database.py
   ```

3. **Configure Row Level Security (RLS)**
   - Enable RLS on all tables
   - Set up policies for user data isolation

### Step 2: Environment Configuration

Create `.env` file with the following variables:

```env
# Database
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key

# Security
SECRET_KEY=your_secret_key_for_sessions

# Payments
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key

# AI Services
OPENAI_API_KEY=sk-your_openai_api_key

# Email (Optional)
SENDGRID_API_KEY=your_sendgrid_api_key

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8501

# Environment
DEBUG=False
ENVIRONMENT=production
```

### Step 3: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

### Step 4: Database Initialization

```bash
# Setup database tables
python scripts/setup_database.py

# Create admin user
python scripts/create_admin.py

# Seed test data (optional)
python scripts/seed_data.py
```

## 🚀 Production Deployment

### Option 1: Vercel Deployment (Recommended)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

4. **Configure Environment Variables:**
   - Go to Vercel Dashboard > Project Settings > Environment Variables
   - Add all variables from your `.env` file

5. **Add Custom Domain (Optional):**
   ```bash
   vercel domains add yourdomain.com
   ```

### Option 2: Manual Server Deployment

1. **Server Requirements:**
   - Ubuntu 20.04+ or similar
   - Python 3.8+
   - Node.js 18+
   - Nginx (for reverse proxy)

2. **Setup Process:**
   ```bash
   # Clone repository
   git clone <repository-url>
   cd BusinessThis
   
   # Install dependencies
   pip install -r requirements.txt
   npm install
   
   # Setup environment
   cp config/env.example .env
   # Edit .env with production values
   
   # Setup database
   python scripts/setup_database.py
   
   # Configure Nginx
   sudo nano /etc/nginx/sites-available/businessthis
   ```

3. **Nginx Configuration:**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://localhost:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /api/ {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Start Services:**
   ```bash
   # Start backend
   python run_backend.py &
   
   # Start frontend
   node server.js &
   
   # Enable and start Nginx
   sudo systemctl enable nginx
   sudo systemctl start nginx
   ```

## 🔍 Testing Deployment

### Health Checks
```bash
# Backend health
curl http://localhost:5000/api/health

# Frontend health
curl http://localhost:3000/

# Ollama health (if enabled)
curl http://localhost:5000/api/health/ollama
```

### Test User Registration
1. Go to your deployed frontend
2. Register a new user
3. Check Supabase dashboard for user creation
4. Test financial profile creation
5. Test safe spending calculator

## 🛠️ Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check SUPABASE_URL and SUPABASE_ANON_KEY
   - Verify database schema is created
   - Check RLS policies

2. **CORS Errors**
   - Update CORS_ORIGINS in environment
   - Check frontend/backend URL configuration

3. **Payment Issues**
   - Verify Stripe keys are correct
   - Check webhook endpoints
   - Test with Stripe test mode first

4. **AI Service Issues**
   - Check OpenAI API key
   - Verify Ollama is running (if using local AI)
   - Check AI service health endpoint

### Logs and Monitoring

```bash
# Backend logs
tail -f logs/backend.log

# Frontend logs
tail -f logs/frontend.log

# System logs
journalctl -u businessthis-backend
journalctl -u businessthis-frontend
```

## 📊 Performance Optimization

### Backend Optimization
- Enable Redis caching
- Use connection pooling
- Implement rate limiting
- Monitor API response times

### Frontend Optimization
- Enable gzip compression
- Use CDN for static assets
- Implement caching headers
- Monitor Core Web Vitals

## 🔒 Security Checklist

- [ ] Environment variables secured
- [ ] Database RLS enabled
- [ ] API rate limiting configured
- [ ] HTTPS enabled
- [ ] Security headers configured
- [ ] Input validation implemented
- [ ] SQL injection prevention
- [ ] XSS protection enabled

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancer
- Implement session storage
- Database connection pooling
- Stateless application design

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement caching layers
- Monitor resource usage

## 🆘 Support

For deployment issues:
- Check logs first
- Verify environment variables
- Test individual components
- Contact support if needed

## 📚 Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Stripe Documentation](https://stripe.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)