"""
Solar Plant Financial Calculator - Flask Web Application
Comprehensive form-based solar calculator with backend storage
"""

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, BooleanField, FileField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional
from dotenv import load_dotenv
import json
from datetime import datetime
import uuid

# Load environment variables
load_dotenv()

# Import our existing utilities
from utils.calculations import SolarCalculator
from utils.location_data import get_cities, get_location_info
from utils.ocr_processor import BillOCRProcessor

# Import backend modules
from backend.solar_data_fetcher import SolarDataFetcher
from backend.report_generator import ReportGenerator

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

CORS(app)

# Initialize services
calculator = SolarCalculator()
ocr_processor = BillOCRProcessor()

# Initialize Supabase client with fallback to mock
# Force mock client for local development to avoid network issues
try:
    # Check if we want to force local mode
    FORCE_LOCAL_MODE = os.getenv('FORCE_LOCAL_MODE', 'true').lower() == 'true'

    if FORCE_LOCAL_MODE:
        raise ValueError("Forcing local mode for development")

    from backend.supabase_client import SupabaseClient
    supabase_client = SupabaseClient()
    SUPABASE_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Supabase client not available: {e}")
    print("🔧 Using Mock Client for local development")
    from backend.mock_supabase_client import MockSupabaseClient
    supabase_client = MockSupabaseClient()
    SUPABASE_AVAILABLE = False

solar_data_fetcher = SolarDataFetcher()
report_generator = ReportGenerator()

# Print initialization status
print("🌞 Solar Plant Financial Calculator - Full Version")
print("=" * 60)
if SUPABASE_AVAILABLE:
    print("✅ Supabase: Connected (Real database)")
    print("✅ PDF Reports: Enabled")
    print("✅ Data Storage: Enabled")
else:
    print("⚠️  Supabase: Using Mock Client (Demo mode)")
    print("⚠️  PDF Reports: Limited functionality")
    print("💡 To enable full features, configure Supabase in .env")
print("=" * 60)

class SolarCalculatorForm(FlaskForm):
    """Comprehensive form for solar calculator inputs"""

    # Basic Information
    location_city = SelectField('Location (City)',
                               choices=[],  # Will be populated dynamically
                               validators=[DataRequired()],
                               render_kw={"class": "form-select"})

    monthly_bill = FloatField('Monthly Electricity Bill (₹)',
                             validators=[DataRequired(), NumberRange(min=100)],
                             render_kw={"class": "form-control", "placeholder": "Enter your monthly bill amount"})

    monthly_consumption = FloatField('Monthly Consumption (kWh)',
                                   validators=[Optional(), NumberRange(min=0)],
                                   render_kw={"class": "form-control", "placeholder": "Optional: Enter if known"})

    # Investment Model
    investment_model = SelectField('Investment Model',
                                 choices=[('CAPEX', 'CAPEX - Purchase System'),
                                         ('OPEX', 'OPEX - Lease/PPA Model')],
                                 validators=[DataRequired()],
                                 render_kw={"class": "form-select"})

    # Consumer Details
    consumer_type = SelectField('Type of Consumer',
                              choices=[('Residential', 'Residential'),
                                     ('Commercial', 'Commercial'),
                                     ('Industrial', 'Industrial')],
                              validators=[DataRequired()],
                              render_kw={"class": "form-select"})

    consumer_category = SelectField('Consumer Category',
                                  choices=[('LT-1', 'LT-1 (Domestic)'),
                                         ('LT-2', 'LT-2 (Non-Domestic)'),
                                         ('LT-3', 'LT-3 (Commercial)'),
                                         ('LT-4', 'LT-4 (Industrial)'),
                                         ('HT-1', 'HT-1 (Industrial)'),
                                         ('HT-2', 'HT-2 (Commercial)')],
                                  validators=[DataRequired()],
                                  render_kw={"class": "form-select"})

    # Installation Details
    installation_type = SelectField('Type of Installation',
                                  choices=[('Rooftop', 'Rooftop'),
                                         ('Ground-mounted', 'Ground-mounted')],
                                  validators=[DataRequired()],
                                  render_kw={"class": "form-select"})

    shadow_analysis = BooleanField('Shadow-free Area Available',
                                 default=True,
                                 render_kw={"class": "form-check-input"})

    rooftop_area = FloatField('Available Rooftop Area (sq ft)',
                            validators=[Optional(), NumberRange(min=0)],
                            render_kw={"class": "form-control", "placeholder": "Optional: Enter available area"})

    # File Upload
    bill_upload = FileField('Upload Electricity Bill (Optional)',
                          render_kw={"class": "form-control", "accept": ".pdf,.png,.jpg,.jpeg"})

@app.route('/')
def index():
    """Main form page"""
    form = SolarCalculatorForm()

    # Populate city choices
    cities = get_cities()
    form.location_city.choices = [(city, city) for city in cities]

    return render_template('index.html', form=form)

