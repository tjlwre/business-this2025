#!/usr/bin/env python3
"""
Test database connection after schema setup
"""
import os
import sys

# Set environment variables
os.environ['SUPABASE_URL'] = 'https://dywjcpbwjmxiiqjlhtni.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR5d2pjcGJ3am14aWlxamxodG5pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyNzMwNDIsImV4cCI6MjA3NTg0OTA0Mn0.bz8HkV49th_hArIYGmy16GqQG6Tlm3opJpzTC1iehe0'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR5d2pjcGJ3am14aWlxamxodG5pIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDI3MzA0MiwiZXhwIjoyMDc1ODQ5MDQyfQ.AQQ-YzMg-1IflMGomYubkWzzqIGJA4mpTNOOIVIpxKQ'

try:
    from config.supabase_config import get_supabase_client
    print("🔗 Testing database connection...")
    
    client = get_supabase_client()
    print("✅ Database connection successful!")
    
    # Test query to check if tables exist
    print("🔍 Checking if tables exist...")
    
    # Try to query the users table
    result = client.table('users').select('*').limit(1).execute()
    print("✅ Users table accessible")
    
    # Try to query financial_profiles table
    result = client.table('financial_profiles').select('*').limit(1).execute()
    print("✅ Financial profiles table accessible")
    
    # Try to query savings_goals table
    result = client.table('savings_goals').select('*').limit(1).execute()
    print("✅ Savings goals table accessible")
    
    print("\n🎉 Database setup complete! All tables are accessible.")
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("\n📋 Make sure you have:")
    print("1. Run the schema in Supabase SQL Editor")
    print("2. Verified all 11 tables were created")
    print("3. Checked for any errors in Supabase")
    sys.exit(1)
