"""
Supabase client for database operations
"""

import os
from supabase import create_client, Client
from datetime import datetime
import uuid
import json
from typing import Dict, Any, Optional

class SupabaseClient:
    def __init__(self):
        """Initialize Supabase client"""
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')

        # Check if we have real credentials (not placeholder values)
        if (not self.url or not self.key or
            'your-project-id' in self.url or
            'your-anon-key-here' in self.key):
            raise ValueError("Supabase URL and KEY must be set with real values in environment variables")

        self.supabase: Client = create_client(self.url, self.key)

    def save_calculation(self, form_data: Dict[str, Any], solar_data: Dict[str, Any],
                        results: Dict[str, Any]) -> str:
        """
        Save calculation data to Supabase

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

            # Prepare data for database
            db_data = {
                'id': calculation_id,
                'created_at': datetime.utcnow().isoformat(),

                # User Input Data
                'location_city': form_data['location_city'],
                'location_state': solar_data.get('state', ''),
                'location_country': 'India',
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

                # Metadata
                'calculation_version': '2.0',
                'user_ip': '',  # Can be populated from request
                'user_agent': ''  # Can be populated from request
            }

            # Insert into database
            result = self.supabase.table('solar_calculations').insert(db_data).execute()

            if result.data:
                return calculation_id
            else:
                raise Exception("Failed to save calculation to database")

        except Exception as e:
            print(f"Error saving calculation: {str(e)}")
            raise e

    def get_calculation(self, calculation_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve calculation data by ID

        Args:
            calculation_id: Calculation ID

        Returns:
            Dict containing calculation data or None if not found
        """
        try:
            result = self.supabase.table('solar_calculations').select('*').eq('id', calculation_id).execute()

            if result.data and len(result.data) > 0:
                return result.data[0]
            else:
                return None

        except Exception as e:
            print(f"Error retrieving calculation: {str(e)}")
            return None

    def get_recent_calculations(self, limit: int = 10) -> list:
        """
        Get recent calculations for analytics

        Args:
            limit: Number of records to retrieve

        Returns:
            List of recent calculations
        """
        try:
            result = self.supabase.table('solar_calculations').select('*').order('created_at', desc=True).limit(limit).execute()
            return result.data or []

        except Exception as e:
            print(f"Error retrieving recent calculations: {str(e)}")
            return []

    def save_location_data(self, city: str, state: str, solar_data: Dict[str, Any]) -> bool:
        """
        Save or update location solar data

        Args:
            city: City name
            state: State name
            solar_data: Solar irradiance and location data

        Returns:
            bool: Success status
        """
        try:
            location_data = {
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

            # Try to update existing record, insert if not exists
            result = self.supabase.table('location_solar_data').upsert(location_data).execute()

            return bool(result.data)

        except Exception as e:
            print(f"Error saving location data: {str(e)}")
            return False

    def get_analytics_data(self) -> Dict[str, Any]:
        """
        Get analytics data for dashboard

        Returns:
            Dict containing analytics information
        """
        try:
            # Get total calculations
            total_result = self.supabase.table('solar_calculations').select('id', count='exact').execute()
            total_calculations = total_result.count or 0

            # Get calculations by investment model
            capex_result = self.supabase.table('solar_calculations').select('id', count='exact').eq('investment_model', 'CAPEX').execute()
            opex_result = self.supabase.table('solar_calculations').select('id', count='exact').eq('investment_model', 'OPEX').execute()

            # Get average system size
            avg_result = self.supabase.table('solar_calculations').select('plant_capacity').execute()
            avg_capacity = 0
            if avg_result.data:
                capacities = [float(row['plant_capacity']) for row in avg_result.data if row['plant_capacity']]
                avg_capacity = sum(capacities) / len(capacities) if capacities else 0

            # Get top cities
            city_result = self.supabase.table('solar_calculations').select('location_city', count='exact').execute()
            city_counts = {}
            if city_result.data:
                for row in city_result.data:
                    city = row['location_city']
                    city_counts[city] = city_counts.get(city, 0) + 1

            top_cities = sorted(city_counts.items(), key=lambda x: x[1], reverse=True)[:5]

            return {
                'total_calculations': total_calculations,
                'capex_calculations': capex_result.count or 0,
                'opex_calculations': opex_result.count or 0,
                'average_system_size': round(avg_capacity, 2),
                'top_cities': top_cities
            }

        except Exception as e:
            print(f"Error getting analytics data: {str(e)}")
            return {
                'total_calculations': 0,
                'capex_calculations': 0,
                'opex_calculations': 0,
                'average_system_size': 0,
                'top_cities': []
            }
