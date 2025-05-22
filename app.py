import streamlit as st
import pandas as pd
import numpy as np
import joblib

# trained model
model = joblib.load("RandomForestRegressor.pkl")

# maps
neighborhood_map = {
    12: 'Bloomington Heights', 2: 'Briardale', 13: 'Brookside', 14: 'Clear Creek',
    16: 'College Creek', 15: 'Crawford', 4: 'Edwards', 11: 'Gilbert',
    1: 'Iowa DOT and Rail Road', 0: 'Meadow Village', 9: 'Mitchell',
    8: 'North Ames', 23: 'Northridge', 7: 'Northpark Villa', 21: 'Northridge Heights',
    20: 'Northwest Ames', 3: 'Old Town', 6: 'South & West of Iowa State University',
    5: 'Sawyer', 10: 'Sawyer West', 19: 'Somerset', 22: 'Stone Brook',
    17: 'Timberland', 18: 'Veenker'
}
neighborhood_reverse = {v: k for k, v in neighborhood_map.items()}

mszoning_map = {
    4: 'Floating Village Residential',
    1: 'Residential High Density',
    3: 'Residential Low Density',
    2: 'Residential Medium Density',
    0: 'Others'
}
mszoning_reverse = {v: k for k, v in mszoning_map.items()}

# UI
st.set_page_config(page_title="House Price Predictor", layout="centered")
st.title("🏠 House Price Prediction Model")

# Information About Model
with st.expander("Information about Model", expanded=False):
    st.markdown("""
    ## House Price Prediction Model
    This project uses a machine learning model [(Random Forest Regressor)](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html) to predict house prices based on various features you provide.

    ### Features Used:
    | Feature             | Description |
    |---------------------|-------------|
    | **MS Zoning**       | Type of residential zoning classification (Low, Medium, High Density) |
    | **Neighborhood**    | The area or locality where the house is located |
    | **Garage Cars**     | Number of cars the garage can hold |
    | **Total Usable Area** | Livable square footage of the house |
    | **Overall Rating**  | A quality score for the house (1 to 10) |
    | **Year Built**      | The year the house was originally built |
    | **Remodeled Age**   | How many years ago the house was remodeled |
    | **Total Rooms**     | Total number of rooms above ground |

    ### How the Model Works:
    - **Training:** Trained on real-world home sales [dataset.](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques)
    - **Encoding:** Categorical values like Zoning/Neighborhood converted using Label Encoding
    - **Prediction:** User inputs are transformed into the training format, and the model predicts based on patterns it learned

    ### Technologies Used:
    - Python
    - Scikit-learn (Random Forest Regressor)
    - Streamlit (Web App Interface)
    - Joblib (Model loading)
    
    [Read more about the project on GitHub](https://github.com/vishwjeet71/house-price-prediction-model)
    """)

# Inputs Section
st.header("Enter House Details Below")

mszoning_display = st.selectbox("MS Zoning", list(mszoning_map.values()))
neighborhood_display = st.selectbox("Neighborhood", list(neighborhood_map.values()))
garage_cars = st.slider("Garage Cars", 0, 5, 1)
total_usable_area = st.number_input("Total Usable Area (sq ft)", min_value=100, max_value=10000, value=400)
overall_rating = st.slider("Overall Rating (1 - 10)", 1, 10, 3)
year_built = st.number_input("Year Built", min_value=1800, max_value=2024, value=1910)
remod_age = st.slider("Remodel Age (years ago)", 0, 200, 150)
total_rms = st.slider("Total Rooms", 1, 20, 5)

# Convert display values to model values
mszoning = mszoning_reverse[mszoning_display]
neighborhood = neighborhood_reverse[neighborhood_display]

# Prepare input
input_data = np.array([[mszoning, neighborhood, garage_cars, total_usable_area,
                        overall_rating, year_built, remod_age, total_rms]])

# Prediction
if st.button("Predict House Price"):
    prediction = model.predict(input_data)[0]
    st.success(f"🏡 Estimated House Price: ${int(prediction):,}")

