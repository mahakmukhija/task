#2
# train_salary_model.py
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Example data (you can load from CSV as well)
data = pd.DataFrame({
    'Experience': [1, 2, 3, 4, 5, 6, 7],
    'Salary': [30000, 35000, 40000, 50000, 55000, 60000, 65000]
})

# Split data into features (X) and target (y)
X = data[['Experience']]
y = data['Salary']

# Train the model
model = LinearRegression()
model.fit(X, y)

# Save the trained model
joblib.dump(model, 'salary_model.pkl')
print("Model saved as salary_model.pkl")