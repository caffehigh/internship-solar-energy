"""
Solar benefit calculation logic
"""
import math

class SolarCalculator:
    def __init__(self):
        # Constants based on requirements
        self.SOLAR_GENERATION_PER_KWP = 4  # units per kWp per day
        self.SYSTEM_COST_MIN = 76000  # ₹ per kWp
        self.SYSTEM_COST_MAX = 80000  # ₹ per kWp
        self.SYSTEM_LIFETIME = 25  # years
        self.CO2_FACTOR = 0.8  # kg CO2 per unit
        self.DAYS_PER_MONTH = 30
        self.MONTHS_PER_YEAR = 12
        
    def calculate_monthly_units(self, monthly_bill, tariff_rate):
        """Calculate monthly electricity units from bill amount"""
        if tariff_rate <= 0:
            return 0
        return monthly_bill / tariff_rate
    
    def calculate_required_capacity(self, monthly_units):
        """Calculate required solar capacity in kWp"""
        daily_units = monthly_units / self.DAYS_PER_MONTH
        return daily_units / self.SOLAR_GENERATION_PER_KWP
    
    def calculate_system_cost(self, capacity_kwp, user_type="Residential"):
        """Calculate system cost based on capacity and user type"""
        # Adjust cost based on user type
        cost_multipliers = {
            "Residential": 1.0,
            "Commercial": 0.95,  # Slight discount for commercial
            "Industrial": 0.90   # Better discount for industrial
        }
        
        multiplier = cost_multipliers.get(user_type, 1.0)
        base_cost = (self.SYSTEM_COST_MIN + self.SYSTEM_COST_MAX) / 2
        return capacity_kwp * base_cost * multiplier
    
    def calculate_monthly_savings(self, monthly_units, tariff_rate):
        """Calculate monthly electricity savings"""
        return monthly_units * tariff_rate
    
    def calculate_annual_savings(self, monthly_savings):
        """Calculate annual electricity savings"""
        return monthly_savings * self.MONTHS_PER_YEAR
    
    def calculate_payback_period(self, system_cost, annual_savings):
        """Calculate payback period in years"""
        if annual_savings <= 0:
            return float('inf')
        return system_cost / annual_savings
    
    def calculate_co2_saved(self, capacity_kwp):
        """Calculate CO2 saved per year in tons"""
        yearly_generation = capacity_kwp * self.SOLAR_GENERATION_PER_KWP * 365
        co2_saved_kg = yearly_generation * self.CO2_FACTOR
        return co2_saved_kg / 1000  # Convert to tons
    
    def calculate_lifetime_savings(self, annual_savings):
        """Calculate total savings over system lifetime"""
        return annual_savings * self.SYSTEM_LIFETIME
    
    def calculate_roi_percentage(self, system_cost, annual_savings):
        """Calculate Return on Investment percentage"""
        if system_cost <= 0:
            return 0
        return (annual_savings / system_cost) * 100
    
    def validate_rooftop_area(self, capacity_kwp, rooftop_area):
        """Check if rooftop area is sufficient for the required capacity"""
        # Assumption: 1 kWp requires approximately 100 sq ft
        required_area = capacity_kwp * 100
        return rooftop_area >= required_area, required_area
    
    def get_comprehensive_analysis(self, monthly_bill, tariff_rate, location, 
                                 user_type="Residential", rooftop_area=None):
        """
        Get comprehensive solar analysis
        
        Args:
            monthly_bill: Monthly electricity bill in ₹
            tariff_rate: Electricity tariff rate in ₹/unit
            location: City name
            user_type: Type of user (Residential/Commercial/Industrial)
            rooftop_area: Available rooftop area in sq ft (optional)
        
        Returns:
            Dictionary with all calculations and recommendations
        """
        # Basic calculations
        monthly_units = self.calculate_monthly_units(monthly_bill, tariff_rate)
        required_capacity = self.calculate_required_capacity(monthly_units)
        system_cost = self.calculate_system_cost(required_capacity, user_type)
        monthly_savings = self.calculate_monthly_savings(monthly_units, tariff_rate)
        annual_savings = self.calculate_annual_savings(monthly_savings)
        payback_period = self.calculate_payback_period(system_cost, annual_savings)
        co2_saved = self.calculate_co2_saved(required_capacity)
        lifetime_savings = self.calculate_lifetime_savings(annual_savings)
        roi_percentage = self.calculate_roi_percentage(system_cost, annual_savings)
        
        # Rooftop area validation
        area_sufficient = True
        required_area = required_capacity * 100
        if rooftop_area:
            area_sufficient, required_area = self.validate_rooftop_area(
                required_capacity, rooftop_area
            )
        
        # Recommendations
        recommendations = self._generate_recommendations(
            payback_period, roi_percentage, area_sufficient, user_type
        )
        
        return {
            "input_data": {
                "monthly_bill": monthly_bill,
                "tariff_rate": tariff_rate,
                "location": location,
                "user_type": user_type,
                "rooftop_area": rooftop_area
            },
            "calculations": {
                "monthly_units": round(monthly_units, 2),
                "required_capacity": round(required_capacity, 2),
                "system_cost": round(system_cost, 0),
                "monthly_savings": round(monthly_savings, 2),
                "annual_savings": round(annual_savings, 0),
                "payback_period": round(payback_period, 1),
                "co2_saved_tons": round(co2_saved, 2),
                "lifetime_savings": round(lifetime_savings, 0),
                "roi_percentage": round(roi_percentage, 1),
                "required_area": round(required_area, 0),
                "area_sufficient": area_sufficient
            },
            "recommendations": recommendations
        }
    
    def _generate_recommendations(self, payback_period, roi_percentage, 
                                area_sufficient, user_type):
        """Generate recommendations based on calculations"""
        recommendations = []
        
        if payback_period <= 6:
            recommendations.append("🟢 Excellent investment! Very quick payback period.")
        elif payback_period <= 10:
            recommendations.append("🟡 Good investment with reasonable payback period.")
        else:
            recommendations.append("🔴 Consider reviewing your electricity usage or tariff rates.")
        
        if roi_percentage >= 15:
            recommendations.append("💰 High return on investment expected.")
        elif roi_percentage >= 10:
            recommendations.append("📈 Moderate return on investment.")
        else:
            recommendations.append("📉 Low return on investment. Consider other factors.")
        
        if not area_sufficient:
            recommendations.append("⚠️ Insufficient rooftop area. Consider high-efficiency panels.")
        
        if user_type == "Commercial":
            recommendations.append("🏢 Commercial users can benefit from tax incentives and depreciation.")
        elif user_type == "Industrial":
            recommendations.append("🏭 Industrial users get the best rates and maximum benefits.")
        
        return recommendations
