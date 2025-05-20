import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

# Example: Load data (replace with your actual data path)
data_path = os.path.join(
    os.path.dirname(__file__), '../../data/processed/sample_asset_data.csv'
)
if not os.path.exists(data_path):
    print(f"Data file not found: {data_path}")
    exit(1)

df = pd.read_csv(data_path)

# Example: Assume binary classification on a 'target' column
y = df['target']
X = df.drop(columns=['target'])

# One-hot encode categorical columns
X = pd.get_dummies(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {acc:.2f}")

# Save model
os.makedirs(
    os.path.join(os.path.dirname(__file__), '../models'), exist_ok=True
)
model_path = os.path.join(
    os.path.dirname(__file__), '../models/logreg_model.joblib'
)
joblib.dump(model, model_path)
print(f"Model saved to {model_path}") 