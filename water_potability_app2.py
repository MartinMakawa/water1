import pandas as pd
import streamlit as st
import joblib

# Load the trained Random Forest model
model=joblib.load('random_forest_original_model.joblib')
    

# Define WHO ranges for specific parameters (example values, replace with accurate ranges)
WHO_RANGES = {
    'ph': (6.5, 8.5),
    'Solids': (250, 600),
    'Chloramines': (0, 4),
    'Sulfate': (100, 500),
    'Conductivity': (0, 400),
    'Trihalomethanes': (0.08, 0.1),
    'Turbidity': (0, 5),
    'Hardness': (60, 120),  # Example range for Hardness, adjust as necessary
    'Organic_carbon': (0, 4)  # Example range for Organic Carbon, adjust as necessary
}

# Function to check if parameter values are within WHO ranges
def check_ranges(sample):
    out_of_range = []
    for param, (low, high) in WHO_RANGES.items():
        if param in sample and not (low <= sample[param] <= high):
            out_of_range.append(param)
    return out_of_range

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Landing Page", "Prediction Page"])

# Landing Page
if page == "Landing Page":
    # Display logo
    st.image("LOGO.png", width=300)  # Adjust width as needed

    st.title("Welcome to the Water Quality Prediction App")

    # Developer names
    st.write("Developed by **Martin Makawa** and **Blessings Nyirenda**")

    st.write("""This app predicts whether water is potable or not based on your water quality parameters. Use the **Prediction Page** to interact with the model and see the predictions in real-time.""")

# Prediction Page
elif page == "Prediction Page":
    st.title("Water Potability Prediction")
    st.subheader("Enter Water Quality Parameters:")

    # Arrange input fields in a grid layout
    col1, col2, col3 = st.columns(3)

    sample_input = {}

    with col1:
        sample_input['ph'] = st.number_input("pH Level", min_value=0.0, max_value=14.0, step=0.1)
        sample_input['Hardness'] = st.number_input("Hardness", min_value=0.0, step=0.1)
        sample_input['Solids'] = st.number_input("Solids", min_value=0.0, step=0.1)
        
       
    with col2:
        sample_input['Chloramines'] = st.number_input("Chloramines", min_value=0.0, step=0.1)
        sample_input['Sulfate'] = st.number_input("Sulfate", min_value=0.0, step=0.1)
        sample_input['Conductivity'] = st.number_input("Conductivity", min_value=0.0, step=0.1)
       
       
    with col3:
        sample_input['Organic_carbon'] = st.number_input("Organic Carbon", min_value=0.0, step=0.1)
        sample_input['Trihalomethanes'] = st.number_input("Trihalomethanes", min_value=0.0, step=0.1)
        sample_input['Turbidity'] = st.number_input("Turbidity", min_value=0.0, step=0.1)

    # Convert input to DataFrame for prediction
    sample_df = pd.DataFrame([sample_input])

    # Make prediction when the button is clicked
    if st.button("Predict Potability"):
        # Get prediction probabilities
        prediction_proba = model.predict_proba(sample_df)[0]
        not_potable_confidence = prediction_proba[0] * 100
        potable_confidence = prediction_proba[1] * 100

        # Determine prediction and format confidence message
        if potable_confidence > not_potable_confidence:
            pred_class = "potable"
            confidence = potable_confidence
        else:
            pred_class = "not potable"
            confidence = not_potable_confidence

        # Check WHO compliance
        out_of_range_params = check_ranges(sample_input)

        # Display prediction with confidence level
        st.write(f"This water sample is likely **{pred_class}** with a confidence level of **{confidence:.2f}%**.")
        
        # Display out-of-range parameters, if any
        if out_of_range_params:
            out_of_range_message = ", ".join(out_of_range_params)
            st.write(f"And, the following parameters are outside WHO-recommended ranges for potable water: {out_of_range_message}.")
        else:
            st.write("All parameters are within WHO-recommended ranges for potable water.")
