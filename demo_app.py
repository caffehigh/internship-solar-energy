"""
Solar Plant Financial Calculator - Demo Flask Application
Simplified version that works without Supabase for demonstration
"""

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, NumberRange, Optional
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

# Import our existing utilities
from utils.calculations import SolarCalculator
from utils.location_data import get_cities, get_location_info
from utils.ocr_processor import BillOCRProcessor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'demo-secret-key-change-this')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

CORS(app)

# Initialize services
calculator = SolarCalculator()
ocr_processor = BillOCRProcessor()

class SolarCalculatorForm(FlaskForm):
    """Comprehensive form for solar calculator inputs"""
    
    # Basic Information
    location_city = SelectField('Location (City)', 
                               choices=[],  # Will be populated dynamically
                               validators=[DataRequired()],
                               render_kw={"class": "form-select"})
    
    monthly_bill = FloatField('Monthly Electricity Bill (₹)', 
                             validators=[DataRequired(), NumberRange(min=100, max=2500000)],
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
            
            # Get location info and solar data
            location_info = get_location_info(form_data['location_city'])
            solar_data = {
                'irradiance': location_info['irradiance'],
                'tariff': location_info['tariff'],
                'state': location_info['state'],
                'data_source': 'local_database'
            }
            
            # Perform comprehensive calculations
            results = calculator.get_comprehensive_analysis(
                monthly_bill=form_data['monthly_bill'],
                tariff_rate=solar_data['tariff'],
                investment_model=form_data['investment_model'],
                solar_irradiance=solar_data['irradiance'],
                consumer_type=form_data['consumer_type']
            )
            
            # Generate a demo calculation ID
            calculation_id = str(uuid.uuid4())[:8]
            
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
    """Generate and download PDF report (Demo)"""
    flash('PDF report generation is available in the full version with Supabase backend.', 'info')
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
    print("🌞 Solar Plant Financial Calculator - Demo Version")
    print("📍 Running on: http://localhost:5000")
    print("📊 Features: Form-based calculator with enhanced calculations")
    print("🔧 Note: This is a demo version. Full version includes Supabase backend and PDF reports.")
    print("-" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
