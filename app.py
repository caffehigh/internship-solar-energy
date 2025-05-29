"""
Solar Benefit Calculator - Streamlit Web Application
"""
import streamlit as st
import pandas as pd
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
            <h3 style="margin: 0;">Investment Model</h3>
        </div>
        ''', unsafe_allow_html=True)

        # Investment Model
        investment_model = st.selectbox(
            "Investment Model",
            ["CAPEX", "OPEX"],
            help="CAPEX: Shows system cost and payback period. OPEX: Shows only savings and generation metrics."
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
                investment_model=investment_model
            )

        # Display results
        display_results(analysis, investment_model)

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

def display_results(analysis, investment_model):
    """Display calculation results with minimal UI"""
    calc = analysis["calculations"]

    # System Specifications
    st.markdown('''
    <div class="icon-header">
        <i class="fas fa-solar-panel solar-icon"></i>
        <h2 class="sub-header" style="margin: 0;">System Specifications</h2>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="System Size",
            value=f"{calc['plant_capacity']:.1f} kWp",
            help="Required solar plant capacity"
        )

    with col2:
        st.metric(
            label="Annual Generation",
            value=f"{calc['yearly_generation']:,.0f} units",
            help="Expected annual electricity generation"
        )

    # Financial Benefits
    st.markdown('''
    <div class="icon-header">
        <i class="fas fa-coins money-icon"></i>
        <h2 class="sub-header" style="margin: 0;">Financial Benefits</h2>
    </div>
    ''', unsafe_allow_html=True)

    if investment_model == "CAPEX":
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="System Cost",
                value=f"₹{calc['investment']:,.0f}",
                help="Total investment required (CAPEX)"
            )

        with col2:
            st.metric(
                label="Annual Savings",
                value=f"₹{calc['annual_savings']:,.0f}",
                help="Expected annual electricity bill savings"
            )

        with col3:
            st.metric(
                label="Payback Period",
                value=f"{calc['payback_period']:.1f} years",
                help="Time to recover your investment"
            )

        with col4:
            st.metric(
                label="25-Year Total Savings",
                value=f"₹{calc['lifetime_savings']:,.0f}",
                help="Total savings over 25 years"
            )
    else:
        # OPEX model - only show savings
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Monthly Savings",
                value=f"₹{calc['monthly_savings']:,.0f}",
                help="Expected monthly electricity bill savings"
            )

        with col2:
            st.metric(
                label="Annual Savings",
                value=f"₹{calc['annual_savings']:,.0f}",
                help="Expected annual electricity bill savings"
            )

        with col3:
            st.metric(
                label="25-Year Total Savings",
                value=f"₹{calc['lifetime_savings']:,.0f}",
                help="Total savings over 25 years"
            )

    # Environmental Impact
    st.markdown('''
    <div class="icon-header">
        <i class="fas fa-leaf eco-icon"></i>
        <h2 class="sub-header" style="margin: 0;">Environmental Impact</h2>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="CO₂ Saved per Year",
            value=f"{calc['annual_co2_saved']:.1f} tons",
            help="Annual CO₂ emission reduction"
        )

    with col2:
        st.metric(
            label="25-Year CO₂ Saved",
            value=f"{calc['lifetime_co2_saved']:.1f} tons",
            help="Total CO₂ emission reduction over 25 years"
        )

    with col3:
        st.metric(
            label="Equivalent Trees Planted",
            value=f"{calc['equivalent_trees']:.0f} trees",
            help="Equivalent environmental impact in trees planted"
        )

def show_sample_benefits():
    """Show sample benefits for different bill amounts"""
    st.markdown('''
    <div class="icon-header">
        <i class="fas fa-coins money-icon"></i>
        <h2 class="sub-header" style="margin: 0;">Sample Benefits by Bill Amount</h2>
    </div>
    ''', unsafe_allow_html=True)

    calculator = SolarCalculator()
    sample_bills = [5000, 25000, 100000, 500000, 1000000]
    sample_data = []

    for bill in sample_bills:
        analysis = calculator.get_comprehensive_analysis(
            monthly_bill=bill,
            tariff_rate=8.0,
            investment_model="CAPEX"
        )
        calc = analysis["calculations"]

        sample_data.append({
            "Monthly Bill (₹)": f"₹{bill:,}",
            "System Size (kWp)": f"{calc['plant_capacity']:.1f}",
            "Investment (₹)": f"₹{calc['investment']:,.0f}",
            "Annual Savings (₹)": f"₹{calc['annual_savings']:,.0f}",
            "Payback (Years)": f"{calc['payback_period']:.1f}"
        })

    df = pd.DataFrame(sample_data)
    st.dataframe(df, hide_index=True, use_container_width=True)

if __name__ == "__main__":
    main()

