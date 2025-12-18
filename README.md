# Crop Suggestion System

## Overview
This project implements an **IoT-enabled real-time crop suggestion and soil monitoring system** designed to assist farmers in making data-driven agricultural decisions. The system collects live environmental data from field-deployed sensors and analyzes soil and weather conditions to recommend suitable crops and irrigation actions.

By combining low-cost hardware with a web-based dashboard, the project aims to improve agricultural productivity, optimize resource usage, and reduce reliance on guesswork.

---

## Motivation
Agricultural decisions in India are often based on traditional knowledge rather than real-time data, leading to inefficient irrigation, poor crop selection, and reduced yields. With the availability of affordable sensors and microcontrollers, it is now possible to build intelligent systems that provide actionable insights to farmers based on actual field conditions.

---

## Key Features
- **Real-Time Data Collection**
  - Soil moisture
  - Temperature
  - Humidity
  - Rainfall
  - Light intensity

- **Crop Suggestion Engine**
  - Recommends suitable crops based on soil and weather conditions
  - Uses rule-based decision logic

- **Web Dashboard**
  - Displays live sensor readings
  - Interactive graphs for soil moisture trends and soil classification

- **Weather Integration**
  - Fetches short-term forecasts using OpenWeatherMap API

- **Alerts & Monitoring**
  - Early warnings for low soil moisture or excess rainfall
  - Remote field monitoring

---

## System Architecture
1. Sensors collect real-time soil and atmospheric data.
2. Arduino processes sensor readings and transmits data to the cloud.
3. Data is stored in a Firebase real-time database.
4. A web application fetches and visualizes data.
5. Decision logic analyzes parameters and suggests crops and irrigation actions.

---

## Hardware Components
- Arduino UNO R3  
- Soil Moisture Sensor  
- DHT11 (Temperature & Humidity)  
- Rainfall Sensor  
- Light Dependent Resistor (LDR)  
- Relay Module and Mini Water Pump  
- Breadboard, Resistors, and Jumper Wires  

---

## Technologies Used
- **Hardware:** Arduino UNO, IoT Sensors
- **Backend / Cloud:** Firebase Realtime Database
- **Frontend:** HTML, CSS, JavaScript
- **APIs:** OpenWeatherMap
- **Development Tools:** Arduino IDE

---

## Implementation Steps
- Sensor integration and testing using Arduino IDE
- Cloud data transmission via Firebase
- Web dashboard development for data visualization
- Rule-based crop suggestion logic
- Testing and calibration under different conditions

---


## Learning Outcomes
- Practical experience with IoT-based systems
- Understanding real-time data collection and visualization
- Integration of hardware with cloud platforms
- Exposure to rule-based decision systems for agriculture

---


## Future Enhancements
- Machine learning–based crop prediction
- Mobile application integration
- SMS or app-based alerts
- Support for multiple farms and regions
