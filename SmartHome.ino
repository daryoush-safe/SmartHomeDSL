
// Auto-generated Arduino code


enum State { IDLE, ALERT, COMFORTABLE };
State currentState = IDLE;


float readTemperature(int pin) {
  int v = analogRead(pin);
  float voltage = v * (5.0 / 1023.0);
  return voltage * 100.0; // LM35
}
float readHumidity(int pin) {
  return analogRead(pin) * 4.88 / 10; // Simplified
}
float readUltrasonic(int pin) {
  // Placeholder ultrasonic sensor logic
  return analogRead(pin);
}


const int tempSensor = A0;
void setup() {
  Serial.begin(9600);
pinMode(13, OUTPUT);
pinMode(8, OUTPUT);
  
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
    case IDLE: if (readTemperature(tempSensor) * 3 > 15) currentState = ALERT; break;
  }
}

void loop() {
  checkTransitions();
  switch(currentState) {
    case IDLE: state_idle(); break;case ALERT: state_alert(); break;case COMFORTABLE: state_comfortable(); break;
  }
}
