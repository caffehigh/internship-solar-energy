"""
Simple test script to verify the Solar Calculator is working correctly
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from utils.calculations import SolarCalculator
        from utils.location_data import get_cities, get_location_info
        from utils.ocr_processor import BillOCRProcessor
        print("✅ All utility modules imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    try:
        from flask import Flask
        from flask_cors import CORS
        from flask_wtf import FlaskForm
        from wtforms import StringField, FloatField, SelectField
        print("✅ All Flask modules imported successfully")
    except ImportError as e:
        print(f"❌ Flask import error: {e}")
        return False
    
    return True

def test_calculations():
    """Test the calculation logic"""
    print("\n🧮 Testing calculation logic...")
    
    try:
        calculator = SolarCalculator()
        
        # Test with sample data
        result = calculator.get_comprehensive_analysis(
            monthly_bill=5000,
            tariff_rate=8.0,
            investment_model="CAPEX",
            solar_irradiance=4.5,
            consumer_type="Residential"
        )
        
        # Verify result structure
        assert 'calculations' in result
        assert 'recommendations' in result
        
        calculations = result['calculations']
        
        # Verify key calculations exist
        required_fields = [
            'monthly_consumption', 'plant_capacity', 'monthly_generation',
            'yearly_generation', 'annual_savings', 'lifetime_savings',
            'investment', 'payback_period', 'annual_co2_saved'
        ]
        
        for field in required_fields:
            assert field in calculations, f"Missing field: {field}"
        
        # Verify calculations are reasonable
        assert calculations['plant_capacity'] > 0, "Plant capacity should be positive"
        assert calculations['annual_savings'] > 0, "Annual savings should be positive"
        assert calculations['payback_period'] > 0, "Payback period should be positive"
        
        print(f"✅ Calculations working correctly")
        print(f"   📊 Plant Capacity: {calculations['plant_capacity']} kWp")
        print(f"   💰 Annual Savings: ₹{calculations['annual_savings']:,.0f}")
        print(f"   ⏱️  Payback Period: {calculations['payback_period']} years")
        
        return True
        
    except Exception as e:
        print(f"❌ Calculation error: {e}")
        return False

def test_location_data():
    """Test location data functionality"""
    print("\n🌍 Testing location data...")
    
    try:
        cities = get_cities()
        assert len(cities) > 0, "No cities found"
        assert 'Delhi' in cities, "Delhi not found in cities"
        
        delhi_info = get_location_info('Delhi')
        assert 'irradiance' in delhi_info, "Irradiance data missing"
        assert 'tariff' in delhi_info, "Tariff data missing"
        assert 'state' in delhi_info, "State data missing"
        
        print(f"✅ Location data working correctly")
        print(f"   🏙️  Total cities: {len(cities)}")
        print(f"   ☀️  Delhi irradiance: {delhi_info['irradiance']} kWh/m²/day")
        print(f"   💡 Delhi tariff: ₹{delhi_info['tariff']}/unit")
        
        return True
        
    except Exception as e:
        print(f"❌ Location data error: {e}")
        return False

def test_form_validation():
    """Test form validation"""
    print("\n📝 Testing form validation...")
    
    try:
        # Import the form class from demo_app
        from demo_app import SolarCalculatorForm
        
        # Create a form instance
        form = SolarCalculatorForm()
        
        # Check if form has required fields
        required_fields = [
            'location_city', 'monthly_bill', 'investment_model',
            'consumer_type', 'consumer_category', 'installation_type'
        ]
        
        for field_name in required_fields:
            assert hasattr(form, field_name), f"Form missing field: {field_name}"
        
        print("✅ Form validation working correctly")
        print(f"   📋 Form has all required fields")
        
        return True
        
    except Exception as e:
        print(f"❌ Form validation error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Solar Calculator Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_calculations,
        test_location_data,
        test_form_validation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Solar Calculator is working correctly.")
        print("\n🌞 You can now run the application:")
        print("   Demo version: python demo_app.py")
        print("   Full version: python solar_app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install flask flask-cors python-dotenv wtforms flask-wtf reportlab")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
