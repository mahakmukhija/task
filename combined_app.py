import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="ML Utility App", layout="centered")
st.title("🧠 ML Utility Dashboard")

# Sidebar navigation
menu = st.sidebar.radio("Choose Task", [
    "Train Salary Prediction Model",
    "Predict Salary",
    "Train House Price Model",
    "Predict House Price",
    "Missing Value Imputation"
])

# ---------- Option 1: Train Salary Prediction Model ----------
if menu == "Train Salary Prediction Model":
    st.header("Train Salary Prediction Model")

    use_sample = st.checkbox("Use sample data", value=True)
    if use_sample:
        data = pd.DataFrame({
            'Experience': [1, 2, 3, 4, 5, 6, 7],
            'Salary': [30000, 35000, 40000, 50000, 55000, 60000, 65000]
        })
        st.write(data)
    else:
        uploaded = st.file_uploader("Upload CSV with 'Experience' and 'Salary'", type="csv")
        if uploaded:
            data = pd.read_csv(uploaded)
            st.write(data)
        else:
            data = None

    if data is not None and 'Experience' in data.columns and 'Salary' in data.columns:
        if st.button("Train and Save Salary Model"):
            X = data[['Experience']]
            y = data['Salary']
            model = LinearRegression().fit(X, y)
            joblib.dump(model, 'salary_model.pkl')
            st.success("Model saved as `salary_model.pkl`")
            st.write(f"Coefficient: {model.coef_[0]:.2f}")
            st.write(f"Intercept: {model.intercept_:.2f}")

# ---------- Option 2: Predict Salary ----------
elif menu == "Predict Salary":
    st.header("Predict Salary")
    if not os.path.exists("salary_model.pkl"):
        st.warning("Model not found. Please train it first.")
    else:
        model = joblib.load('salary_model.pkl')
        exp = st.number_input("Enter years of experience", min_value=0.0, step=0.5)
        if st.button("Predict Salary"):
            prediction = model.predict([[exp]])[0]
            st.success(f"Predicted Salary: ₹{prediction:,.2f}")

# ---------- Option 3: Train House Price Model ----------
elif menu == "Train House Price Model":
    st.header("Train House Price Prediction Model")

    use_sample = st.checkbox("Use sample data", value=True)
    if use_sample:
        data = pd.DataFrame({
            'Area': [500, 1000, 1500, 2000, 2500],
            'Price': [300000, 500000, 700000, 900000, 1100000]
        })
        st.write(data)
    else:
        uploaded = st.file_uploader("Upload CSV with 'Area' and 'Price'", type="csv")
        if uploaded:
            data = pd.read_csv(uploaded)
            st.write(data)
        else:
            data = None

    if data is not None and 'Area' in data.columns and 'Price' in data.columns:
        if st.button("Train and Save House Price Model"):
            X = data[['Area']]
            y = data['Price']
            model = LinearRegression().fit(X, y)
            joblib.dump(model, 'house_price_model.pkl')
            st.success("Model saved as `house_price_model.pkl`")
            st.write(f"Coefficient: {model.coef_[0]:.2f}")
            st.write(f"Intercept: {model.intercept_:.2f}")

# ---------- Option 4: Predict House Price ----------
elif menu == "Predict House Price":
    st.header("Predict House Price")
    if not os.path.exists("house_price_model.pkl"):
        st.warning("Model not found. Please train it first.")
    else:
        model = joblib.load('house_price_model.pkl')
        area = st.number_input("Enter house area (sq. ft)", min_value=100.0, step=50.0)
        if st.button("Predict Price"):
            prediction = model.predict([[area]])[0]
            st.success(f"Predicted House Price: ₹{prediction:,.2f}")

# ---------- Option 5: Missing Value Imputation ----------
elif menu == "Missing Value Imputation":
    st.header("Missing Value Imputation for Target Variable 'Y'")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("Original Dataset")
        st.write(df)

        st.subheader("Missing Value Summary")
        st.write(df.isnull().sum())

        if 'Y' in df.columns:
            st.subheader("Distribution of Y (with missing values)")
            fig, ax = plt.subplots()
            sns.histplot(df["Y"], kde=True, ax=ax)
            st.pyplot(fig)

            st.header("Basic Imputation Techniques")
            if df["Y"].isnull().sum() > 0:
                st.write("Mean Imputation:", df["Y"].fillna(df["Y"].mean()).head())
                st.write("Median Imputation:", df["Y"].fillna(df["Y"].median()).head())
                st.write("Mode Imputation:", df["Y"].fillna(df["Y"].mode()[0]).head())

            st.header("Linear Regression Imputation")
            if df["Y"].isnull().sum() > 0:
                df_known = df[df["Y"].notnull()]
                df_missing = df[df["Y"].isnull()]
                X_known = df_known.drop(columns=["Y"]).select_dtypes(include=[np.number])
                y_known = df_known["Y"]
                X_missing = df_missing.drop(columns=["Y"])[X_known.columns]

                if not X_known.empty and not X_missing.empty:
                    model = LinearRegression().fit(X_known, y_known)
                    y_pred = model.predict(X_missing)
                    df.loc[df["Y"].isnull(), "Y"] = y_pred
                    st.success("Missing Y values imputed using Linear Regression.")
                    st.subheader("Updated Dataset")
                    st.write(df)

                    st.download_button(
                        label="Download Updated Dataset",
                        data=df.to_csv(index=False),
                        file_name="updated_dataset.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No numeric features available for regression.")
            else:
                st.info("No missing values in Y.")
        else:
            st.error("Column 'Y' not found in dataset.")
