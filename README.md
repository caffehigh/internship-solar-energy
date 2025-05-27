# ☀️ Solar Benefit Calculator

A comprehensive Python web application built with Streamlit that helps users calculate potential savings from installing solar panels based on their electricity usage and location.

## 🎯 Features

### User Input Section
- **Monthly Electricity Bill Input** with OCR support for PDF/image upload
- **Location Selection** from 100+ Indian cities with location-specific data
- **Optional Parameters**: Tariff rate, rooftop area, user type (Residential/Commercial/Industrial)

### Advanced Calculations
- Solar generation potential based on location-specific irradiance data
- System sizing recommendations (kWp capacity)
- Cost estimation with user-type specific pricing
- Monthly and annual savings calculations
- Payback period analysis
- CO₂ emission reduction calculations
- ROI percentage and lifetime savings

### Interactive Visualizations
- Cumulative savings over 25-year system lifetime
- Monthly bill breakdown charts
- Environmental impact metrics
- Sample benefits comparison table

### OCR Integration
- Upload electricity bills (PDF/Image) for automatic data extraction
- Smart text parsing to extract bill amounts and units
- Data validation and suggestions

## 🛠️ Technologies Used

- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Python with modular architecture
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly (interactive charts)
- **OCR**: PyTesseract, PIL, PyPDF2
- **Data**: Comprehensive Indian city database with solar irradiance and tariff data

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/caffehigh/internship-solar-energy.git
   cd internship-solar-energy
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Access the app**: Open your browser and go to `http://localhost:8501`

## 🚀 Usage

1. **Upload Bill (Optional)**: Upload your electricity bill PDF/image for automatic data extraction
2. **Enter Details**: Input your monthly bill amount and select your city
3. **Configure Options**: Set tariff rate, rooftop area, and user type
4. **Calculate**: Click "Calculate Solar Benefits" to get comprehensive analysis
5. **Review Results**: Analyze savings, payback period, and environmental impact

## 📊 Calculation Methodology

### Key Assumptions
- **Solar Generation**: 4 units per kWp per day
- **System Cost**: ₹76,000 - ₹80,000 per kWp
- **System Lifetime**: 25 years
- **CO₂ Factor**: 0.8 kg per unit

### Formulas Used
- **Monthly Units** = Bill Amount ÷ Tariff Rate
- **Required Capacity** = Monthly Units ÷ (30 × 4)
- **System Cost** = Capacity × Cost per kWp × User Type Multiplier
- **Annual Savings** = Monthly Savings × 12
- **Payback Period** = System Cost ÷ Annual Savings
- **CO₂ Saved** = Yearly Generation × 0.8 kg/unit

## 🏗️ Project Structure

```
internship-solar-energy/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── utils/
│   ├── calculations.py    # Solar calculation logic
│   ├── location_data.py   # Indian cities with solar data
│   └── ocr_processor.py   # OCR functionality for bills
├── README.md             # Project documentation
└── .gitignore           # Git ignore rules
```

## 🌍 Supported Locations

The application includes data for 100+ Indian cities with:
- Location-specific solar irradiance values
- Average electricity tariff rates
- State-wise categorization

## 🤝 Contributing

This is an internship project. Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
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
