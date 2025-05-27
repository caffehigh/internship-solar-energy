"""
Location data with solar irradiance information for Indian cities
"""

# Solar irradiance data for major Indian cities (kWh/m²/day)
LOCATION_DATA = {
    "Delhi": {"state": "Delhi", "irradiance": 4.5, "tariff": 6.5},
    "Mumbai": {"state": "Maharashtra", "irradiance": 4.8, "tariff": 7.2},
    "Bangalore": {"state": "Karnataka", "irradiance": 5.2, "tariff": 5.8},
    "Chennai": {"state": "Tamil Nadu", "irradiance": 5.5, "tariff": 4.5},
    "Hyderabad": {"state": "Telangana", "irradiance": 5.3, "tariff": 6.8},
    "Pune": {"state": "Maharashtra", "irradiance": 5.0, "tariff": 7.0},
    "Kolkata": {"state": "West Bengal", "irradiance": 4.2, "tariff": 6.2},
    "Ahmedabad": {"state": "Gujarat", "irradiance": 5.8, "tariff": 5.5},
    "Jaipur": {"state": "Rajasthan", "irradiance": 6.0, "tariff": 5.2},
    "Lucknow": {"state": "Uttar Pradesh", "irradiance": 4.8, "tariff": 5.8},
    "Kanpur": {"state": "Uttar Pradesh", "irradiance": 4.7, "tariff": 5.8},
    "Nagpur": {"state": "Maharashtra", "irradiance": 5.4, "tariff": 7.0},
    "Indore": {"state": "Madhya Pradesh", "irradiance": 5.6, "tariff": 6.0},
    "Thane": {"state": "Maharashtra", "irradiance": 4.8, "tariff": 7.2},
    "Bhopal": {"state": "Madhya Pradesh", "irradiance": 5.5, "tariff": 6.0},
    "Visakhapatnam": {"state": "Andhra Pradesh", "irradiance": 5.1, "tariff": 6.5},
    "Pimpri-Chinchwad": {"state": "Maharashtra", "irradiance": 5.0, "tariff": 7.0},
    "Patna": {"state": "Bihar", "irradiance": 4.5, "tariff": 5.5},
    "Vadodara": {"state": "Gujarat", "irradiance": 5.7, "tariff": 5.5},
    "Ghaziabad": {"state": "Uttar Pradesh", "irradiance": 4.5, "tariff": 5.8},
    "Ludhiana": {"state": "Punjab", "irradiance": 4.3, "tariff": 6.8},
    "Agra": {"state": "Uttar Pradesh", "irradiance": 4.9, "tariff": 5.8},
    "Nashik": {"state": "Maharashtra", "irradiance": 5.2, "tariff": 7.0},
    "Faridabad": {"state": "Haryana", "irradiance": 4.6, "tariff": 6.0},
    "Meerut": {"state": "Uttar Pradesh", "irradiance": 4.7, "tariff": 5.8},
    "Rajkot": {"state": "Gujarat", "irradiance": 5.9, "tariff": 5.5},
    "Kalyan-Dombivali": {"state": "Maharashtra", "irradiance": 4.8, "tariff": 7.2},
    "Vasai-Virar": {"state": "Maharashtra", "irradiance": 4.8, "tariff": 7.2},
    "Varanasi": {"state": "Uttar Pradesh", "irradiance": 4.6, "tariff": 5.8},
    "Srinagar": {"state": "Jammu and Kashmir", "irradiance": 4.8, "tariff": 4.2},
    "Aurangabad": {"state": "Maharashtra", "irradiance": 5.3, "tariff": 7.0},
    "Dhanbad": {"state": "Jharkhand", "irradiance": 4.4, "tariff": 5.0},
    "Amritsar": {"state": "Punjab", "irradiance": 4.4, "tariff": 6.8},
    "Navi Mumbai": {"state": "Maharashtra", "irradiance": 4.8, "tariff": 7.2},
    "Allahabad": {"state": "Uttar Pradesh", "irradiance": 4.8, "tariff": 5.8},
    "Ranchi": {"state": "Jharkhand", "irradiance": 4.6, "tariff": 5.0},
    "Howrah": {"state": "West Bengal", "irradiance": 4.2, "tariff": 6.2},
    "Coimbatore": {"state": "Tamil Nadu", "irradiance": 5.4, "tariff": 4.5},
    "Jabalpur": {"state": "Madhya Pradesh", "irradiance": 5.4, "tariff": 6.0},
    "Gwalior": {"state": "Madhya Pradesh", "irradiance": 5.3, "tariff": 6.0},
    "Vijayawada": {"state": "Andhra Pradesh", "irradiance": 5.2, "tariff": 6.5},
    "Jodhpur": {"state": "Rajasthan", "irradiance": 6.2, "tariff": 5.2},
    "Madurai": {"state": "Tamil Nadu", "irradiance": 5.6, "tariff": 4.5},
    "Raipur": {"state": "Chhattisgarh", "irradiance": 5.1, "tariff": 5.5},
    "Kota": {"state": "Rajasthan", "irradiance": 5.9, "tariff": 5.2},
    "Chandigarh": {"state": "Chandigarh", "irradiance": 4.5, "tariff": 5.5},
    "Guwahati": {"state": "Assam", "irradiance": 3.8, "tariff": 6.0},
    "Solapur": {"state": "Maharashtra", "irradiance": 5.4, "tariff": 7.0},
    "Hubli-Dharwad": {"state": "Karnataka", "irradiance": 5.1, "tariff": 5.8},
    "Bareilly": {"state": "Uttar Pradesh", "irradiance": 4.6, "tariff": 5.8},
    "Moradabad": {"state": "Uttar Pradesh", "irradiance": 4.6, "tariff": 5.8},
    "Mysore": {"state": "Karnataka", "irradiance": 5.0, "tariff": 5.8},
    "Gurgaon": {"state": "Haryana", "irradiance": 4.6, "tariff": 6.0},
    "Aligarh": {"state": "Uttar Pradesh", "irradiance": 4.7, "tariff": 5.8},
    "Jalandhar": {"state": "Punjab", "irradiance": 4.3, "tariff": 6.8},
    "Tiruchirappalli": {"state": "Tamil Nadu", "irradiance": 5.5, "tariff": 4.5},
    "Bhubaneswar": {"state": "Odisha", "irradiance": 4.9, "tariff": 5.2},
    "Salem": {"state": "Tamil Nadu", "irradiance": 5.4, "tariff": 4.5},
    "Warangal": {"state": "Telangana", "irradiance": 5.2, "tariff": 6.8},
    "Mira-Bhayandar": {"state": "Maharashtra", "irradiance": 4.8, "tariff": 7.2},
    "Thiruvananthapuram": {"state": "Kerala", "irradiance": 4.7, "tariff": 5.8},
    "Bhiwandi": {"state": "Maharashtra", "irradiance": 4.8, "tariff": 7.2},
    "Saharanpur": {"state": "Uttar Pradesh", "irradiance": 4.6, "tariff": 5.8},
    "Guntur": {"state": "Andhra Pradesh", "irradiance": 5.3, "tariff": 6.5},
    "Amravati": {"state": "Maharashtra", "irradiance": 5.3, "tariff": 7.0},
    "Bikaner": {"state": "Rajasthan", "irradiance": 6.1, "tariff": 5.2},
    "Noida": {"state": "Uttar Pradesh", "irradiance": 4.5, "tariff": 5.8},
    "Jamshedpur": {"state": "Jharkhand", "irradiance": 4.5, "tariff": 5.0},
    "Bhilai Nagar": {"state": "Chhattisgarh", "irradiance": 5.1, "tariff": 5.5},
    "Cuttack": {"state": "Odisha", "irradiance": 4.8, "tariff": 5.2},
    "Firozabad": {"state": "Uttar Pradesh", "irradiance": 4.8, "tariff": 5.8},
    "Kochi": {"state": "Kerala", "irradiance": 4.6, "tariff": 5.8},
    "Bhavnagar": {"state": "Gujarat", "irradiance": 5.8, "tariff": 5.5},
    "Dehradun": {"state": "Uttarakhand", "irradiance": 4.4, "tariff": 5.5},
    "Durgapur": {"state": "West Bengal", "irradiance": 4.3, "tariff": 6.2},
    "Asansol": {"state": "West Bengal", "irradiance": 4.3, "tariff": 6.2},
    "Nanded": {"state": "Maharashtra", "irradiance": 5.4, "tariff": 7.0},
    "Kolhapur": {"state": "Maharashtra", "irradiance": 5.1, "tariff": 7.0},
    "Ajmer": {"state": "Rajasthan", "irradiance": 5.8, "tariff": 5.2},
    "Akola": {"state": "Maharashtra", "irradiance": 5.5, "tariff": 7.0},
    "Gulbarga": {"state": "Karnataka", "irradiance": 5.2, "tariff": 5.8},
    "Jamnagar": {"state": "Gujarat", "irradiance": 5.9, "tariff": 5.5},
    "Ujjain": {"state": "Madhya Pradesh", "irradiance": 5.5, "tariff": 6.0},
    "Loni": {"state": "Uttar Pradesh", "irradiance": 4.5, "tariff": 5.8},
    "Siliguri": {"state": "West Bengal", "irradiance": 4.0, "tariff": 6.2},
    "Jhansi": {"state": "Uttar Pradesh", "irradiance": 4.9, "tariff": 5.8},
    "Ulhasnagar": {"state": "Maharashtra", "irradiance": 4.8, "tariff": 7.2},
    "Jammu": {"state": "Jammu and Kashmir", "irradiance": 4.7, "tariff": 4.2},
    "Sangli-Miraj & Kupwad": {"state": "Maharashtra", "irradiance": 5.2, "tariff": 7.0},
    "Mangalore": {"state": "Karnataka", "irradiance": 4.8, "tariff": 5.8},
    "Erode": {"state": "Tamil Nadu", "irradiance": 5.4, "tariff": 4.5},
    "Belgaum": {"state": "Karnataka", "irradiance": 5.1, "tariff": 5.8},
    "Ambattur": {"state": "Tamil Nadu", "irradiance": 5.5, "tariff": 4.5},
    "Tirunelveli": {"state": "Tamil Nadu", "irradiance": 5.6, "tariff": 4.5},
    "Malegaon": {"state": "Maharashtra", "irradiance": 5.2, "tariff": 7.0},
    "Gaya": {"state": "Bihar", "irradiance": 4.6, "tariff": 5.5},
    "Jalgaon": {"state": "Maharashtra", "irradiance": 5.4, "tariff": 7.0},
    "Udaipur": {"state": "Rajasthan", "irradiance": 5.9, "tariff": 5.2},
    "Maheshtala": {"state": "West Bengal", "irradiance": 4.2, "tariff": 6.2}
}

def get_cities():
    """Return list of available cities"""
    return sorted(LOCATION_DATA.keys())

def get_location_info(city):
    """Get location information for a city"""
    return LOCATION_DATA.get(city, {"state": "Unknown", "irradiance": 4.5, "tariff": 6.0})

def get_default_tariff(city):
    """Get default electricity tariff for a city"""
    location_info = get_location_info(city)
    return location_info.get("tariff", 6.0)

def get_solar_irradiance(city):
    """Get solar irradiance for a city"""
    location_info = get_location_info(city)
    return location_info.get("irradiance", 4.5)
