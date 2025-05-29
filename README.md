# ☀️ Solar Plant Financial Calculator v2.0

A comprehensive form-based web application that helps users calculate potential savings, system requirements, and environmental impact from installing solar panels. Built with Flask and enhanced with backend storage capabilities.

## 🚀 What's New in Version 2.0

### ✨ Major Enhancements
- **Complete UI Redesign**: Professional form-based interface with Bootstrap 5
- **Enhanced Calculations**: Precise formulas based on your specifications
- **Backend Integration**: Supabase database for data storage and analytics
- **Smart Pricing**: Consumer type and system size-specific pricing matrix
- **PDF Reports**: Professional downloadable reports with comprehensive analysis
- **Personalized Recommendations**: AI-driven suggestions based on calculations

### 🎯 Core Features

#### Comprehensive Input Form
- **Location Selection**: 100+ Indian cities with Global Solar Atlas integration
- **Bill Processing**: OCR support for automatic data extraction from uploaded bills
- **Consumer Details**: Residential/Commercial/Industrial with category selection
- **Installation Options**: Rooftop/Ground-mounted with shadow analysis
- **Investment Models**: CAPEX (purchase) vs OPEX (lease/PPA) analysis

#### Advanced Calculations
- **Precise Formulas**: Plant Capacity = Monthly Consumption ÷ (Irradiance × PR × 30)
- **Smart Pricing Matrix**: Dynamic cost per kW based on consumer type and system size
- **Financial Analysis**: ROI, payback period, lifetime savings with 25-year projections
- **Environmental Impact**: CO₂ reduction and equivalent trees planted calculations
- **System Specifications**: Panel count, inverter capacity, area requirements

#### Professional Results Dashboard
- **Visual Metrics**: Clean cards showing key performance indicators
- **Detailed Breakdown**: System specs, generation, financial, and environmental data
- **Recommendations**: Personalized suggestions based on calculation results
- **Download Reports**: PDF generation with comprehensive analysis

## 🛠️ Technology Stack

### Frontend
- **Framework**: Flask with Jinja2 templates
- **Styling**: Bootstrap 5 with custom CSS
- **Icons**: Font Awesome 6
- **Forms**: WTForms with Flask-WTF integration
- **Responsive**: Mobile-first design approach

### Backend
- **Language**: Python 3.12+
- **Framework**: Flask with CORS support
- **Database**: Supabase (PostgreSQL) with real-time features
- **File Processing**: OCR with PyTesseract and PIL
- **PDF Generation**: ReportLab for professional reports
- **Data Processing**: Pandas and NumPy for calculations

### Integrations
- **Supabase**: Backend-as-a-Service for data storage and analytics
- **Global Solar Atlas**: Enhanced solar irradiance data (optional)
- **OCR Processing**: Automatic bill data extraction
- **Cloud Storage**: Secure data persistence and retrieval

## 📦 Quick Start

### Demo Version (No Setup Required)
```bash
# Clone the repository
git clone https://github.com/caffehigh/internship-solar-energy.git
cd internship-solar-energy

# Install dependencies
pip install flask flask-cors python-dotenv wtforms flask-wtf reportlab

# Run demo application
python demo_app.py
```

Access the demo at: `http://localhost:5000`

### Full Version with Supabase Backend

