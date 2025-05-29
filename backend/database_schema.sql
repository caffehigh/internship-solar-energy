-- Solar Plant Calculator Database Schema for Supabase

-- Table for storing user calculations
CREATE TABLE solar_calculations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- User Input Data
    location_city TEXT NOT NULL,
    location_state TEXT,
    location_country TEXT DEFAULT 'India',
    monthly_bill DECIMAL(12,2) NOT NULL,
    monthly_consumption DECIMAL(10,2),
    investment_model TEXT CHECK (investment_model IN ('CAPEX', 'OPEX')) NOT NULL,
    consumer_type TEXT CHECK (consumer_type IN ('Residential', 'Commercial', 'Industrial')) NOT NULL,
    consumer_category TEXT NOT NULL,
    installation_type TEXT CHECK (installation_type IN ('Rooftop', 'Ground-mounted')) NOT NULL,
    shadow_free_area BOOLEAN DEFAULT true,
    rooftop_area DECIMAL(8,2),
    tariff_rate DECIMAL(6,2) NOT NULL,
    
    -- Solar Data (fetched from Global Solar Atlas)
    solar_irradiance DECIMAL(5,2),
    ghi_annual DECIMAL(6,2),
    dni_annual DECIMAL(6,2),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    
    -- Calculated Results
    plant_capacity DECIMAL(10,2),
    monthly_generation DECIMAL(10,2),
    yearly_generation DECIMAL(12,2),
    investment_amount DECIMAL(15,2),
    monthly_savings DECIMAL(10,2),
    annual_savings DECIMAL(12,2),
    lifetime_savings DECIMAL(15,2),
    payback_period DECIMAL(5,2),
    co2_saved_annual DECIMAL(8,2),
    co2_saved_lifetime DECIMAL(10,2),
    equivalent_trees DECIMAL(8,0),
    
    -- System Specifications
    panel_count INTEGER,
    inverter_capacity DECIMAL(8,2),
    estimated_area_required DECIMAL(8,2),
    
    -- Additional Metadata
    calculation_version TEXT DEFAULT '1.0',
    user_ip TEXT,
    user_agent TEXT
);

