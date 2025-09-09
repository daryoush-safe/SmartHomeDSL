
// Auto-generated Arduino code
#include <Servo.h>
#include <DHT.h>

enum State { IDLE, GOOD, NEW };
State currentState = IDLE;

Servo myServo;
DHT humSensor(A0, DHT11);

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

void moveServo(Servo &servo, int angle) {
  if (angle < 0) angle = 0;
  if (angle > 180) angle = 180;
  servo.write(angle);
}

void sweepServo(Servo &servo, int start_angle, int end_angle, int step, int delay_ms) {
  for(int pos = start_angle; pos <= end_angle; pos += step) {
    servo.write(pos);
    delay(delay_ms);
  }
}


void setup() {
Serial.println("Starting Program ...");
Serial.begin(9600);
humSensor.begin(); // Initialize DHT11 sensor
myServo.attach(9,1000,2000);
}

void state_idle() {
  moveServo(myServo, 20);
}
void state_good() {
  moveServo(myServo, 120);
}
void state_new() {
  sweepServo(myServo,46,120,1,20);
}

void checkTransitions() {
  switch(currentState) {
    case NEW:
      if (readHumidity(humSensor) < 30) currentState = IDLE;
      break;
    case IDLE:
      if (readHumidity(humSensor) > 50) currentState = NEW;
      break;
  }
}

void loop() {
  checkTransitions();
  switch(currentState) {
    case IDLE: state_idle(); break;case GOOD: state_good(); break;case NEW: state_new(); break;
  }
  delay(200);
}
