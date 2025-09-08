
// Auto-generated Arduino code
#include <DHT.h>

enum State { IDLE, ALERT, COMFORTABLE };
State currentState = IDLE;

DHT humSensor(15, DHT11);

float readTemperature(int pin) {
  int v = analogRead(pin);
  float voltage = v * (5.0 / 1023.0);
  float value = voltage * 100.0; // LM35
  Serial.print("temperature: ");
  Serial.println(value);
  return value;
}

float readHumidity(DHT &sensor) {
  float h = sensor.readHumidity();
  if (isnan(h)) {
    Serial.println("Failed to read from DHT sensor!");
    return -1;
  }
  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.println(" %");
  return h;
}

float readDistance(int TRIG_PIN, int ECHO_PIN) {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  // Send 10 µs pulse
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Measure pulse duration
  float duration = pulseIn(ECHO_PIN, HIGH);

  // Calculate distance in cm
  float distance = duration * 0.034 / 2;

  // Print result
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
  return distance;
}

bool readMotion(int pirPin) {
int motion = digitalRead(pirPin);
if (motion == HIGH) {
Serial.println("Motion Detected!");
return true;
} else {
Serial.println("No Motion");
return false;
}
}


void setup() {
Serial.println("Starting Program ...");
Serial.begin(9600);
pinMode(13, OUTPUT);
pinMode(14, INPUT);
humSensor.begin(); // Initialize DHT11 sensor
pinMode(2, OUTPUT);
pinMode(3, INPUT);
pinMode(4, INPUT);

}

void state_idle() {
  digitalWrite(13, LOW);
}
void state_alert() {
  digitalWrite(13, !digitalRead(13)); delay(500);
}
void state_comfortable() {
  digitalWrite(13, HIGH);
}

void checkTransitions() {
  switch(currentState) {
    case IDLE:
      if (readHumidity(humSensor) >= 30) currentState = COMFORTABLE;
      break;
    case ALERT:
      if (readMotion(4) &&readTemperature(14) < 3) currentState = IDLE;
      break;
  }
}

void loop() {
  checkTransitions();
  switch(currentState) {
    case IDLE: state_idle(); break;case ALERT: state_alert(); break;case COMFORTABLE: state_comfortable(); break;
  }
  delay(200);
}
