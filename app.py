import streamlit as st
import joblib
import pandas as pd

# --- 1. Load the Trained Model ---
# The model was saved as 'gradient_boosting_model.joblib'
# Ensure this file is accessible by your Streamlit app (e.g., in the same directory)
try:
    model = joblib.load('gradient_boosting_model.joblib')
except FileNotFoundError:
    st.error("Error: 'gradient_boosting_model.joblib' not found. Please ensure the model file is in the correct directory.")
    st.stop()

# --- 2. Define Features ---
# These are the 15 features used to train the model
feature_columns = [
    'Region', 
    'Province', 
    'Family Size', 
    'Salaries/Wages from Regular Employment',
    'Salaries/Wages from Seasonal Employment',
    'Net Share of Crops, Fruits, etc. (Tot. Net Value of Share)',
    'Cash Receipts, Support, etc. from Abroad',
    'Cash Receipts, Support, etc. from Domestic Source',
    'Rentals Received from Non-Agri Lands, etc.',
    'Pension and Retirement Benefits',
    'Dividends from Investment',
    'Other Sources of Income NEC',
    'Family Sustenance Activities',
    'Transportation, Storage Services',
    'Hhld, Income from Entrepreneurial Activities, Total'
]

# --- 3. Streamlit App Interface ---
st.set_page_config(page_title="Income Predictor", layout="wide")
st.title("Household Income Prediction")
st.write("Enter the details below to predict the 'Income from Salaries and Wages'.")

# Create input fields for each feature
input_data = {}

# Organize inputs into columns for better layout
col1, col2, col3 = st.columns(3)

with col1:
    st.header("General Information")
    input_data['Region'] = st.number_input('Region', min_value=1, max_value=17, value=1, step=1)
    input_data['Province'] = st.number_input('Province', min_value=1, max_value=81, value=28, step=1)
    input_data['Family Size'] = st.number_input('Family Size (Total Individuals)', min_value=1.0, value=3.0, step=0.5)

with col2:
    st.header("Salaries & Wages")
    input_data['Salaries/Wages from Regular Employment'] = st.number_input('Salaries/Wages from Regular Employment', min_value=0, value=50000, step=1000)
    input_data['Salaries/Wages from Seasonal Employment'] = st.number_input('Salaries/Wages from Seasonal Employment', min_value=0, value=5000, step=1000)
    input_data['Net Share of Crops, Fruits, etc. (Tot. Net Value of Share)'] = st.number_input('Net Share of Crops, Fruits, etc.', min_value=0, value=0, step=1000)

with col3:
    st.header("Other Income Sources")
    input_data['Cash Receipts, Support, etc. from Abroad'] = st.number_input('Cash Receipts, Support, etc. from Abroad', min_value=0, value=0, step=1000)
    input_data['Cash Receipts, Support, etc. from Domestic Source'] = st.number_input('Cash Receipts, Support, etc. from Domestic Source', min_value=0, value=0, step=1000)
    input_data['Rentals Received from Non-Agri Lands, etc.'] = st.number_input('Rentals Received from Non-Agri Lands, etc.', min_value=0, value=0, step=100)

col4, col5, col6 = st.columns(3)

with col4:
    input_data['Pension and Retirement Benefits'] = st.number_input('Pension and Retirement Benefits', min_value=0, value=0, step=1000)
    input_data['Dividends from Investment'] = st.number_input('Dividends from Investment', min_value=0, value=0, step=100)
    input_data['Other Sources of Income NEC'] = st.number_input('Other Sources of Income NEC', min_value=0, value=0, step=100)

with col5:
    input_data['Family Sustenance Activities'] = st.number_input('Family Sustenance Activities', min_value=0, value=0, step=1000)
    input_data['Transportation, Storage Services'] = st.number_input('Transportation, Storage Services', min_value=0.0, value=1500.0, step=10.0)
    input_data['Hhld, Income from Entrepreneurial Activities, Total'] = st.number_input('Hhld, Income from Entrepreneurial Activities, Total', min_value=0.0, value=2000.0, step=10.0)

# --- 4. Prediction Button ---
if st.button('Predict Income'):
    # Create a DataFrame from the input data
    input_df = pd.DataFrame([input_data])
    
    # Ensure the order of columns matches the training data
    input_df = input_df[feature_columns]
    
    # Make prediction
    prediction = model.predict(input_df)[0]
    
    st.success(f"Predicted Income from Salaries and Wages: ₱{prediction:,.2f}")
