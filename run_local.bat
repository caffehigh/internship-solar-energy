@echo off
echo 🌞 Starting Solar Calculator in Local Mode
echo ================================================
echo ✅ Network calls disabled
echo ✅ Using mock database
echo ✅ Local development mode
echo ================================================

set FORCE_LOCAL_MODE=true
set FLASK_ENV=development

python solar_app.py
