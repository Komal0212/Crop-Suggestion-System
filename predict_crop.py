import serial
import pandas as pd
import joblib
import time
import json
import matplotlib.pyplot as plt
import os

model = joblib.load("crop_model.pkl")

arduino = serial.Serial("COM5", 9600, timeout=2)
time.sleep(2)

print("Connected! Reading one-time sensor data...")

csv_file = "sensor_history.csv"

#Reading sensor data
while True:
    data = arduino.readline().decode().strip()
    if not data:
        continue

    parts = data.split(',')
    if len(parts) != 5:
        print("Skipping:", data)
        continue

    try:
        temperature = float(parts[0])
        humidity = float(parts[1])
        soil = float(parts[2])
        light = float(parts[3])
        rain = float(parts[4])
    except:
        print("Invalid:", data)
        continue

    break 

# Predicting crop
features = pd.DataFrame([[temperature, humidity, soil, light, rain]],
                        columns=['Temperature', 'Humidity', 'SoilMoisture', 'Sunlight', 'Precipitation'])

prediction = model.predict(features)[0]

# saving to JSON file
sensor_data = {
    "temperature": temperature,
    "humidity": humidity,
    "soil": soil,
    "light": light,
    "rain": rain,
    "crop": prediction
}

with open(r'C:\Users\DELL\Desktop\crop recommendation\sensor.json', "w") as f:
    json.dump(sensor_data, f)

row = pd.DataFrame([[temperature, humidity, soil, light, rain]],
                   columns=['Temperature', 'Humidity', 'Soil', 'Light', 'Rain'])

if os.path.exists(csv_file):
    row.to_csv(csv_file, mode='a', header=False, index=False)
else:
    row.to_csv(csv_file, mode='w', header=True, index=False)

# Generating graph
data_hist = pd.read_csv(csv_file)

plt.figure(figsize=(8, 5))
plt.plot(data_hist.index, data_hist['Soil'], marker='o')
plt.xlabel("Reading Number")
plt.ylabel("Soil Moisture")
plt.title("Soil Moisture Trend")
plt.grid(True)
plt.tight_layout()
plt.savefig("trend.png")
plt.close()

print("\nFINAL OUTPUT")
print(f"T={temperature}°C | H={humidity}% | Soil={soil} | Light={light} | Rain={rain}")
print("Predicted Crop:", prediction)

print("\nExiting predict.py ...")
exit(0)
