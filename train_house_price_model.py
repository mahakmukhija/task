import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="🏠 House Price Trainer", layout="centered")
st.title("🏠 Train a Model to Predict House Prices Based on Area")

# Step 1: Create dataset
data = {
    'Area': [500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000],
    'Price': [1500000, 2200000, 3000000, 3500000, 4200000, 4800000, 5500000, 6000000, 6700000, 8000000]
}
df = pd.DataFrame(data)

st.subheader("📊 Sample Dataset")
st.dataframe(df)

# Step 2: Prepare features and target
X = df[['Area']]  # Independent variable
y = df['Price']   # Dependent variable

# Step 3: Train model
model = LinearRegression()
model.fit(X, y)

# Step 4: Show results
st.subheader("📈 Trained Model Parameters")
st.write(f"**Coefficient (₹ per sq ft):** {model.coef_[0]:,.2f}")
st.write(f"**Intercept (₹):** {model.intercept_:,.2f}")

# Optional: Prediction preview
st.subheader("🏡 Predict Price for Given Area")
area_input = st.number_input("Enter Area (sq ft):", min_value=100, max_value=10000, value=1500, step=100)

if st.button("Predict Price"):
    price_pred = model.predict([[area_input]])[0]
    st.success(f"💰 Estimated House Price: ₹{price_pred:,.2f}")
