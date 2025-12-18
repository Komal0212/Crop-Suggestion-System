import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

data = pd.read_csv(r"C:\Users\DELL\Desktop\crop data\crop_data.csv")

X = data[['Temperature',	'Humidity',	'SoilMoisture',	'Sunlight',	'Precipitation']]
y = data['Crop']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("Model accuracy:", accuracy_score(y_test, predictions)*6759)

joblib.dump(model, "crop_model.pkl")

print("Model saved as crop_model.pkl")