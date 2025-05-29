# 🚀 Solar Plant Financial Calculator - Setup Guide

## Quick Start (Demo Version)

The demo version works immediately without any backend setup:

```bash
# 1. Install dependencies
pip install flask flask-cors python-dotenv wtforms flask-wtf reportlab

# 2. Run demo application
python demo_app.py

# 3. Open browser
# Go to: http://localhost:5000
```

## Full Version Setup (With Supabase Backend)

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up/Login and create a new project
3. Wait for the project to be ready (2-3 minutes)
4. Go to Settings → API
5. Copy your:
   - Project URL
   - Anon public key

### Step 2: Setup Database

1. Go to SQL Editor in your Supabase dashboard
2. Copy the entire content from `backend/database_schema.sql`
3. Paste and run the SQL script
4. This will create all required tables and sample data

### Step 3: Configure Environment

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your Supabase credentials:
   ```env
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-anon-key-here
   FLASK_SECRET_KEY=your-secret-key-here
   ```

### Step 4: Install Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt
```

### Step 5: Run Full Application

```bash
# Run the full application with backend
python solar_app.py
```

## Features Comparison

| Feature | Demo Version | Full Version |
|---------|-------------|--------------|
| Form-based Calculator | ✅ | ✅ |
| Enhanced Calculations | ✅ | ✅ |
| Professional UI | ✅ | ✅ |
| OCR Bill Processing | ✅ | ✅ |
| Results Dashboard | ✅ | ✅ |
| Personalized Recommendations | ✅ | ✅ |
| **Data Storage** | ❌ | ✅ |
| **PDF Reports** | ❌ | ✅ |
| **Calculation History** | ❌ | ✅ |
| **Analytics Dashboard** | ❌ | ✅ |
| **Global Solar Atlas API** | ❌ | ✅ |

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure you're in the correct directory
   cd "c:\Users\lENOVO\Documents\augment-projects\Internship solar"
   
   # Install missing packages
   pip install flask flask-cors python-dotenv wtforms flask-wtf
   ```

2. **Template Errors**
   - Ensure all files in `templates/` directory exist
   - Check that Flask can find the templates folder

3. **Supabase Connection Issues**
   - Verify your `.env` file has correct credentials
   - Check that your Supabase project is active
   - Ensure database schema has been run

4. **OCR Not Working**
   ```bash
   # Install Tesseract OCR
   # Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
   # Add to PATH environment variable
   
   pip install pytesseract pillow
   ```

### Testing the Application

1. **Test Demo Version**:
   - Fill out the form with sample data
   - Use: Monthly Bill = ₹5000, Location = Delhi
   - Check if results page loads correctly

2. **Test Full Version**:
   - Same as demo, plus:
   - Check if data is saved in Supabase
   - Test PDF download functionality

## File Structure

```
solar-plant-calculator/
├── demo_app.py              # Demo version (no backend)
├── solar_app.py             # Full version (with Supabase)
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── results.html
│   └── demo_info.html
├── backend/                # Backend modules
│   ├── database_schema.sql
│   ├── supabase_client.py
│   ├── solar_data_fetcher.py
│   └── report_generator.py
├── utils/                  # Utility modules
│   ├── calculations.py
│   ├── location_data.py
│   └── ocr_processor.py
└── static/                 # Static files
    └── favicon.ico
```

## Next Steps

1. **Customize**: Modify calculations, add more cities, adjust pricing
2. **Deploy**: Deploy to Heroku, Vercel, or other cloud platforms
3. **Enhance**: Add more features like user accounts, advanced analytics
4. **Scale**: Implement caching, optimize database queries

## Support

- Check the main README.md for detailed feature documentation
- Review the code comments for implementation details
- Test with the demo version first before setting up the full version

---

**🌞 Happy Solar Calculating!**
