"""
Mock Supabase client for testing without actual Supabase credentials
This allows the full app to run and demonstrate all features
"""

import os
import uuid
import json
from datetime import datetime
from typing import Dict, Any, Optional

class MockSupabaseClient:
    """Mock Supabase client that simulates database operations"""
    
    def __init__(self):
        """Initialize mock client"""
        self.mock_data = {
            'calculations': {},
            'location_data': {},
            'analytics': {
                'total_calculations': 0,
                'capex_calculations': 0,
                'opex_calculations': 0,
                'average_system_size': 0,
                'top_cities': []
            }
        }
        print("🔧 Using Mock Supabase Client (for demo purposes)")
        print("💡 To use real Supabase, update .env with your credentials")
    
    def save_calculation(self, form_data: Dict[str, Any], solar_data: Dict[str, Any], 
                        results: Dict[str, Any]) -> str:
        """
        Mock save calculation data
        
        Args:
            form_data: Form input data
            solar_data: Solar irradiance and location data
            results: Calculation results
            
        Returns:
            str: Calculation ID
        """
        try:
            calculation_id = str(uuid.uuid4())
            calculations = results['calculations']
            
            # Prepare mock data
            mock_record = {
                'id': calculation_id,
                'created_at': datetime.utcnow().isoformat(),
                
                # User Input Data
                'location_city': form_data['location_city'],
                'location_state': solar_data.get('state', ''),
                'monthly_bill': float(form_data['monthly_bill']),
                'monthly_consumption': float(form_data.get('monthly_consumption') or 0),
                'investment_model': form_data['investment_model'],
                'consumer_type': form_data['consumer_type'],
                'consumer_category': form_data['consumer_category'],
                'installation_type': form_data['installation_type'],
                'shadow_free_area': form_data['shadow_analysis'],
                'rooftop_area': float(form_data.get('rooftop_area') or 0),
                'tariff_rate': float(solar_data.get('tariff', 6.0)),
                
                # Solar Data
                'solar_irradiance': float(solar_data.get('irradiance', 4.5)),
                'ghi_annual': float(solar_data.get('ghi_annual', 0)),
                'dni_annual': float(solar_data.get('dni_annual', 0)),
                'latitude': float(solar_data.get('latitude', 0)),
                'longitude': float(solar_data.get('longitude', 0)),
                
                # Calculated Results
                'plant_capacity': float(calculations['plant_capacity']),
                'monthly_generation': float(calculations['monthly_generation']),
                'yearly_generation': float(calculations['yearly_generation']),
                'investment_amount': float(calculations.get('investment', 0)),
                'monthly_savings': float(calculations['monthly_savings']),
                'annual_savings': float(calculations['annual_savings']),
                'lifetime_savings': float(calculations['lifetime_savings']),
                'payback_period': float(calculations.get('payback_period', 0)),
                'co2_saved_annual': float(calculations['annual_co2_saved']),
                'co2_saved_lifetime': float(calculations['lifetime_co2_saved']),
                'equivalent_trees': float(calculations['equivalent_trees']),
                
                # System Specifications
                'panel_count': int(calculations.get('panel_count', 0)),
                'inverter_capacity': float(calculations.get('inverter_capacity', 0)),
                'estimated_area_required': float(calculations.get('area_required', 0)),
            }
            
            # Store in mock database
            self.mock_data['calculations'][calculation_id] = mock_record
            
            # Update analytics
            self._update_analytics(mock_record)
            
            print(f"✅ Mock: Saved calculation {calculation_id[:8]}...")
            return calculation_id
                
        except Exception as e:
            print(f"❌ Mock: Error saving calculation: {str(e)}")
            raise e
    
    def get_calculation(self, calculation_id: str) -> Optional[Dict[str, Any]]:
        """
        Mock retrieve calculation data by ID
        
        Args:
            calculation_id: Calculation ID
            
        Returns:
            Dict containing calculation data or None if not found
        """
        try:
            if calculation_id in self.mock_data['calculations']:
                print(f"✅ Mock: Retrieved calculation {calculation_id[:8]}...")
                return self.mock_data['calculations'][calculation_id]
            else:
                print(f"❌ Mock: Calculation {calculation_id[:8]}... not found")
                return None
                
        except Exception as e:
            print(f"❌ Mock: Error retrieving calculation: {str(e)}")
            return None
    
    def get_recent_calculations(self, limit: int = 10) -> list:
        """
        Mock get recent calculations
        
        Args:
            limit: Number of records to retrieve
            
        Returns:
            List of recent calculations
        """
        try:
            calculations = list(self.mock_data['calculations'].values())
            # Sort by created_at descending
            calculations.sort(key=lambda x: x['created_at'], reverse=True)
            result = calculations[:limit]
            print(f"✅ Mock: Retrieved {len(result)} recent calculations")
            return result
            
        except Exception as e:
            print(f"❌ Mock: Error retrieving recent calculations: {str(e)}")
            return []
    
    def save_location_data(self, city: str, state: str, solar_data: Dict[str, Any]) -> bool:
        """
        Mock save location data
        
        Args:
            city: City name
            state: State name
            solar_data: Solar irradiance and location data
            
        Returns:
            bool: Success status
        """
        try:
            location_key = f"{city}_{state}"
            self.mock_data['location_data'][location_key] = {
                'city': city,
                'state': state,
                'country': 'India',
                'latitude': float(solar_data.get('latitude', 0)),
                'longitude': float(solar_data.get('longitude', 0)),
                'ghi_annual': float(solar_data.get('ghi_annual', 0)),
                'dni_annual': float(solar_data.get('dni_annual', 0)),
                'avg_irradiance': float(solar_data.get('irradiance', 4.5)),
                'default_tariff': float(solar_data.get('tariff', 6.0)),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            print(f"✅ Mock: Saved location data for {city}, {state}")
            return True
            
        except Exception as e:
            print(f"❌ Mock: Error saving location data: {str(e)}")
            return False
    
    def get_analytics_data(self) -> Dict[str, Any]:
        """
        Mock get analytics data
        
        Returns:
            Dict containing analytics information
        """
        try:
            analytics = self.mock_data['analytics'].copy()
            print(f"✅ Mock: Retrieved analytics data")
            return analytics
            
        except Exception as e:
            print(f"❌ Mock: Error getting analytics data: {str(e)}")
            return {
                'total_calculations': 0,
                'capex_calculations': 0,
                'opex_calculations': 0,
                'average_system_size': 0,
                'top_cities': []
            }
    
    def _update_analytics(self, calculation: Dict[str, Any]):
        """Update mock analytics data"""
        analytics = self.mock_data['analytics']
        
        # Update totals
        analytics['total_calculations'] += 1
        
        if calculation['investment_model'] == 'CAPEX':
            analytics['capex_calculations'] += 1
        else:
            analytics['opex_calculations'] += 1
        
        # Update average system size
        total_capacity = 0
        count = 0
        for calc in self.mock_data['calculations'].values():
            total_capacity += calc['plant_capacity']
            count += 1
        
        if count > 0:
            analytics['average_system_size'] = round(total_capacity / count, 2)
        
        # Update top cities
        city_counts = {}
        for calc in self.mock_data['calculations'].values():
            city = calc['location_city']
            city_counts[city] = city_counts.get(city, 0) + 1
        
        analytics['top_cities'] = sorted(city_counts.items(), key=lambda x: x[1], reverse=True)[:5]