-- Table for storing location data and solar irradiance
CREATE TABLE location_solar_data (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    country TEXT DEFAULT 'India',
    latitude DECIMAL(10,6) NOT NULL,
    longitude DECIMAL(10,6) NOT NULL,
    ghi_annual DECIMAL(6,2), -- Global Horizontal Irradiance
    dni_annual DECIMAL(6,2), -- Direct Normal Irradiance
    avg_irradiance DECIMAL(5,2),
    default_tariff DECIMAL(6,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(city, state, country)
);

-- Table for consumer categories
CREATE TABLE consumer_categories (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    category_code TEXT UNIQUE NOT NULL,
    category_name TEXT NOT NULL,
    voltage_level TEXT CHECK (voltage_level IN ('LT', 'HT')) NOT NULL,
    consumer_type TEXT CHECK (consumer_type IN ('Residential', 'Commercial', 'Industrial')) NOT NULL,
    typical_tariff_range_min DECIMAL(6,2),
    typical_tariff_range_max DECIMAL(6,2),
    description TEXT
);

-- Insert consumer categories
INSERT INTO consumer_categories (category_code, category_name, voltage_level, consumer_type, typical_tariff_range_min, typical_tariff_range_max, description) VALUES
-- LT Categories
('LT-1A', 'Domestic (0-100 units)', 'LT', 'Residential', 2.50, 4.00, 'Residential consumers with monthly consumption 0-100 units'),
('LT-1B', 'Domestic (101-300 units)', 'LT', 'Residential', 4.00, 6.50, 'Residential consumers with monthly consumption 101-300 units'),
('LT-1C', 'Domestic (Above 300 units)', 'LT', 'Residential', 6.50, 9.00, 'Residential consumers with monthly consumption above 300 units'),
('LT-2A', 'Non-Domestic (Commercial)', 'LT', 'Commercial', 7.00, 10.00, 'Commercial establishments, shops, offices'),
('LT-2B', 'Non-Domestic (Small Industries)', 'LT', 'Commercial', 8.00, 11.00, 'Small scale industries and manufacturing'),
('LT-3', 'Agricultural', 'LT', 'Commercial', 1.50, 3.00, 'Agricultural and farming activities'),
('LT-4', 'Street Lighting', 'LT', 'Commercial', 6.00, 8.00, 'Municipal street lighting'),
('LT-5', 'Temporary Supply', 'LT', 'Commercial', 10.00, 15.00, 'Temporary connections for events, construction'),

-- HT Categories  
('HT-1', 'Industrial (General)', 'HT', 'Industrial', 6.00, 9.00, 'General industrial consumers'),
('HT-2', 'Industrial (Continuous Process)', 'HT', 'Industrial', 5.50, 8.50, 'Industries with continuous manufacturing process'),
('HT-3', 'Commercial (Large)', 'HT', 'Commercial', 8.00, 12.00, 'Large commercial establishments, malls, hospitals'),
('HT-4', 'Railway Traction', 'HT', 'Commercial', 4.00, 6.00, 'Railway electrification and traction'),
('HT-5', 'Bulk Supply', 'HT', 'Industrial', 5.00, 7.50, 'Bulk power supply to large consumers'),
('HT-6', 'Public Lighting', 'HT', 'Commercial', 7.00, 9.00, 'Public infrastructure lighting'),
('HT-7', 'Mixed Load', 'HT', 'Commercial', 7.50, 10.50, 'Mixed commercial and residential complexes');

-- Insert sample location data (major Indian cities)
INSERT INTO location_solar_data (city, state, latitude, longitude, ghi_annual, dni_annual, avg_irradiance, default_tariff) VALUES
('Mumbai', 'Maharashtra', 19.0760, 72.8777, 1825, 1650, 5.0, 7.2),
('Delhi', 'Delhi', 28.7041, 77.1025, 1750, 1580, 4.8, 6.5),
('Bangalore', 'Karnataka', 12.9716, 77.5946, 1900, 1720, 5.2, 5.8),
('Chennai', 'Tamil Nadu', 13.0827, 80.2707, 1950, 1780, 5.3, 4.5),
('Hyderabad', 'Telangana', 17.3850, 78.4867, 1875, 1700, 5.1, 6.8),
('Pune', 'Maharashtra', 18.5204, 73.8567, 1850, 1680, 5.1, 7.0),
('Kolkata', 'West Bengal', 22.5726, 88.3639, 1650, 1480, 4.5, 6.2),
('Ahmedabad', 'Gujarat', 23.0225, 72.5714, 2000, 1850, 5.5, 5.5),
('Jaipur', 'Rajasthan', 26.9124, 75.7873, 2100, 1950, 5.8, 5.2),
('Surat', 'Gujarat', 21.1702, 72.8311, 1975, 1800, 5.4, 5.5),
('Lucknow', 'Uttar Pradesh', 26.8467, 80.9462, 1800, 1620, 4.9, 5.8),
('Kanpur', 'Uttar Pradesh', 26.4499, 80.3319, 1780, 1600, 4.9, 5.8),
('Nagpur', 'Maharashtra', 21.1458, 79.0882, 1900, 1720, 5.2, 7.0),
('Indore', 'Madhya Pradesh', 22.7196, 75.8577, 1925, 1750, 5.3, 6.0),
('Thane', 'Maharashtra', 19.2183, 72.9781, 1825, 1650, 5.0, 7.2),
('Bhopal', 'Madhya Pradesh', 23.2599, 77.4126, 1875, 1700, 5.1, 6.0),
('Visakhapatnam', 'Andhra Pradesh', 17.6868, 83.2185, 1850, 1680, 5.1, 6.5),
('Pimpri-Chinchwad', 'Maharashtra', 18.6298, 73.7997, 1850, 1680, 5.1, 7.0),
('Patna', 'Bihar', 25.5941, 85.1376, 1750, 1580, 4.8, 5.5),
('Vadodara', 'Gujarat', 22.3072, 73.1812, 1950, 1780, 5.3, 5.5),
('Pen', 'Maharashtra', 18.7373, 73.0982, 1825, 1650, 5.0, 7.0);

-- Create indexes for better performance
CREATE INDEX idx_solar_calculations_created_at ON solar_calculations(created_at);
CREATE INDEX idx_solar_calculations_location ON solar_calculations(location_city, location_state);
CREATE INDEX idx_location_solar_data_city_state ON location_solar_data(city, state);
CREATE INDEX idx_consumer_categories_type ON consumer_categories(consumer_type, voltage_level);

-- Enable Row Level Security (RLS)
ALTER TABLE solar_calculations ENABLE ROW LEVEL SECURITY;
ALTER TABLE location_solar_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE consumer_categories ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (since this is a calculator app)
CREATE POLICY "Allow public read access" ON location_solar_data FOR SELECT USING (true);
CREATE POLICY "Allow public read access" ON consumer_categories FOR SELECT USING (true);
CREATE POLICY "Allow public insert" ON solar_calculations FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public read own calculations" ON solar_calculations FOR SELECT USING (true);
