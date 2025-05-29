# 🚀 Supabase Backend Setup Guide

## Step 1: Create Supabase Project

1. **Go to Supabase**: Visit [supabase.com](https://supabase.com)
2. **Sign Up/Login**: Create account or login
3. **New Project**: Click "New Project"
4. **Project Details**:
   - Organization: Select or create
   - Name: `solar-calculator`
   - Database Password: Create strong password
   - Region: Choose closest to your location
5. **Create Project**: Wait 2-3 minutes for setup

## Step 2: Get Project Credentials

1. **Go to Settings**: Click Settings → API
2. **Copy These Values**:
   ```
   Project URL: https://your-project-id.supabase.co
   Anon Public Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

## Step 3: Setup Database Schema

1. **Go to SQL Editor**: In Supabase dashboard
2. **Copy & Run**: Copy entire content from `backend/database_schema.sql`
3. **Execute**: Click "Run" to create all tables

## Step 4: Configure Environment

1. **Update .env file**:
   ```env
   # Replace with your actual Supabase credentials
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-anon-key-here
   FLASK_SECRET_KEY=your-secret-key-here
   ```

## Step 5: Test Connection

Run the full application:
```bash
python solar_app.py
```

## Verification Checklist

- [ ] Supabase project created
- [ ] Database schema executed successfully
- [ ] Environment variables configured
- [ ] Application connects to database
- [ ] Calculations are saved to database
- [ ] PDF reports generate successfully

## Next Steps

Once connected, you'll have:
- ✅ Data persistence
- ✅ PDF report downloads
- ✅ Calculation history
- ✅ Analytics dashboard
- ✅ Enhanced solar data