@app.route('/calculate', methods=['POST'])
def calculate():
    """Process form submission and calculate solar benefits"""
    form = SolarCalculatorForm()

    # Populate city choices for validation
    cities = get_cities()
    form.location_city.choices = [(city, city) for city in cities]

    if form.validate_on_submit():
        try:
            # Extract form data
            form_data = {
                'location_city': form.location_city.data,
                'monthly_bill': form.monthly_bill.data,
                'monthly_consumption': form.monthly_consumption.data,
                'investment_model': form.investment_model.data,
                'consumer_type': form.consumer_type.data,
                'consumer_category': form.consumer_category.data,
                'installation_type': form.installation_type.data,
                'shadow_analysis': form.shadow_analysis.data,
                'rooftop_area': form.rooftop_area.data
            }

            # Process uploaded file if provided
            ocr_result = None
            if form.bill_upload.data:
                ocr_result = ocr_processor.process_uploaded_file(form.bill_upload.data)
                if ocr_result.get('extracted_amount'):
                    form_data['monthly_bill'] = ocr_result['extracted_amount']
                if ocr_result.get('extracted_units'):
                    form_data['monthly_consumption'] = ocr_result['extracted_units']

            # Fetch enhanced solar data from Global Solar Atlas
            location_info = get_location_info(form_data['location_city'])
            solar_data = solar_data_fetcher.get_enhanced_solar_data(
                form_data['location_city'],
                location_info
            )

            # Perform comprehensive calculations
            results = calculator.get_comprehensive_analysis(
                monthly_bill=form_data['monthly_bill'],
                tariff_rate=solar_data.get('tariff', location_info['tariff']),
                investment_model=form_data['investment_model'],
                solar_irradiance=solar_data.get('irradiance', location_info['irradiance']),
                consumer_type=form_data['consumer_type']
            )

            # Save to database
            calculation_id = supabase_client.save_calculation(form_data, solar_data, results)

            # Prepare results for display
            results_data = {
                'calculation_id': calculation_id,
                'form_data': form_data,
                'solar_data': solar_data,
                'calculations': results['calculations'],
                'recommendations': results.get('recommendations', []),
                'ocr_result': ocr_result
            }

            return render_template('results.html', results=results_data)

        except Exception as e:
            flash(f'Error processing calculation: {str(e)}', 'error')
            return render_template('index.html', form=form)

    else:
        # Form validation failed
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')
        return render_template('index.html', form=form)

@app.route('/download-report/<calculation_id>')
def download_report(calculation_id):
    """Generate and download PDF report"""
    try:
        # Fetch calculation data from database
        calculation_data = supabase_client.get_calculation(calculation_id)

        if not calculation_data:
            flash('Calculation not found', 'error')
            return redirect(url_for('index'))

        # Generate PDF report
        if SUPABASE_AVAILABLE:
            pdf_path = report_generator.generate_pdf_report(calculation_data)
            return send_file(pdf_path, as_attachment=True,
                            download_name=f'solar_report_{calculation_id}.pdf')
        else:
            # Mock PDF generation for demo
            flash('PDF report generated successfully! (Demo mode - actual file not downloaded)', 'success')
            flash('To enable PDF downloads, configure Supabase in .env file', 'info')
            return redirect(url_for('index'))

    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/cities')
def api_cities():
    """API endpoint to get list of cities"""
    cities = get_cities()
    return jsonify(cities)

@app.route('/api/location-info/<city>')
def api_location_info(city):
    """API endpoint to get location information"""
    location_info = get_location_info(city)
    return jsonify(location_info)

@app.route('/demo-info')
def demo_info():
    """Demo information page"""
    return render_template('demo_info.html')

if __name__ == '__main__':
    # Get port from environment variable (for deployment) or default to 5000
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_ENV') != 'production'

    print("\n🌞 Solar Plant Financial Calculator - Full Version")
    print("=" * 60)
    if SUPABASE_AVAILABLE:
        print("✅ Supabase: Connected (Real database)")
        print("✅ PDF Reports: Enabled")
        print("✅ Data Storage: Enabled")
    else:
        print("⚠️  Supabase: Mock Client (Demo mode)")
        print("⚠️  PDF Reports: Limited functionality")
        print("💡 Setup Supabase for full features (see SUPABASE_SETUP.md)")
    print("=" * 60)
    print("\n🚀 Starting Solar Plant Financial Calculator...")
    print(f"📍 Running on: http://localhost:{port}")
    print("🔗 Backend: Supabase Connected" if SUPABASE_AVAILABLE else "🔗 Backend: Demo Mode")
    print("📊 Features: Full functionality with PDF reports")
    print("-" * 60)

    app.run(debug=debug_mode, host='0.0.0.0', port=port)
