#!/bin/bash

# BusinessThis Deployment Script for businessthis.com
echo "🚀 Deploying BusinessThis to businessthis.com"

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "Installing Vercel CLI..."
    npm install -g vercel
fi

# Login to Vercel (if not already logged in)
echo "Checking Vercel authentication..."
vercel whoami || vercel login

# Deploy to production
echo "Deploying to production..."
vercel --prod --yes

# Set custom domain
echo "Setting up custom domain: businessthis.com"
vercel domains add businessthis.com

# Configure environment variables
echo "Please add these environment variables in Vercel dashboard:"
echo "SUPABASE_URL=https://dywjcpbwjmxiiqjlhtni.supabase.co"
echo "SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR5d2pjcGJ3am14aWlxamxodG5pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyNzMwNDIsImV4cCI6MjA3NTg0OTA0Mn0.bz8HkV49th_hArIYGmy16GqQG6Tlm3opJpzTC1iehe0"
echo "SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR5d2pjcGJ3am14aWlxamxodG5pIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDI3MzA0MiwiZXhwIjoyMDc1ODQ5MDQyfQ.AQQ-YzMg-1IflMGomYubkWzzqIGJA4mpTNOOIVIpxKQ"
echo "SECRET_KEY=Nl0XQ0x_fjXedo7k5ndezilkpcNZZ0ZRPP7XFpZ1mdQ"
echo "DEBUG=False"
echo "ENVIRONMENT=production"

echo "✅ Deployment complete!"
echo "🌐 Your app will be available at: https://businessthis.com"
