#!/usr/bin/env python3
"""
Local startup script for Solar Calculator
Forces local mode to avoid network issues
"""

import os
import sys

# Set environment variables for local mode
os.environ['FORCE_LOCAL_MODE'] = 'true'
os.environ['FLASK_ENV'] = 'development'

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🌞 Starting Solar Calculator in Local Mode")
print("=" * 50)
print("✅ Network calls disabled")
print("✅ Using mock database")
print("✅ Local development mode")
print("=" * 50)

# Import and run the Flask app
if __name__ == "__main__":
    from solar_app import app
    
    # Run the app
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=False  # Disable reloader to avoid issues
    )
