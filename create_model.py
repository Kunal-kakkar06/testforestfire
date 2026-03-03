import pickle
import os
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Create test model
print("Creating test model...")
model = RandomForestRegressor(n_estimators=10, random_state=42)
X_test = np.random.rand(100, 11)  # 11 features
y_test = np.random.rand(100)
model.fit(X_test, y_test)

# Create models directory
os.makedirs('models', exist_ok=True)

# Save model
with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Test model created and saved to models/model.pkl")
