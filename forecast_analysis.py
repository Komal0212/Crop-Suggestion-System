import serial
import time
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_KEY = "0ec2351cbd4ff92a39cfb05aded19a82"   
CITY = "Hisar,IN"               
PORT = "COM5"                   
CROP = "Wheat"                  
MIN_MOISTURE = 40               
MAX_MOISTURE = 60               

def get_forecast_data(api_key, city):
    print("[INFO] Fetching weather forecast...")
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    res = requests.get(url)
    data = res.json()

    if res.status_code != 200:
        raise Exception(f"API Error: {data.get('message', 'Unknown error')}")

    records = []
    for entry in data['list']:
        date = entry['dt_txt'].split(" ")[0]
        temp = entry['main']['temp']
        rain = entry.get('rain', {}).get('3h', 0)
        records.append((date, temp, rain))

    df = pd.DataFrame(records, columns=['date', 'temperature', 'rainfall'])
    forecast = df.groupby('date').agg({'temperature':'mean','rainfall':'sum'}).reset_index()
    print(" Forecast data loaded successfully.\n")
    return forecast

def read_sensor_data(port):
    
    try:
        line = port.readline().decode('utf-8').strip()
        if not line:
            return None
        print(f"[SERIAL] {line}")

        if not any(char.isdigit() for char in line):
            return None

        parts = line.split(',')
        if len(parts) < 5:
            return None

        temp = float(parts[0])
        humidity = float(parts[1])
        soil_moisture = float(parts[2])
        light = float(parts[3])
        rain = float(parts[4])

        return {
            'temperature_sensor': temp,
            'humidity_sensor': humidity,
            'soil_moisture': soil_moisture,
            'light': light,
            'rain_sensor': rain
        }

    except Exception as e:
        print(f"WARNING: Serial read error: {e}")
        return None

def irrigation_control(arduino, soil_moisture):
    if soil_moisture < MIN_MOISTURE:
        print("ALERT: Soil moisture too low! Starting irrigation...")
        arduino.write(b'ON\n')
        time.sleep(5)
        arduino.write(b'OFF\n')

        print(" Irrigation stopped (relay off)")
    elif soil_moisture > MAX_MOISTURE:
        print(" Soil moisture sufficient. No irrigation needed.")
    else:
        print(" Soil moisture optimal for crop.")

try:
    arduino = serial.Serial(PORT, 9600, timeout=2)
    time.sleep(2)
    print(f" Arduino detected on {PORT}")
except Exception as e:
    print(f"ERROR: Cannot connect to Arduino: {e}")
    exit()

# Fetching weather forecast
try:
    forecast = get_forecast_data(API_KEY, CITY)
except Exception as e:
    print(f"ERROR: Unable to fetch forecast: {e}")
    exit()

# Read sensor data
sensor_data = None
print(" Waiting for Arduino data...")
for _ in range(15): 
    data = read_sensor_data(arduino)
    if data:
        sensor_data = data
        break
    time.sleep(1)

if not sensor_data:
    print("ERROR: No valid sensor data received.")
    exit()

soil_moisture = sensor_data['soil_moisture']
print(f"Current soil moisture: {soil_moisture}%")

irrigation_control(arduino, soil_moisture)

plt.figure(figsize=(10, 5))

#Graph 1: Soil Moisture vs Temperature
plt.subplot(1, 2, 1)
plt.scatter(forecast['temperature'], [soil_moisture]*len(forecast), color='orange', label='Soil Moisture')
plt.xlabel('Temperature (°C)')
plt.ylabel('Soil Moisture (%)')
plt.title('Soil Moisture vs Temperature')
plt.grid(True)
plt.legend()

#Graph 2: Soil Moisture vs Rainfall
plt.subplot(1, 2, 2)
plt.scatter(forecast['rainfall'], [soil_moisture]*len(forecast), color='green', label='Soil Moisture')
plt.xlabel('Rainfall (mm)')
plt.ylabel('Soil Moisture (%)')
plt.title('Soil Moisture vs Rainfall')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
plt.figure(figsize=(10, 5))

#Graph 1: Soil Moisture vs Temperature
plt.subplot(1, 2, 1)
plt.scatter(forecast['temperature'], [soil_moisture]*len(forecast), color='orange', label='Soil Moisture')
plt.xlabel('Temperature (°C)')
plt.ylabel('Soil Moisture (%)')
plt.title('Soil Moisture vs Temperature')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save first graph
plt.savefig(r'C:\Users\DELL\Desktop\crop recommendation\CropPredictionProject\graph1.png')

# Graph 2: Soil Moisture vs Rainfall
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.scatter(forecast['rainfall'], [soil_moisture]*len(forecast), color='green', label='Soil Moisture')
plt.xlabel('Rainfall (mm)')
plt.ylabel('Soil Moisture (%)')
plt.title('Soil Moisture vs Rainfall')
plt.grid(True)
plt.legend()
plt.tight_layout()

#Save second graph
plt.savefig(r'C:\Users\DELL\Desktop\crop recommendation\CropPredictionProject\graph2.png')

print(" Graphs saved successfully.")
