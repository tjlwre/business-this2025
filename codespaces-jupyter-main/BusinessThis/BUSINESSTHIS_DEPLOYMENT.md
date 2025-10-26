# BusinessThis.com Deployment Guide

## 🚀 Deploy to businessthis.com

### Prerequisites
- Vercel account (free)
- Domain: businessthis.com (configured in Vercel)
- Supabase credentials (already provided)
- Stripe credentials (needed for payments)

### Quick Deployment Steps

#### Option 1: Using Deployment Script (Recommended)
```bash
# Run the deployment script
./deploy-to-businessthis.sh
```

#### Option 2: Manual Deployment
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

4. **Add Custom Domain:**
   ```bash
   vercel domains add businessthis.com
   ```

### Environment Variables Setup

In Vercel Dashboard > Project Settings > Environment Variables, add:

```
SUPABASE_URL = https://dywjcpbwjmxiiqjlhtni.supabase.co
SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR5d2pjcGJ3am14aWlxamxodG5pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyNzMwNDIsImV4cCI6MjA3NTg0OTA0Mn0.bz8HkV49th_hArIYGmy16GqQG6Tlm3opJpzTC1iehe0
SUPABASE_SERVICE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR5d2pjcGJ3am14aWlxamxodG5pIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDI3MzA0MiwiZXhwIjoyMDc1ODQ5MDQyfQ.AQQ-YzMg-1IflMGomYubkWzzqIGJA4mpTNOOIVIpxKQ
SECRET_KEY = Nl0XQ0x_fjXedo7k5ndezilkpcNZZ0ZRPP7XFpZ1mdQ
DEBUG = False
ENVIRONMENT = production
API_BASE_URL = https://businessthis.com/api
FRONTEND_URL = https://businessthis.com
```

### Domain Configuration

1. **In Vercel Dashboard:**
   - Go to your project
   - Click "Domains"
   - Add "businessthis.com"
   - Follow DNS configuration instructions

2. **DNS Settings:**
   - Point your domain to Vercel's nameservers
   - Or add CNAME record pointing to your Vercel deployment

### Project Structure for businessthis.com

```
businessthis.com/
├── / (Landing page - server.js)
├── /api/ (Backend API - backend/app.py)
├── /app (Streamlit frontend - deployed separately)
├── /about (About page)
├── /pricing (Pricing page)
└── /contact (Contact page)
```

### Testing Your Deployment

1. **Backend API Test:**
   ```bash
   curl https://businessthis.com/api/health
   ```

2. **Frontend Test:**
   - Visit https://businessthis.com
   - Test user registration
   - Test financial calculations

3. **Database Test:**
   - Check Supabase dashboard for new users
   - Verify data is being saved

### Troubleshooting

#### Common Issues:

1. **Domain not resolving:**
   - Check DNS settings
   - Wait 24-48 hours for DNS propagation
   - Verify domain is added in Vercel

2. **Backend not working:**
   - Check environment variables
   - Verify Supabase connection
   - Check Vercel function logs

3. **Frontend not loading:**
   - Check if server.js is working
   - Verify static file serving
   - Check browser console for errors

### Next Steps After Deployment

1. **Set up Stripe payments**
2. **Configure email notifications**
3. **Set up monitoring and analytics**
4. **Launch marketing campaign**

### Support

If you encounter issues:
1. Check Vercel function logs
2. Check Supabase logs
3. Test API endpoints individually
4. Verify environment variables

## 🎉 Success!

Once deployed, your BusinessThis platform will be live at:
- **Main site**: https://businessthis.com
- **API**: https://businessthis.com/api
- **Admin**: https://businessthis.com/admin (if implemented)
