
// Auto-generated Arduino code
#include <LiquidCrystal.h>

enum State { IDLE, ALERT, COMFORTABLE };
State currentState = IDLE;

LiquidCrystal lcd(12, 11, 10, 9, 8, 7); // Adjust pins

float readTemperature(int pin) {
  int v = analogRead(pin);
  float voltage = v * (5.0 / 1023.0);
  float value =  voltage * 100.0; // LM35
  Serial.print("temperature: ");
  Serial.println(value);
  return value;
}
float readHumidity(int pin) {
  return analogRead(pin) * 4.88 / 10; // Simplified
}
float readUltrasonic(int pin) {
  // Placeholder ultrasonic sensor logic
  return analogRead(pin);
}
float readLight(int pin) {
  int value = analogRead(pin);
  Serial.print("light: ");
  Serial.println(value);
  return value; // 0 (dark) to 1023 (bright)
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
pinMode(A0, INPUT);
pinMode(A1, INPUT);
pinMode(2, OUTPUT);
pinMode(3, INPUT);
pinMode(4, INPUT);
lcd.begin(16, 2);  // Initialize 16x2 LCD

}

void state_idle() {
  digitalWrite(13, LOW);
}
void state_alert() {
  digitalWrite(13, !digitalRead(13)); delay(500);
}
void state_comfortable() {
  digitalWrite(13, HIGH);
  lcd.clear();
  lcd.print("comfortable");
}

void checkTransitions() {
  switch(currentState) {
    case IDLE:
      if (readTemperature(A0) * 3 > 15) currentState = ALERT;
      else if (readDistance(2, 3) > 15) currentState = ALERT;
      else if (readLight(A1) >= 100) currentState = COMFORTABLE;
      break;
    case ALERT:
      if (readMotion(4) &&readTemperature(A0) < 3) currentState = IDLE;
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
