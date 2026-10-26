
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression

# Training data
# Each row: [study_hours, prev_score]
X = np.array([
    [1, 40],  # Studied 1 hour, scored 40 previously → Fail
    [2, 45],  # Studied 2 hours, scored 45 → Fail
    [3, 50],  # Studied 3 hours, scored 50 → Fail
    [4, 60],  # Studied 4 hours, scored 60 → Pass
    [5, 65],  # Studied 5 hours, scored 65 → Pass
    [6, 70],  # Studied 6 hours, scored 70 → Pass
    [7, 75],  # Studied 7 hours, scored 75 → Pass
    [8, 85],  # Studied 8 hours, scored 85 → Pass
    [2, 80],  # Studied 2 hours but high previous score → Pass
    [1, 30],  # Studied 1 hour, low previous score → Fail
])

# 0 = Fail, 1 = Pass
y = np.array([0, 0, 0, 1, 1, 1, 1, 1, 1, 0])

# Train the model
model = LogisticRegression()
model.fit(X, y)  # This is where learning happens

# Save the trained model to disk
joblib.dump(model, "model.pkl")
print("Model trained and saved to model.pkl")

# Quick test on the training data
predictions = model.predict(X)

print("Sample predictions:", predictions)
print("Actual labels:     ", y)
