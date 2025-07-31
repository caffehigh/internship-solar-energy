"""
Enhanced solar data fetcher with Global Solar Atlas integration
"""

import requests
import os
from typing import Dict, Any, Optional
import json
from utils.location_data import get_location_info

class SolarDataFetcher:
    def __init__(self):
        """Initialize solar data fetcher"""
        self.api_key = os.getenv('SOLAR_ATLAS_API_KEY')
        self.base_url = "https://globalsolaratlas.info/api"
        
        # Coordinates for major Indian cities (for API calls)
        self.city_coordinates = {
            "Delhi": {"lat": 28.7041, "lon": 77.1025},
            "Mumbai": {"lat": 19.0760, "lon": 72.8777},
            "Bangalore": {"lat": 12.9716, "lon": 77.5946},
            "Chennai": {"lat": 13.0827, "lon": 80.2707},
            "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
            "Pune": {"lat": 18.5204, "lon": 73.8567},
            "Kolkata": {"lat": 22.5726, "lon": 88.3639},
            "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
            "Jaipur": {"lat": 26.9124, "lon": 75.7873},
            "Surat": {"lat": 21.1702, "lon": 72.8311},
            "Lucknow": {"lat": 26.8467, "lon": 80.9462},
            "Kanpur": {"lat": 26.4499, "lon": 80.3319},
            "Nagpur": {"lat": 21.1458, "lon": 79.0882},
            "Indore": {"lat": 22.7196, "lon": 75.8577},
            "Thane": {"lat": 19.2183, "lon": 72.9781},
            "Bhopal": {"lat": 23.2599, "lon": 77.4126},
            "Visakhapatnam": {"lat": 17.6868, "lon": 83.2185},
            "Pimpri-Chinchwad": {"lat": 18.6298, "lon": 73.7997},
            "Patna": {"lat": 25.5941, "lon": 85.1376},
            "Vadodara": {"lat": 22.3072, "lon": 73.1812}
        }
    
    def get_enhanced_solar_data(self, city: str, fallback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get enhanced solar data for a city, with API integration and fallback

        Args:
            city: City name
            fallback_data: Fallback data from local database

        Returns:
            Dict containing enhanced solar data
        """
        try:
            # For local deployment, always use enhanced local data
            # API integration disabled to avoid network issues
            return self._enhance_local_data(city, fallback_data)

        except Exception as e:
            print(f"Error fetching enhanced solar data: {str(e)}")
            return self._enhance_local_data(city, fallback_data)
    
    def _fetch_from_api(self, city: str) -> Optional[Dict[str, Any]]:
        """
        Fetch solar data from Global Solar Atlas API
        
        Args:
            city: City name
            
        Returns:
            Dict containing API data or None if failed
        """
        try:
            coords = self.city_coordinates.get(city)
            if not coords:
                return None
            
            # Note: This is a placeholder for actual Global Solar Atlas API
            # The real API endpoint and parameters would need to be configured
            # based on the actual API documentation
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'format': 'json'
            }
            
            # Placeholder API call - replace with actual endpoint
            # response = requests.get(f"{self.base_url}/solar-data", headers=headers, params=params)
            
            # For now, return enhanced local data with coordinates
            return {
                'latitude': coords['lat'],
                'longitude': coords['lon'],
                'data_source': 'api_enhanced',
                'ghi_annual': self._estimate_ghi_from_irradiance(city),
                'dni_annual': self._estimate_dni_from_irradiance(city)
            }
            
        except Exception as e:
            print(f"API fetch error for {city}: {str(e)}")
            return None
    
    def _enhance_local_data(self, city: str, local_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance local data with additional calculations
        
        Args:
            city: City name
            local_data: Local database data
            
        Returns:
            Dict containing enhanced local data
        """
        enhanced_data = local_data.copy()
        
        # Add coordinates if available
        if city in self.city_coordinates:
            coords = self.city_coordinates[city]
            enhanced_data.update({
                'latitude': coords['lat'],
                'longitude': coords['lon']
            })
        
        # Estimate GHI and DNI from irradiance
        irradiance = local_data.get('irradiance', 4.5)
        enhanced_data.update({
            'ghi_annual': self._estimate_ghi_from_irradiance(city, irradiance),
            'dni_annual': self._estimate_dni_from_irradiance(city, irradiance),
            'data_source': 'local_enhanced'
        })
        
        # Add climate zone information
        enhanced_data['climate_zone'] = self._get_climate_zone(city)
        
        # Add seasonal variation estimates
        enhanced_data['seasonal_variation'] = self._get_seasonal_variation(city)
        
        return enhanced_data
    
    def _estimate_ghi_from_irradiance(self, city: str, irradiance: float = None) -> float:
        """
        Estimate Global Horizontal Irradiance from daily irradiance
        
        Args:
            city: City name
            irradiance: Daily irradiance (kWh/m²/day)
            
        Returns:
            Annual GHI (kWh/m²/year)
        """
        if irradiance is None:
            local_data = get_location_info(city)
            irradiance = local_data.get('irradiance', 4.5)
        
        # Convert daily irradiance to annual GHI
        # Assuming some seasonal variation and efficiency factors
        annual_ghi = irradiance * 365 * 0.85  # 85% efficiency factor
        return round(annual_ghi, 2)
    
    def _estimate_dni_from_irradiance(self, city: str, irradiance: float = None) -> float:
        """
        Estimate Direct Normal Irradiance from daily irradiance
        
        Args:
            city: City name
            irradiance: Daily irradiance (kWh/m²/day)
            
        Returns:
            Annual DNI (kWh/m²/year)
        """
        if irradiance is None:
            local_data = get_location_info(city)
            irradiance = local_data.get('irradiance', 4.5)
        
        # DNI is typically 80-90% of GHI in good solar regions
        ghi = self._estimate_ghi_from_irradiance(city, irradiance)
        dni = ghi * 0.85  # 85% of GHI
        return round(dni, 2)
    
    def _get_climate_zone(self, city: str) -> str:
        """
        Get climate zone for a city
        
        Args:
            city: City name
            
        Returns:
            Climate zone classification
        """
        # Simplified climate zone mapping for Indian cities
        desert_cities = ['Jaipur', 'Jodhpur', 'Bikaner', 'Ahmedabad']
        coastal_cities = ['Mumbai', 'Chennai', 'Visakhapatnam', 'Kochi']
        hill_cities = ['Shimla', 'Darjeeling', 'Ooty']
        
        if city in desert_cities:
            return 'Hot-Dry'
        elif city in coastal_cities:
            return 'Hot-Humid'
        elif city in hill_cities:
            return 'Temperate'
        else:
            return 'Composite'
    
    def _get_seasonal_variation(self, city: str) -> Dict[str, float]:
        """
        Get seasonal irradiance variation for a city
        
        Args:
            city: City name
            
        Returns:
            Dict with seasonal multipliers
        """
        # Simplified seasonal variation for Indian cities
        # Based on typical solar patterns in India
        
        local_data = get_location_info(city)
        base_irradiance = local_data.get('irradiance', 4.5)
        
        # Seasonal multipliers (relative to annual average)
        return {
            'winter': round(base_irradiance * 0.8, 2),  # Dec-Feb
            'summer': round(base_irradiance * 1.2, 2),  # Mar-May
            'monsoon': round(base_irradiance * 0.6, 2), # Jun-Sep
            'post_monsoon': round(base_irradiance * 1.0, 2)  # Oct-Nov
        }
    
    def get_weather_impact_factors(self, city: str) -> Dict[str, float]:
        """
        Get weather impact factors for solar generation
        
        Args:
            city: City name
            
        Returns:
            Dict with weather impact factors
        """
        climate_zone = self._get_climate_zone(city)
        
        # Weather impact factors based on climate zone
        factors = {
            'Hot-Dry': {
                'dust_factor': 0.95,  # 5% loss due to dust
                'temperature_factor': 0.92,  # 8% loss due to high temperature
                'humidity_factor': 0.98,  # 2% loss due to low humidity
                'cloud_factor': 0.95   # 5% loss due to occasional clouds
            },
            'Hot-Humid': {
                'dust_factor': 0.98,  # 2% loss due to dust (rain cleans)
                'temperature_factor': 0.94,  # 6% loss due to high temperature
                'humidity_factor': 0.96,  # 4% loss due to high humidity
                'cloud_factor': 0.85   # 15% loss due to frequent clouds
            },
            'Temperate': {
                'dust_factor': 0.97,  # 3% loss due to dust
                'temperature_factor': 0.98,  # 2% loss due to moderate temperature
                'humidity_factor': 0.97,  # 3% loss due to moderate humidity
                'cloud_factor': 0.90   # 10% loss due to clouds
            },
            'Composite': {
                'dust_factor': 0.96,  # 4% loss due to dust
                'temperature_factor': 0.95,  # 5% loss due to variable temperature
                'humidity_factor': 0.97,  # 3% loss due to variable humidity
                'cloud_factor': 0.90   # 10% loss due to variable cloud cover
            }
        }
        
        return factors.get(climate_zone, factors['Composite'])
