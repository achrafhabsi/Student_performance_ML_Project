import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
import pickle
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("MY_DATA.csv")  # Replace with actual file

# Features and target
X = df.drop(columns=["result", "G3"])
df.replace('U', np.nan, inplace=True)
df = df.apply(pd.to_numeric, errors='coerce')

y = df["result"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Random Forest model
rf = RandomForestClassifier()

# Grid search for best parameters
param_grid = {"n_estimators": [50, 100, 200]}
grid_rf = GridSearchCV(rf, param_grid, cv=5, scoring='accuracy')
grid_rf.fit(X_train, y_train)

# Save the trained model using pickle
with open("random_forest_model.pkl", "wb") as file:
    pickle.dump(grid_rf.best_estimator_, file)

print("Model saved as random_forest_model.pkl")