1. **Setup Supabase Project**:
   - Create account at [supabase.com](https://supabase.com)
   - Create new project and note the URL and anon key
   - Run the SQL schema from `backend/database_schema.sql`

2. **Configure Environment**:
   ```bash
   # Copy and edit environment file
   cp .env.example .env
   # Add your Supabase credentials to .env
   ```

3. **Install All Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Full Application**:
   ```bash
   python solar_app.py
   ```

## 🚀 Usage Guide

### Step 1: Input Your Details
- **Location**: Select your city from 100+ Indian cities
- **Monthly Bill**: Enter your electricity bill amount (₹100 - ₹25,00,000)
- **Consumption**: Optional - will be calculated if not provided
- **Upload Bill**: Optional OCR processing for automatic data extraction

### Step 2: Configure Options
- **Investment Model**: Choose CAPEX (purchase) or OPEX (lease/PPA)
- **Consumer Type**: Residential, Commercial, or Industrial
- **Installation**: Rooftop or Ground-mounted
- **Area**: Optional rooftop area for validation

### Step 3: Get Results
- **System Specifications**: Capacity, panels, inverter, area requirements
- **Financial Analysis**: Investment, savings, payback period, ROI
- **Environmental Impact**: CO₂ reduction and equivalent trees
- **Recommendations**: Personalized suggestions based on your data

### Step 4: Download Report
- **PDF Generation**: Comprehensive analysis report (Full version only)
- **Data Storage**: Calculations saved for future reference (Full version only)

## 📊 Enhanced Calculation Methodology

### Core Formulas (Your Specifications)
```
1. Plant Capacity (kW) = Monthly Consumption / (Avg Irradiance × PR × 30)
2. Investment (CAPEX) = Capacity × Cost per kW
3. Monthly Generation = Capacity × Avg Irradiance × PR × 30
4. Yearly Generation = Monthly Generation × 12
5. Savings/year = Yearly Generation × Tariff
6. Payback = Investment / Annual Savings
7. CO₂ Saved = Yearly Generation × 0.8 (kg CO₂/unit)
```

### Smart Pricing Matrix
| Consumer Type | System Size | Cost per kW |
|---------------|-------------|-------------|
| **Residential** | < 5 kW | ₹80,000 |
| | 5-10 kW | ₹78,000 |
| | > 10 kW | ₹76,000 |
| **Commercial** | < 50 kW | ₹75,000 |
| | 50-100 kW | ₹72,000 |
| | > 100 kW | ₹70,000 |
| **Industrial** | < 100 kW | ₹70,000 |
| | 100-500 kW | ₹68,000 |
| | > 500 kW | ₹65,000 |

### Key Assumptions
- **Performance Ratio (PR)**: 75%
- **System Lifetime**: 25 years
- **CO₂ Factor**: 0.8 kg per kWh
- **Panel Efficiency**: 400W per panel
- **Space Requirement**: ~8 sq ft per kW

### Formulas Used
- **Monthly Units** = Bill Amount ÷ Tariff Rate
- **Required Capacity** = Monthly Units ÷ (30 × 4)
- **System Cost** = Capacity × Cost per kWp × User Type Multiplier
- **Annual Savings** = Monthly Savings × 12
- **Payback Period** = System Cost ÷ Annual Savings
- **CO₂ Saved** = Yearly Generation × 0.8 kg/unit

## 📁 Project Structure

```
solar-plant-calculator/
├── demo_app.py                    # Demo Flask application (no backend required)
├── solar_app.py                   # Full Flask application with Supabase
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .env                          # Environment variables (create from example)
├── templates/                    # HTML templates
│   ├── base.html                 # Base template with Bootstrap 5
│   ├── index.html                # Main form page
│   ├── results.html              # Results dashboard
│   └── demo_info.html            # Demo information page
├── backend/                      # Backend modules
│   ├── database_schema.sql       # Supabase database schema
│   ├── supabase_client.py        # Database operations
│   ├── solar_data_fetcher.py     # Enhanced solar data with API integration
│   └── report_generator.py       # PDF report generation
├── utils/                        # Utility modules
│   ├── calculations.py           # Enhanced calculation logic
│   ├── location_data.py          # Indian cities with solar data
│   └── ocr_processor.py          # OCR functionality for bills
└── README.md                     # Project documentation
```

## 🌍 Enhanced Location Data

The application includes comprehensive data for 100+ Indian cities:
- **Solar Irradiance**: Location-specific kWh/m²/day values
- **Electricity Tariffs**: State-wise average rates
- **Coordinates**: Latitude/longitude for API integration
- **Climate Zones**: Hot-Dry, Hot-Humid, Temperate, Composite
- **Seasonal Variations**: Monthly irradiance patterns

## 🔧 API Integrations

### Global Solar Atlas (Optional)
- Enhanced solar irradiance data
- GHI (Global Horizontal Irradiance) values
- DNI (Direct Normal Irradiance) values
- Weather impact factors

### Supabase Backend
- Real-time data storage
- Analytics and reporting
- User calculation history
- Location data management

## 🤝 Contributing & Development

This is an internship project. Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Development Setup
```bash
# Clone and setup
git clone https://github.com/caffehigh/internship-solar-energy.git
cd internship-solar-energy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run demo version
python demo_app.py
```

## 📈 Sample Results

### Residential Example (₹5,000/month bill)
- **System Size**: 3.7 kWp
- **Investment**: ₹2,96,000 (CAPEX)
- **Annual Savings**: ₹60,000
- **Payback Period**: 4.9 years
- **25-Year Savings**: ₹15,00,000
- **CO₂ Reduction**: 3.6 tons/year

### Commercial Example (₹1,00,000/month bill)
- **System Size**: 74.1 kWp
- **Investment**: ₹51,87,000 (CAPEX)
- **Annual Savings**: ₹12,00,000
- **Payback Period**: 4.3 years
- **25-Year Savings**: ₹3,00,00,000
- **CO₂ Reduction**: 71.0 tons/year

## 🔮 Future Enhancements

- **Mobile App**: React Native application
- **Advanced Analytics**: Machine learning predictions
- **IoT Integration**: Real-time system monitoring
- **Multi-language Support**: Regional language options
- **Government Schemes**: Integration with subsidy programs
- **Financing Options**: Loan and EMI calculators

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Caffehigh** - [GitHub Profile](https://github.com/caffehigh)

## 🙏 Acknowledgments

- Global Solar Atlas for solar irradiance data
- Supabase for backend infrastructure
- Bootstrap team for UI components
- Flask community for web framework
- All contributors and testers

---

**⚡ Start calculating your solar savings today!**

Visit the demo at: `http://localhost:5000` after running `python demo_app.py`
3. Make your changes
4. Submit a pull request

## 📄 License

This project is developed as part of an internship program. License information will be updated as needed.

## 🔮 Future Enhancements

- Real-time electricity tariff API integration
- Advanced OCR with multiple bill format support
- Solar panel brand and efficiency comparisons
- Government subsidy calculations
- Mobile-responsive design
- Multi-language support
