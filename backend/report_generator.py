"""
PDF Report Generator for Solar Calculator Results
"""

import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import tempfile
from typing import Dict, Any

class ReportGenerator:
    def __init__(self):
        """Initialize report generator"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for the report"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2E8B57')
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#4CAF50')
        )
        
        # Section header style
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#FF6B35')
        )
        
        # Normal text with custom formatting
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6
        )
    
    def generate_pdf_report(self, calculation_data: Dict[str, Any]) -> str:
        """
        Generate comprehensive PDF report
        
        Args:
            calculation_data: Complete calculation data from database
            
        Returns:
            Path to generated PDF file
        """
        # Create temporary file
        temp_dir = tempfile.gettempdir()
        pdf_filename = f"solar_report_{calculation_data['id']}.pdf"
        pdf_path = os.path.join(temp_dir, pdf_filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=A4, 
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Build content
        story = []
        
        # Header
        story.extend(self._build_header(calculation_data))
        
        # Input Summary
        story.extend(self._build_input_summary(calculation_data))
        
        # System Specifications
        story.extend(self._build_system_specs(calculation_data))
        
        # Financial Analysis
        story.extend(self._build_financial_analysis(calculation_data))
        
        # Environmental Impact
        story.extend(self._build_environmental_impact(calculation_data))
        
        # Recommendations
        story.extend(self._build_recommendations(calculation_data))
        
        # Footer
        story.extend(self._build_footer())
        
        # Build PDF
        doc.build(story)
        
        return pdf_path
    
    def _build_header(self, data: Dict[str, Any]) -> list:
        """Build report header"""
        story = []
        
        # Title
        story.append(Paragraph("Solar Plant Financial Calculator", self.title_style))
        story.append(Paragraph("Comprehensive Analysis Report", self.subtitle_style))
        story.append(Spacer(1, 20))
        
        # Report info
        report_info = [
            ['Report Generated:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
            ['Calculation ID:', data['id'][:8] + '...'],
            ['Location:', f"{data['location_city']}, {data.get('location_state', 'India')}"],
            ['Investment Model:', data['investment_model']],
            ['Consumer Type:', data['consumer_type']]
        ]
        
        info_table = Table(report_info, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 30))
        
        return story
    
    def _build_input_summary(self, data: Dict[str, Any]) -> list:
        """Build input summary section"""
        story = []
        
        story.append(Paragraph("Input Summary", self.section_style))
        
        input_data = [
            ['Monthly Electricity Bill', f"₹{data['monthly_bill']:,.0f}"],
            ['Monthly Consumption', f"{data.get('monthly_consumption', 0):,.0f} kWh"],
            ['Electricity Tariff Rate', f"₹{data['tariff_rate']:.2f}/unit"],
            ['Solar Irradiance', f"{data.get('solar_irradiance', 0):.1f} kWh/m²/day"],
            ['Installation Type', data['installation_type']],
            ['Consumer Category', data['consumer_category']],
            ['Shadow-free Area', 'Yes' if data.get('shadow_free_area', True) else 'No']
        ]
        
        if data.get('rooftop_area', 0) > 0:
            input_data.append(['Available Rooftop Area', f"{data['rooftop_area']:,.0f} sq ft"])
        
        input_table = Table(input_data, colWidths=[3*inch, 2*inch])
        input_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(input_table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _build_system_specs(self, data: Dict[str, Any]) -> list:
        """Build system specifications section"""
        story = []
        
        story.append(Paragraph("Recommended System Specifications", self.section_style))
        
        specs_data = [
            ['System Capacity', f"{data['plant_capacity']:.1f} kWp"],
            ['Estimated Panel Count', f"{data.get('panel_count', 0):,} panels"],
            ['Inverter Capacity', f"{data.get('inverter_capacity', 0):.1f} kW"],
            ['Estimated Area Required', f"{data.get('estimated_area_required', 0):.0f} sq ft"],
            ['Monthly Generation', f"{data['monthly_generation']:,.0f} kWh"],
            ['Annual Generation', f"{data['yearly_generation']:,.0f} kWh"]
        ]
        
        specs_table = Table(specs_data, colWidths=[3*inch, 2*inch])
        specs_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e8')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(specs_table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _build_financial_analysis(self, data: Dict[str, Any]) -> list:
        """Build financial analysis section"""
        story = []
        
        story.append(Paragraph("Financial Analysis", self.section_style))
        
        financial_data = [
            ['Monthly Savings', f"₹{data['monthly_savings']:,.0f}"],
            ['Annual Savings', f"₹{data['annual_savings']:,.0f}"],
            ['25-Year Total Savings', f"₹{data['lifetime_savings']:,.0f}"]
        ]
        
        if data['investment_model'] == 'CAPEX':
            financial_data.extend([
                ['Total Investment Required', f"₹{data['investment_amount']:,.0f}"],
                ['Payback Period', f"{data['payback_period']:.1f} years"],
                ['Return on Investment (25 years)', f"{((data['lifetime_savings'] / data['investment_amount']) * 100):.1f}%"]
            ])
        
        financial_table = Table(financial_data, colWidths=[3*inch, 2*inch])
        financial_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff3cd')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(financial_table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _build_environmental_impact(self, data: Dict[str, Any]) -> list:
        """Build environmental impact section"""
        story = []
        
        story.append(Paragraph("Environmental Impact", self.section_style))
        
        env_data = [
            ['Annual CO₂ Reduction', f"{data['co2_saved_annual']:.1f} tons"],
            ['25-Year CO₂ Reduction', f"{data['co2_saved_lifetime']:.1f} tons"],
            ['Equivalent Trees Planted', f"{data['equivalent_trees']:,.0f} trees"]
        ]
        
        env_table = Table(env_data, colWidths=[3*inch, 2*inch])
        env_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#d4edda')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(env_table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _build_recommendations(self, data: Dict[str, Any]) -> list:
        """Build recommendations section"""
        story = []
        
        story.append(Paragraph("Recommendations", self.section_style))
        
        # Add some standard recommendations based on the data
        recommendations = []
        
        if data['investment_model'] == 'CAPEX' and data['payback_period'] <= 6:
            recommendations.append("✓ Excellent investment opportunity with quick payback period")
        
        if data['plant_capacity'] > 10:
            recommendations.append("✓ Consider phased installation to spread investment")
        
        if data['consumer_type'] == 'Commercial':
            recommendations.append("✓ Explore accelerated depreciation benefits for commercial installations")
        
        recommendations.extend([
            "✓ Ensure regular cleaning and maintenance for optimal performance",
            "✓ Consider battery storage for backup power during outages",
            "✓ Monitor system performance through mobile app or web portal",
            "✓ Review electricity bill patterns after installation"
        ])
        
        for rec in recommendations:
            story.append(Paragraph(rec, self.normal_style))
        
        story.append(Spacer(1, 20))
        
        return story
    
    def _build_footer(self) -> list:
        """Build report footer"""
        story = []
        
        story.append(Spacer(1, 30))
        
        footer_text = """
        <b>Disclaimer:</b> This report is generated based on the inputs provided and standard assumptions. 
        Actual results may vary based on local conditions, system quality, maintenance, and other factors. 
        Please consult with certified solar installers for detailed site assessment and final system design.
        """
        
        story.append(Paragraph(footer_text, self.normal_style))
        
        # Contact info
        contact_text = """
        <b>Generated by:</b> Solar Plant Financial Calculator v2.0<br/>
        For more information, visit our website or contact our support team.
        """
        
        story.append(Spacer(1, 10))
        story.append(Paragraph(contact_text, self.normal_style))
        
        return story
