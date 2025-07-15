"""
Enhanced Solar benefit calculation logic with precise formulas
"""
import math
from typing import Dict, Any, Optional

class SolarCalculator:
    def __init__(self):
        # Enhanced constants based on your specifications
        self.PERFORMANCE_RATIO = 0.75  # PR (Performance Ratio)
        self.SYSTEM_LIFETIME = 25  # years
        self.CO2_FACTOR = 0.8  # kg CO2 per unit
        self.DAYS_PER_MONTH = 30
        self.MONTHS_PER_YEAR = 12

        # Cost per kW based on consumer type and system size
        self.COST_PER_KW = {
            'Residential': {
                'small': 80000,    # < 5 kW
                'medium': 78000,   # 5-10 kW
                'large': 76000     # > 10 kW
            },
            'Commercial': {
                'small': 75000,    # < 50 kW
                'medium': 72000,   # 50-100 kW
                'large': 70000     # > 100 kW
            },
            'Industrial': {
                'small': 70000,    # < 100 kW
                'medium': 68000,   # 100-500 kW
                'large': 65000     # > 500 kW
            }
        }

    def calculate_monthly_consumption(self, monthly_bill, tariff_rate):
        """Calculate monthly electricity consumption from bill amount"""
        if tariff_rate <= 0:
            return 0
        return monthly_bill / tariff_rate

    def calculate_plant_capacity(self, monthly_consumption, avg_irradiance=4.5):
        """Calculate required plant capacity using: Capacity = Monthly Consumption / (Avg Irradiance × PR × 30)"""
        return monthly_consumption / (avg_irradiance * self.PERFORMANCE_RATIO * self.DAYS_PER_MONTH)

    def calculate_investment_capex_simple(self, capacity_kw, consumer_type="Residential"):
        """Calculate investment (CAPEX) using: Investment = Capacity × Cost per kW"""
        cost_per_kw = self.get_cost_per_kw(consumer_type, capacity_kw)
        return capacity_kw * cost_per_kw

    def calculate_monthly_generation(self, capacity_kw, avg_irradiance=4.5):
        """Calculate monthly generation using: Monthly Generation = Capacity × Avg Irradiance × PR × 30"""
        return capacity_kw * avg_irradiance * self.PERFORMANCE_RATIO * self.DAYS_PER_MONTH

    def calculate_yearly_generation(self, monthly_generation):
        """Calculate yearly generation using: Yearly Generation = Monthly Generation × 12"""
        return monthly_generation * self.MONTHS_PER_YEAR

    def calculate_annual_savings_from_generation(self, yearly_generation, tariff_rate):
        """Calculate annual savings using: Annual Savings = Yearly Generation × Tariff"""
        return yearly_generation * tariff_rate

    def calculate_monthly_savings_from_annual(self, annual_savings):
        """Calculate monthly savings from annual savings"""
        return annual_savings / self.MONTHS_PER_YEAR

    def calculate_payback_period_from_investment(self, investment, annual_savings):
        """Calculate payback period using: Payback Period = Investment / Annual Savings"""
        if annual_savings <= 0:
            return float('inf')
        return investment / annual_savings

    def calculate_co2_saved_annual(self, yearly_generation):
        """Calculate CO2 saved per year using: CO₂ Saved = Yearly Generation × 0.8"""
        co2_saved_kg = yearly_generation * self.CO2_FACTOR
        return co2_saved_kg / 1000  # Convert to tons

    def calculate_co2_saved_lifetime(self, annual_co2_saved):
        """Calculate total CO2 saved over 25 years"""
        return annual_co2_saved * self.SYSTEM_LIFETIME

    def calculate_lifetime_savings(self, annual_savings):
        """Calculate total savings over system lifetime"""
        return annual_savings * self.SYSTEM_LIFETIME

    def calculate_equivalent_trees(self, annual_co2_saved):
        """Calculate equivalent trees planted (1 tree = ~22 kg CO2/year)"""
        return (annual_co2_saved * 1000) / 22  # Convert tons to kg, then divide by 22 kg/tree

    def get_cost_per_kw(self, consumer_type: str, capacity: float) -> float:
        """
        Get cost per kW based on consumer type and system size

        Args:
            consumer_type: Type of consumer (Residential/Commercial/Industrial)
            capacity: System capacity in kW

        Returns:
            Cost per kW in ₹
        """
        cost_matrix = self.COST_PER_KW.get(consumer_type, self.COST_PER_KW['Residential'])

        if consumer_type == 'Residential':
            if capacity < 5:
                return cost_matrix['small']
            elif capacity <= 10:
                return cost_matrix['medium']
            else:
                return cost_matrix['large']
        elif consumer_type == 'Commercial':
            if capacity < 50:
                return cost_matrix['small']
            elif capacity <= 100:
                return cost_matrix['medium']
            else:
                return cost_matrix['large']
        else:  # Industrial
            if capacity < 100:
                return cost_matrix['small']
            elif capacity <= 500:
                return cost_matrix['medium']
            else:
                return cost_matrix['large']

    def calculate_plant_capacity_precise(self, monthly_consumption: float, avg_irradiance: float) -> float:
        """
        Calculate plant capacity using your specified formula:
        Plant Capacity (kW) = Monthly Consumption / (Avg Irradiance x PR x 30)

        Args:
            monthly_consumption: Monthly electricity consumption in kWh
            avg_irradiance: Average solar irradiance in kWh/m²/day

        Returns:
            Required plant capacity in kW
        """
        if avg_irradiance <= 0:
            avg_irradiance = 4.5  # Default fallback

        capacity = monthly_consumption / (avg_irradiance * self.PERFORMANCE_RATIO * 30)
        return max(1.0, capacity)  # Minimum 1 kW system

    def calculate_monthly_generation_precise(self, capacity: float, avg_irradiance: float) -> float:
        """
        Calculate monthly generation using your specified formula:
        Monthly Generation = Capacity x Avg Irradiance x PR x 30

        Args:
            capacity: System capacity in kW
            avg_irradiance: Average solar irradiance in kWh/m²/day

        Returns:
            Monthly generation in kWh
        """
        return capacity * avg_irradiance * self.PERFORMANCE_RATIO * 30

    def calculate_investment_capex(self, capacity: float, consumer_type: str) -> float:
        """
        Calculate investment for CAPEX model:
        Investment (CAPEX) = Capacity x Cost per kW

        Args:
            capacity: System capacity in kW
            consumer_type: Type of consumer

        Returns:
            Total investment in ₹
        """
        cost_per_kw = self.get_cost_per_kw(consumer_type, capacity)
        return capacity * cost_per_kw

    def calculate_annual_savings_precise(self, yearly_generation: float, tariff_rate: float) -> float:
        """
        Calculate annual savings:
        Savings/year = Yearly Generation x Tariff

        Args:
            yearly_generation: Annual generation in kWh
            tariff_rate: Electricity tariff rate in ₹/unit

        Returns:
            Annual savings in ₹
        """
        return yearly_generation * tariff_rate

    def calculate_payback_period_precise(self, investment: float, annual_savings: float) -> float:
        """
        Calculate payback period:
        Payback = Investment / Annual Savings

        Args:
            investment: Total investment in ₹
            annual_savings: Annual savings in ₹

        Returns:
            Payback period in years
        """
        if annual_savings <= 0:
            return 999  # Invalid case
        return investment / annual_savings

    def calculate_co2_saved(self, yearly_generation: float) -> float:
        """
        Calculate CO2 saved:
        CO2 Saved = Yearly Generation x 0.8 (kg CO2/unit)

        Args:
            yearly_generation: Annual generation in kWh

        Returns:
            CO2 saved in kg per year
        """
        return yearly_generation * self.CO2_FACTOR

    def get_comprehensive_analysis(self, monthly_bill: float, tariff_rate: float,
                                 investment_model: str = "CAPEX", solar_irradiance: float = None,
                                 consumer_type: str = "Residential") -> Dict[str, Any]:
        """
        Get comprehensive solar analysis using your precise formulas

        Args:
            monthly_bill: Monthly electricity bill in ₹
            tariff_rate: Electricity tariff rate in ₹/unit
            investment_model: "CAPEX" or "OPEX"
            solar_irradiance: Solar irradiance for location
            consumer_type: Type of consumer

        Returns:
            Dictionary with all calculations and recommendations
        """
        # Use provided solar irradiance or default
        avg_irradiance = solar_irradiance if solar_irradiance else 4.5

        # Step 1: Calculate monthly consumption
        monthly_consumption = self.calculate_monthly_consumption(monthly_bill, tariff_rate)

        # Step 2: Calculate plant capacity using precise formula
        plant_capacity = self.calculate_plant_capacity_precise(monthly_consumption, avg_irradiance)

        # Step 3: Calculate generation using precise formulas
        monthly_generation = self.calculate_monthly_generation_precise(plant_capacity, avg_irradiance)
        yearly_generation = monthly_generation * 12

        # Step 4: Calculate savings using precise formulas
        annual_savings = self.calculate_annual_savings_precise(yearly_generation, tariff_rate)
        monthly_savings = annual_savings / 12
        lifetime_savings = annual_savings * self.SYSTEM_LIFETIME

        # Step 5: Calculate environmental impact using precise formulas
        annual_co2_saved_kg = self.calculate_co2_saved(yearly_generation)
        annual_co2_saved = annual_co2_saved_kg / 1000  # Convert to tons
        lifetime_co2_saved = annual_co2_saved * self.SYSTEM_LIFETIME
        equivalent_trees = self.calculate_equivalent_trees(annual_co2_saved)

        # Step 6: Calculate investment and payback (only for CAPEX)
        investment = 0
        payback_period = 0
        if investment_model == "CAPEX":
            investment = self.calculate_investment_capex(plant_capacity, consumer_type)
            payback_period = self.calculate_payback_period_precise(investment, annual_savings)

        # Step 7: Calculate additional system specifications
        panel_count = math.ceil(plant_capacity / 0.4)  # Assuming 400W panels
        inverter_capacity = plant_capacity * 0.8  # 80% of DC capacity
        area_required = plant_capacity * 8  # ~8 sq ft per kW for rooftop

        # Step 8: Generate recommendations
        recommendations = self._generate_recommendations(
            plant_capacity, investment, payback_period, consumer_type, investment_model
        )

        return {
            "input_data": {
                "monthly_bill": monthly_bill,
                "tariff_rate": tariff_rate,
                "investment_model": investment_model,
                "consumer_type": consumer_type,
                "solar_irradiance": avg_irradiance
            },
            "calculations": {
                "monthly_consumption": round(monthly_consumption, 2),
                "plant_capacity": round(plant_capacity, 2),
                "monthly_generation": round(monthly_generation, 2),
                "yearly_generation": round(yearly_generation, 0),
                "monthly_savings": round(monthly_savings, 2),
                "annual_savings": round(annual_savings, 0),
                "lifetime_savings": round(lifetime_savings, 0),
                "investment": round(investment, 0),
                "payback_period": round(payback_period, 1),
                "annual_co2_saved": round(annual_co2_saved, 2),
                "lifetime_co2_saved": round(lifetime_co2_saved, 2),
                "equivalent_trees": round(equivalent_trees, 0),
                "panel_count": panel_count,
                "inverter_capacity": round(inverter_capacity, 2),
                "area_required": round(area_required, 2)
            },
            "recommendations": recommendations
        }

    def _generate_recommendations(self, capacity: float, investment: float,
                                payback_period: float, consumer_type: str,
                                investment_model: str) -> list:
        """Generate personalized recommendations based on calculations"""
        recommendations = []

        # System size recommendations
        if capacity < 3:
            recommendations.append({
                "type": "system_size",
                "title": "Small System Recommendation",
                "message": f"A {capacity:.1f} kW system is suitable for your consumption. Consider energy-efficient appliances to maximize benefits.",
                "priority": "medium"
            })
        elif capacity > 10 and consumer_type == "Residential":
            recommendations.append({
                "type": "system_size",
                "title": "Large Residential System",
                "message": f"Your {capacity:.1f} kW requirement is quite large for residential use. Consider splitting into phases or reviewing consumption patterns.",
                "priority": "high"
            })

        # Payback period recommendations
        if investment_model == "CAPEX":
            if payback_period <= 5:
                recommendations.append({
                    "type": "financial",
                    "title": "Excellent Investment",
                    "message": f"With a {payback_period:.1f} year payback period, this is an excellent investment opportunity.",
                    "priority": "high"
                })
            elif payback_period > 8:
                recommendations.append({
                    "type": "financial",
                    "title": "Consider OPEX Model",
                    "message": f"With a {payback_period:.1f} year payback, you might want to consider the OPEX/lease model instead.",
                    "priority": "medium"
                })

        # Consumer type specific recommendations
        if consumer_type == "Commercial":
            recommendations.append({
                "type": "tax_benefits",
                "title": "Tax Benefits Available",
                "message": "Commercial installations are eligible for accelerated depreciation and other tax benefits. Consult a tax advisor.",
                "priority": "medium"
            })

        return recommendations


