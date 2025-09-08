
// Auto-generated Arduino code


enum State { IDLE, S1, S2, S3 };
State currentState = IDLE;


float readTemperature(int pin) {
  int v = analogRead(pin);
  float voltage = v * (5.0 / 1023.0);
  float value = voltage * 100.0; // LM35
  Serial.print("temperature: ");
  Serial.println(value);
  return value;
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
pinMode(6, OUTPUT);
pinMode(14, INPUT);
pinMode(15, INPUT);
pinMode(2, OUTPUT);
pinMode(3, INPUT);
pinMode(4, INPUT);

}

void state_idle() {
  digitalWrite(6, LOW);
}
void state_s1() {
  analogWrite(6, 191);
  analogWrite(10, 211);
  analogWrite(9, 55);
  analogWrite(5, 160);
}
void state_s2() {
  analogWrite(6, 128);
  analogWrite(10, 40);
  analogWrite(9, 120);
  analogWrite(5, 20);
}
void state_s3() {
  analogWrite(6, 64);
  analogWrite(10, 255);
  analogWrite(9, 0);
  analogWrite(5, 255);
}

void checkTransitions() {
  switch(currentState) {
    case IDLE:
      if (readTemperature(14) > 3) currentState = S1;
      break;
    case S1:
      if (readTemperature(14) > 5) currentState = S2;
      break;
    case S2:
      if (readTemperature(14) > 7) currentState = S3;
      break;
  }
}

void loop() {
  checkTransitions();
  switch(currentState) {
    case IDLE: state_idle(); break;case S1: state_s1(); break;case S2: state_s2(); break;case S3: state_s3(); break;
  }
  delay(200);
}
