@echo off
echo 🚀 Deploying BusinessThis to businessthis.com

REM Check if vercel CLI is installed
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing Vercel CLI...
    npm install -g vercel
)

REM Login to Vercel (if not already logged in)
echo Checking Vercel authentication...
vercel whoami
if %ERRORLEVEL% NEQ 0 (
    echo Please login to Vercel...
    vercel login
)

REM Deploy to production
echo Deploying to production...
vercel --prod --yes

REM Set custom domain
echo Setting up custom domain: businessthis.com
vercel domains add businessthis.com

echo.
echo Please add these environment variables in Vercel dashboard:
echo SUPABASE_URL=https://dywjcpbwjmxiiqjlhtni.supabase.co
echo SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR5d2pjcGJ3am14aWlxamxodG5pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyNzMwNDIsImV4cCI6MjA3NTg0OTA0Mn0.bz8HkV49th_hArIYGmy16GqQG6Tlm3opJpzTC1iehe0
echo SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR5d2pjcGJ3am14aWlxamxodG5pIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDI3MzA0MiwiZXhwIjoyMDc1ODQ5MDQyfQ.AQQ-YzMg-1IflMGomYubkWzzqIGJA4mpTNOOIVIpxKQ
echo SECRET_KEY=Nl0XQ0x_fjXedo7k5ndezilkpcNZZ0ZRPP7XFpZ1mdQ
echo DEBUG=False
echo ENVIRONMENT=production
echo.
echo ✅ Deployment complete!
echo 🌐 Your app will be available at: https://businessthis.com
pause
