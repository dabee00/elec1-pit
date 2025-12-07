import streamlit as st
import joblib
import pandas as pd

# Load the trained Linear Regression model
try:
    linear_model = joblib.load('linear_regression_model.joblib')
except FileNotFoundError:
    st.error("Error: 'linear_regression_model.joblib' not found. Please ensure the model file is in the same directory as app.py.")
    st.stop()

# Define a function to make predictions
def predict_income(features_dict):
    # Define the exact feature names and their order as used during training
    feature_names = [
        'Communication Expenditure',
        'Housing and water Expenditure',
        'Miscellaneous Goods and Services Expenditure',
        'Total Food Expenditure',
        'Transportation Expenditure',
        'Clothing, Footwear and Other Wear Expenditure',
        'Total Income from Entrepreneurial Acitivites',
        'Imputed House Rental Value',
        'Number of Airconditioner'
    ]
    # Convert the dictionary of features to a list in the correct order
    input_values = [features_dict[name] for name in feature_names]
    # Convert list to a DataFrame for prediction
    input_df = pd.DataFrame([input_values], columns=feature_names)
    prediction = linear_model.predict(input_df)[0]
    return prediction

# --- Streamlit App Layout ---
st.set_page_config(page_title="Household Income Predictor", layout="wide", page_icon="🏡")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stNumberInput input {
        border-radius: 5px;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .stInfo {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #bee5eb;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for inputs
st.sidebar.title("🏡 Input Parameters")
st.sidebar.markdown("Adjust the values below to input your household data for prediction.")

# Dictionary to store feature inputs
input_features = {}

st.sidebar.subheader("💰 Expenditure Details")
col1, col2 = st.sidebar.columns(2)
with col1:
    input_features['Communication Expenditure'] = st.number_input(
        'Communication Expenditure (e.g., internet, phone bills) in PHP',
        min_value=0.0, value=5000.0, step=100.0, format="%.2f",
        help="Enter the total amount spent on communication services per year."
    )
    input_features['Housing and water Expenditure'] = st.number_input(
        'Housing and Water Expenditure (rent, utilities) in PHP',
        min_value=0.0, value=30000.0, step=500.0, format="%.2f",
        help="Enter the total amount spent on housing and water utilities per year."
    )
    input_features['Miscellaneous Goods and Services Expenditure'] = st.number_input(
        'Miscellaneous Goods and Services Expenditure in PHP',
        min_value=0.0, value=10000.0, step=100.0, format="%.2f",
        help="Enter the total amount spent on various other goods and services per year."
    )
with col2:
    input_features['Total Food Expenditure'] = st.number_input(
        'Total Food Expenditure (groceries, dining out) in PHP',
        min_value=0.0, value=50000.0, step=500.0, format="%.2f",
        help="Enter the total amount spent on food items per year."
    )
    input_features['Transportation Expenditure'] = st.number_input(
        'Transportation Expenditure (fuel, fares, maintenance) in PHP',
        min_value=0.0, value=15000.0, step=100.0, format="%.2f",
        help="Enter the total amount spent on transportation per year."
    )
    input_features['Clothing, Footwear and Other Wear Expenditure'] = st.number_input(
        'Clothing, Footwear, and Other Wear Expenditure in PHP',
        min_value=0.0, value=7500.0, step=50.0, format="%.2f",
        help="Enter the total amount spent on clothing and footwear per year."
    )

st.sidebar.markdown("---")
st.sidebar.subheader("💼 Income and Housing")
col3, col4 = st.sidebar.columns(2)
with col3:
    input_features['Total Income from Entrepreneurial Acitivites'] = st.number_input(
        'Total Income from Entrepreneurial Activities (annual) in PHP',
        min_value=0.0, value=20000.0, step=500.0, format="%.2f",
        help="Enter the total annual income derived from entrepreneurial activities."
    )
with col4:
    input_features['Imputed House Rental Value'] = st.number_input(
        'Imputed House Rental Value (annual) in PHP',
        min_value=0.0, value=10000.0, step=100.0, format="%.2f",
        help="If the household owns the house, enter its estimated annual rental value. Enter 0 if renting."
    )

st.sidebar.markdown("---")
st.sidebar.subheader("🏠 Household Assets")
input_features['Number of Airconditioner'] = st.sidebar.number_input(
    'Number of Airconditioners (count)',
    min_value=0, max_value=10, value=0, step=1,
    help="Enter the total number of air conditioners in the household."
)

# Main area
st.title('🏡 Total Household Income Predictor')
st.markdown("""
    Welcome to the **Household Income Predictor**! This application uses a Linear Regression model to estimate a household's total income based on various expenditure and asset indicators.
    
    Use the sidebar to input your data, then click the button below to get a prediction.
""")

# Prediction button
if st.button('💰 Predict Total Household Income'):
    try:
        predicted_income = predict_income(input_features)
        st.success(f'**Predicted Total Household Income:** PHP {predicted_income:,.2f}')
        st.balloons()
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")

st.markdown("---")
st.info("This prediction is based on a Linear Regression model trained on specific socio-economic data. Results are indicative and should be used for reference only.")
