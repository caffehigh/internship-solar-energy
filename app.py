"""
Solar Benefit Calculator - Streamlit Web Application
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.calculations import SolarCalculator
from utils.location_data import get_cities, get_default_tariff, get_location_info
from utils.ocr_processor import BillOCRProcessor

# Page configuration
st.set_page_config(
    page_title="Solar Benefit Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple, clean CSS styling
st.markdown("""
<style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

    .main-header {
        font-size: 2.5rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 600;
    }

    .sub-header {
        font-size: 1.3rem;
        color: #2E8B57;
        margin-bottom: 1rem;
        font-weight: 500;
    }

    .icon-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 1rem;
    }

    .solar-icon { color: #FFD700; }
    .chart-icon { color: #4CAF50; }
    .money-icon { color: #2196F3; }
    .settings-icon { color: #607D8B; }
    .upload-icon { color: #9C27B0; }

    .recommendation-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header with clean design
    st.markdown('''
    <div class="icon-header" style="justify-content: center;">
        <i class="fas fa-solar-panel solar-icon" style="font-size: 2.5rem;"></i>
        <h1 class="main-header" style="margin: 0;">Solar Benefit Calculator</h1>
    </div>
    <p style="text-align: center; font-size: 1.1rem; color: #666; margin-top: -1rem;">
        <i class="fas fa-calculator money-icon"></i> Calculate your potential savings with solar energy
    </p>
    ''', unsafe_allow_html=True)

    # Initialize calculator and OCR processor
    calculator = SolarCalculator()
    ocr_processor = BillOCRProcessor()

    # Sidebar for inputs
    with st.sidebar:
        st.markdown('''
        <div class="icon-header">
            <i class="fas fa-sliders-h settings-icon"></i>
            <h2 class="sub-header" style="margin: 0;">Input Parameters</h2>
        </div>
        ''', unsafe_allow_html=True)

        # OCR Upload Section
        st.markdown('''
        <div class="icon-header">
            <i class="fas fa-file-upload upload-icon"></i>
            <h3 style="margin: 0;">Upload Electricity Bill (Optional)</h3>
        </div>
        ''', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload your electricity bill",
            type=['pdf', 'png', 'jpg', 'jpeg'],
            help="Upload a PDF or image of your electricity bill for automatic data extraction"
        )

        # Initialize default values
        default_amount = 0.0
        default_units = 0.0
        default_tariff = 6.0

        # Process uploaded file
        if uploaded_file is not None:
            with st.spinner("Processing uploaded file..."):
                ocr_result = ocr_processor.process_uploaded_file(uploaded_file)

                if "error" in ocr_result:
                    st.error(ocr_result["error"])
                else:
                    st.success(ocr_result["message"])

                    if ocr_result.get("extracted_amount"):
                        default_amount = ocr_result["extracted_amount"]
                        st.info(f"Extracted Amount: ₹{default_amount}")

                    if ocr_result.get("extracted_units"):
                        default_units = ocr_result["extracted_units"]
                        calculated_tariff = default_amount / default_units if default_units > 0 else 6.0
                        # Ensure tariff is within reasonable bounds (1-20 ₹/unit)
                        default_tariff = max(1.0, min(calculated_tariff, 20.0))
                        st.info(f"Extracted Units: {default_units}")
                        st.info(f"Calculated Tariff: ₹{default_tariff:.2f}/unit")
                        if calculated_tariff > 20.0:
                            st.warning(f"⚠️ Calculated tariff (₹{calculated_tariff:.2f}/unit) seems high. Using ₹{default_tariff:.2f}/unit instead.")

        st.markdown("---")

        # Manual Input Section
        st.markdown('''
        <div class="icon-header">
            <i class="fas fa-edit money-icon"></i>
            <h3 style="margin: 0;">Manual Input</h3>
        </div>
        ''', unsafe_allow_html=True)

        # Monthly electricity bill
        safe_default = min(default_amount, 2500000.0) if default_amount > 0 else 3000.0
        monthly_bill = st.number_input(
            "Monthly Electricity Bill (₹)",
            min_value=0.0,
            max_value=2500000.0,
            value=safe_default,
            step=1000.0,
            help="Enter your average monthly electricity bill amount (up to ₹25,00,000)"
        )

        # Location selection
        cities = get_cities()
        selected_city = st.selectbox(
            "Select Your City",
            cities,
            index=cities.index("Delhi") if "Delhi" in cities else 0,
            help="Select your city to get location-specific calculations"
        )

        # Get location info
        location_info = get_location_info(selected_city)
        suggested_tariff = location_info["tariff"]

        # Tariff rate
        safe_tariff = max(1.0, min(default_tariff if default_tariff > 1.0 else suggested_tariff, 20.0))
        tariff_rate = st.number_input(
            "Electricity Tariff Rate (₹/unit)",
            min_value=1.0,
            max_value=20.0,
            value=safe_tariff,
            step=0.1,
            help=f"Suggested rate for {selected_city}: ₹{suggested_tariff}/unit"
        )

        st.markdown('''
        <div class="icon-header">
            <i class="fas fa-cogs settings-icon"></i>
            <h3 style="margin: 0;">Optional Parameters</h3>
        </div>
        ''', unsafe_allow_html=True)

        # User type
        user_type = st.selectbox(
            "Type of User",
            ["Residential", "Commercial", "Industrial"],
            help="Different user types have different cost structures"
        )

        # Rooftop area
        rooftop_area = st.number_input(
            "Available Rooftop Area (sq. ft.)",
            min_value=0.0,
            max_value=10000.0,
            value=1000.0,
            step=50.0,
            help="Enter available rooftop area for solar panel installation"
        )

        # Calculate button
        calculate_button = st.button("⚡ Calculate Solar Benefits", type="primary")

    # Main content area
    if calculate_button or monthly_bill > 0:
        if monthly_bill <= 0:
            st.error("Please enter a valid monthly electricity bill amount.")
            return

        # Perform calculations
        with st.spinner("Calculating solar benefits..."):
            analysis = calculator.get_comprehensive_analysis(
                monthly_bill=monthly_bill,
                tariff_rate=tariff_rate,
                location=selected_city,
                user_type=user_type,
                rooftop_area=rooftop_area
            )

        # Display results
        display_results(analysis, location_info)

    else:
        # Welcome message
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div class="icon-header" style="justify-content: center;">
                <i class="fas fa-sun solar-icon" style="font-size: 2rem;"></i>
                <h3>Welcome to the Solar Benefit Calculator!</h3>
            </div>
            <p><i class="fas fa-info-circle chart-icon"></i> Enter your electricity bill details in the sidebar to get started.</p>
            <p><i class="fas fa-upload upload-icon"></i> You can either upload your electricity bill for automatic data extraction or enter the details manually.</p>
        </div>
        """, unsafe_allow_html=True)

        # Show sample benefits
        show_sample_benefits()

def display_results(analysis, location_info):
    """Display calculation results"""
    calc = analysis["calculations"]
    recommendations = analysis["recommendations"]

    # Key Metrics Row
    st.markdown('''
    <div class="icon-header">
        <i class="fas fa-chart-line chart-icon"></i>
        <h2 class="sub-header" style="margin: 0;">Key Results</h2>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Recommended System Size",
            value=f"{calc['required_capacity']:.1f} kWp",
            help="Solar system capacity needed to meet your electricity needs"
        )

    with col2:
        st.metric(
            label="Estimated System Cost",
            value=f"₹{calc['system_cost']:,.0f}",
            help="Total cost of solar system installation"
        )

    with col3:
        st.metric(
            label="Annual Savings",
            value=f"₹{calc['annual_savings']:,.0f}",
            help="Expected annual electricity bill savings"
        )

    with col4:
        st.metric(
            label="Payback Period",
            value=f"{calc['payback_period']:.1f} years",
            help="Time to recover your investment"
        )

    # Detailed Analysis
    st.markdown('''
    <div class="icon-header">
        <i class="fas fa-analytics chart-icon"></i>
        <h2 class="sub-header" style="margin: 0;">Detailed Analysis</h2>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Monthly breakdown
        st.markdown("#### Monthly Breakdown")
        monthly_data = {
            "Parameter": [
                "Current Monthly Bill",
                "Monthly Units Consumed",
                "Monthly Savings with Solar",
                "Net Monthly Cost"
            ],
            "Value": [
                f"₹{analysis['input_data']['monthly_bill']:,.0f}",
                f"{calc['monthly_units']:.0f} units",
                f"₹{calc['monthly_savings']:,.0f}",
                f"₹{analysis['input_data']['monthly_bill'] - calc['monthly_savings']:,.0f}"
            ]
        }
        st.dataframe(pd.DataFrame(monthly_data), hide_index=True)

        # Environmental impact
        st.markdown("#### Environmental Impact")
        env_data = {
            "Parameter": [
                "CO₂ Saved per Year",
                "Equivalent Trees Planted",
                "25-Year CO₂ Reduction"
            ],
            "Value": [
                f"{calc['co2_saved_tons']:.1f} tons",
                f"{calc['co2_saved_tons'] * 16:.0f} trees",
                f"{calc['co2_saved_tons'] * 25:.1f} tons"
            ]
        }
        st.dataframe(pd.DataFrame(env_data), hide_index=True)

    with col2:
        # Financial summary
        st.markdown("#### Financial Summary")
        financial_data = {
            "Parameter": [
                "System Cost",
                "Annual Savings",
                "25-Year Total Savings",
                "Return on Investment",
                "Required Rooftop Area"
            ],
            "Value": [
                f"₹{calc['system_cost']:,.0f}",
                f"₹{calc['annual_savings']:,.0f}",
                f"₹{calc['lifetime_savings']:,.0f}",
                f"{calc['roi_percentage']:.1f}%",
                f"{calc['required_area']:.0f} sq ft"
            ]
        }
        st.dataframe(pd.DataFrame(financial_data), hide_index=True)

        # Area validation
        if calc['area_sufficient']:
            st.success("✅ Your rooftop area is sufficient for the recommended system size!")
        else:
            st.warning(f"⚠️ You need at least {calc['required_area']:.0f} sq ft for the recommended system.")

    # Visualizations
    create_visualizations(analysis)

    # Recommendations
    st.markdown('''
    <div class="icon-header">
        <i class="fas fa-lightbulb solar-icon"></i>
        <h2 class="sub-header" style="margin: 0;">Recommendations</h2>
    </div>
    ''', unsafe_allow_html=True)

    for recommendation in recommendations:
        st.markdown(f"""
        <div class="recommendation-box">
            {recommendation}
        </div>
        """, unsafe_allow_html=True)

def create_visualizations(analysis):
    """Create charts and visualizations"""
    calc = analysis["calculations"]

    st.markdown('''
    <div class="icon-header">
        <i class="fas fa-chart-bar chart-icon"></i>
        <h2 class="sub-header" style="margin: 0;">Visual Analysis</h2>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Savings over time chart
        years = list(range(1, 26))
        cumulative_savings = [calc['annual_savings'] * year for year in years]

        fig_savings = go.Figure()
        fig_savings.add_trace(go.Scatter(
            x=years,
            y=cumulative_savings,
            mode='lines+markers',
            name='Cumulative Savings',
            line=dict(color='#2E8B57', width=3)
        ))

        # Add system cost line
        fig_savings.add_hline(
            y=calc['system_cost'],
            line_dash="dash",
            line_color="red",
            annotation_text="System Cost"
        )

        fig_savings.update_layout(
            title="Cumulative Savings Over Time",
            xaxis_title="Years",
            yaxis_title="Savings (₹)",
            height=400
        )

        st.plotly_chart(fig_savings, use_container_width=True)

    with col2:
        # Monthly comparison pie chart
        monthly_bill = analysis['input_data']['monthly_bill']
        monthly_savings = calc['monthly_savings']
        remaining_bill = monthly_bill - monthly_savings

        fig_pie = go.Figure(data=[go.Pie(
            labels=['Solar Savings', 'Remaining Bill'],
            values=[monthly_savings, remaining_bill],
            hole=.3,
            marker_colors=['#2E8B57', '#FF6B35']
        )])

        fig_pie.update_layout(
            title="Monthly Bill Breakdown",
            height=400
        )

        st.plotly_chart(fig_pie, use_container_width=True)

def show_sample_benefits():
    """Show sample benefits for different bill amounts"""
    st.markdown('''
    <div class="icon-header">
        <i class="fas fa-coins money-icon"></i>
        <h2 class="sub-header" style="margin: 0;">Sample Benefits by Bill Amount</h2>
    </div>
    ''', unsafe_allow_html=True)

    calculator = SolarCalculator()
    sample_bills = [2000, 5000, 10000, 15000, 20000]
    sample_data = []

    for bill in sample_bills:
        analysis = calculator.get_comprehensive_analysis(
            monthly_bill=bill,
            tariff_rate=6.0,
            location="Delhi",
            user_type="Residential"
        )
        calc = analysis["calculations"]

        sample_data.append({
            "Monthly Bill (₹)": f"₹{bill:,}",
            "System Size (kWp)": f"{calc['required_capacity']:.1f}",
            "System Cost (₹)": f"₹{calc['system_cost']:,.0f}",
            "Annual Savings (₹)": f"₹{calc['annual_savings']:,.0f}",
            "Payback (Years)": f"{calc['payback_period']:.1f}"
        })

    df = pd.DataFrame(sample_data)
    st.dataframe(df, hide_index=True, use_container_width=True)

if __name__ == "__main__":
    main()

