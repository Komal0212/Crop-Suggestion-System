#include "DHT.h"

// -------- DHT Sensor --------
#define DHTPIN 3       // DATA pin jaha DHT connected hai
#define DHTTYPE DHT22  // Agar DHT11 use kar rahe ho toh change karo
DHT dht(DHTPIN, DHTTYPE);

// -------- Other Sensors --------
#define SOIL_PIN A0
#define LDR_PIN A1
#define RAIN_PIN A2
#define RELAY_PIN 4

int soilValue = 0;
int ldrValue = 0;
int rainValue = 0;

void setup() {
  Serial.begin(9600);

  // ---- Initialize sensors & relay ----
  pinMode(SOIL_PIN, INPUT);
  pinMode(LDR_PIN, INPUT);
  pinMode(RAIN_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH); // relay OFF initially

  // ---- Initialize DHT ----
  dht.begin();
  Serial.println("Crop Suggestion System Initializing...");
  delay(2000);  // wait for DHT to stabilize

  // ---- Read DHT with retries ----
  float temperature = NAN;
  float humidity = NAN;

  for (int i = 0; i < 5; i++) {      // max 5 attempts
    temperature = dht.readTemperature();
    humidity = dht.readHumidity();
    if (!isnan(temperature) && !isnan(humidity)) break;  // success
    delay(2000);
  }

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("DHT_ERROR");  // still failed
    return;  // stop here
  }

  // ---- Read other sensors ----
  soilValue = analogRead(SOIL_PIN);
  int soilPercent = map(soilValue, 0, 1023, 0, 100);

  ldrValue = analogRead(LDR_PIN);
  int sunlight = map(ldrValue, 0, 1023, 0, 1023);

  rainValue = analogRead(RAIN_PIN);
  int precipitation = map(rainValue, 0, 1023, 0, 10);

  // ---- Send CSV once ----
  Serial.print(temperature); Serial.print(",");
  Serial.print(humidity); Serial.print(",");
  Serial.print(soilPercent); Serial.print(",");
  Serial.print(sunlight); Serial.print(",");
  Serial.println(precipitation);

  // ---- Wait 5 seconds for relay command from Python ----
  unsigned long startTime = millis();
  while (millis() - startTime < 5000) {
    if (Serial.available() > 0) {
      String cmd = Serial.readStringUntil('\n');
      cmd.trim();
      if (cmd == "ON") digitalWrite(RELAY_PIN, LOW);   // Active LOW → motor ON
      else if (cmd == "OFF") digitalWrite(RELAY_PIN, HIGH); // motor OFF
    }
  }

  // Ensure relay OFF after 5 seconds
  digitalWrite(RELAY_PIN, HIGH);
}

void loop() {
  // nothing — single reading only
}
