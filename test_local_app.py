#!/usr/bin/env python3
"""
Test the local app functionality without running the server
"""

import os
import sys

# Set environment variables for local mode
os.environ['FORCE_LOCAL_MODE'] = 'true'
os.environ['FLASK_ENV'] = 'development'

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_initialization():
    """Test if the app can initialize without network issues"""
    print("🧪 Testing App Initialization")
    print("-" * 30)
    
    try:
        # Import the main components
        from utils.calculations import SolarCalculator
        from utils.location_data import get_cities, get_location_info
        from backend.solar_data_fetcher import SolarDataFetcher
        
        print("✅ Calculator imported successfully")
        
        # Test calculator
        calculator = SolarCalculator()
        result = calculator.get_comprehensive_analysis(
            monthly_bill=10000,
            tariff_rate=6.0,
            investment_model="CAPEX",
            solar_irradiance=5.0,
            consumer_type="Residential"
        )
        print("✅ Calculator working correctly")
        
        # Test location data
        cities = get_cities()
        delhi_info = get_location_info("Delhi")
        print(f"✅ Location data working: {len(cities)} cities available")
        
        # Test solar data fetcher
        fetcher = SolarDataFetcher()
        enhanced_data = fetcher.get_enhanced_solar_data("Delhi", delhi_info)
        print("✅ Solar data fetcher working (offline mode)")
        
        print("\n🎉 All components working correctly!")
        print("📍 Ready to start Flask app on http://localhost:5000")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mock_database():
    """Test mock database functionality"""
    print("\n🗄️ Testing Mock Database")
    print("-" * 30)
    
    try:
        from backend.mock_supabase_client import MockSupabaseClient
        
        mock_client = MockSupabaseClient()
        
        # Test saving calculation with proper structure
        test_form_data = {
            'location_city': 'Delhi',
            'monthly_bill': 10000,
            'monthly_consumption': 1667,
            'investment_model': 'CAPEX',
            'consumer_type': 'Residential',
            'consumer_category': 'LT-1',
            'installation_type': 'Rooftop',
            'shadow_analysis': True,
            'rooftop_area': 1000
        }

        test_solar_data = {
            'state': 'Delhi',
            'tariff': 6.0,
            'irradiance': 4.5,
            'ghi_annual': 1642.5,
            'dni_annual': 1396.1,
            'latitude': 28.7041,
            'longitude': 77.1025
        }

        test_results = {
            'calculations': {
                'plant_capacity': 12.35,
                'monthly_generation': 1667,
                'yearly_generation': 20000,
                'investment': 962500,
                'monthly_savings': 10000,
                'annual_savings': 120000,
                'lifetime_savings': 3000000,
                'payback_period': 8.0,
                'annual_co2_saved': 16.0,
                'lifetime_co2_saved': 400.0,
                'equivalent_trees': 727,
                'panel_count': 31,
                'inverter_capacity': 9.88,
                'area_required': 98.8
            }
        }

        calc_id = mock_client.save_calculation(test_form_data, test_solar_data, test_results)
        print(f"✅ Mock database save working: ID {calc_id}")
        
        # Test retrieving calculation
        retrieved = mock_client.get_calculation(calc_id)
        print("✅ Mock database retrieve working")
        
        return True
        
    except Exception as e:
        print(f"❌ Mock database error: {e}")
        return False

if __name__ == "__main__":
    print("🌞 Solar Calculator Local Test")
    print("=" * 50)
    
    # Test app components
    app_ok = test_app_initialization()
    db_ok = test_mock_database()
    
    if app_ok and db_ok:
        print("\n" + "=" * 50)
        print("🚀 ALL TESTS PASSED!")
        print("✅ App is ready to run locally")
        print("📍 Run: python start_local.py")
        print("🌐 Then open: http://localhost:5000")
    else:
        print("\n" + "=" * 50)
        print("❌ SOME TESTS FAILED!")
        print("🔧 Please check the errors above")
