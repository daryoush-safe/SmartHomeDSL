# SmartHomeDSL: A Domain-Specific Language for Smart Home Automation

## Overview

SmartHomeDSL is a Domain-Specific Language (DSL) designed to simplify the creation of state machines for smart home automation systems. It provides a high-level, human-readable syntax for defining devices, states, actions, and state transitions, which are then translated into Arduino-compatible C++ code. Built using ANTLR4, the DSL generates an Abstract Syntax Tree (AST) that is validated and processed to produce executable code for controlling hardware like sensors, actuators, and displays on microcontrollers (e.g., Arduino Uno).

### Key Features
- **Device Declarations**: Define hardware devices with specific types and pin assignments.
- **State Declarations**: Group actions (e.g., device controls, delays) into states.
- **Transition Declarations**: Specify conditions for state transitions, including logical expressions and device getters.
- **Validation**: Ensures correct device types, pin assignments, and state references during parsing.
- **Code Generation**: Produces Arduino C++ code with setup, loop, state functions, and helper utilities.
- **Extensibility**: Supports a variety of common IoT devices with easy expansion for new hardware.

This project is ideal for IoT prototyping, home automation projects, or educational purposes, enabling users to focus on logic rather than low-level Arduino programming.

## Project Structure

```
SmartHomeDSL/
├── gen/                             # ANTLR-generated lexer and parser files
│   ├── SmartHomeStateMachineLexer.py # Lexer for tokenizing DSL input
│   ├── SmartHomeStateMachineParser.py# Parser for building parse tree
│   └── ...                          # Other ANTLR-generated files
├── required_code_collection/        # Utility modules for AST processing
│   ├── astTree.py                   # AST implementation
│   ├── make_ast_subtree.py          # Helper for constructing AST nodes
│   ├── ast_to_networkx_graph.py      # Optional AST visualization (requires Graphviz)
├── test/                            # Sample DSL input files
│   ├── test.txt                     # Motion and temperature-based example
│   ├── test2.txt                    # Servo and RGB LED example
│   ├── test3.txt                    # Humidity and buzzer example
├── .gitignore                       # Git ignore file
├── code_generator.py                # Generates Arduino C++ code from AST
├── CustomListener.py                # ANTLR listener for AST construction and validation
├── main.py                          # Entry point for parsing and code generation
├── requirements.txt                 # Python dependencies (e.g., antlr4, networkx)
├── SmartHome.ino                    # Generated Arduino output (overwritten on run)
└── SmartHomeStateMachine.g4         # ANTLR grammar defining DSL syntax
```

## Supported Devices and Functions

SmartHomeDSL supports a range of common smart home devices, each with specific getter methods (for reading data) and action methods (for controlling hardware). Devices are declared with a type and optional pin assignments, validated against supported types and pin compatibility.

### Device Types and Methods

Below is a comprehensive list of supported devices, their types (digital or analog), and their methods with input counts:

- **LED** (Digital)
  - **Action Methods**:
    - `on()`: 0 inputs – Turns the LED on.
    - `off()`: 0 inputs – Turns the LED off.
    - `toggle()`: 0 inputs – Toggles the LED state.
    - `blink(ms)`: 1 input (ms: integer, e.g., 500) – Blinks LED with specified delay in milliseconds.
    - `setBrightness(percentage)`: 1 input (percentage: integer, 0-100) – Sets LED brightness (PWM).
- **BUTTON** (Digital)
  - **Getter Methods**:
    - `isPressed()`: 0 inputs – Returns true if button is pressed.
- **SERVO** (Digital)
  - **Action Methods**:
    - `moveServo(angle)`: 1 input (angle: integer, 0-180) – Moves servo to specified angle.
    - `sweepServo(start_angle, end_angle, step, delay_ms)`: 4 inputs (start_angle, end_angle, step, delay_ms: integers) – Sweeps servo from start to end angle with step increment and delay.
- **LCD** (Digital, requires 6 pins: RS, EN, D4-D7)
  - **Action Methods**:
    - `display(text)`: 1 input (text: string, e.g., "Hello") – Displays text on LCD.
- **BUZZER** (Digital)
  - **Action Methods**:
    - `off()`: 0 inputs – Stops buzzer sound.
    - `beep(ms)`: 1 input (ms: integer, e.g., 1000) – Plays a 1kHz tone for specified milliseconds.
- **TEMPERATURE_SENSOR** (Analog, e.g., LM35)
  - **Getter Methods**:
    - `getTemperature()`: 0 inputs – Returns temperature in Celsius.
- **HUMIDITY_SENSOR** (Analog, e.g., DHT11)
  - **Getter Methods**:
    - `getHumidity()`: 0 inputs – Returns humidity percentage.
- **MOTION_SENSOR** (Digital, e.g., PIR)
  - **Getter Methods**:
    - `isMotionDetected()`: 0 inputs – Returns true if motion is detected.
- **LIGHT_SENSOR** (Analog, e.g., photoresistor)
  - **Getter Methods**:
    - `getLight()`: 0 inputs – Returns light level (0-1023, low for dark, high for bright).
- **ULTRASONIC_SENSOR** (Digital, requires 2 pins: TRIG, ECHO)
  - **Getter Methods**:
    - `getDistance()`: 0 inputs – Returns distance in centimeters.
- **RGB_LED** (Digital, requires 3 pins: R, G, B)
  - **Action Methods**:
    - `setColor(r, g, b)`: 3 inputs (r, g, b: integers, 0-255) – Sets RGB LED color.
- **POTENTIOMETER** (Analog)
  - **Getter Methods**:
    - `readPotentiometer()`: 0 inputs – Returns value (0-1023).
- **DISPLAY** (Digital, similar to LCD)
  - **Action Methods**:
    - `display(text)`: 1 input (text: string, e.g., "Status: OK") – Displays text on the screen.

### Pin Assignments

Devices require specific pin types based on their digital or analog nature. Pins are validated to ensure uniqueness and compatibility:

- **Analog Pins** (for analog devices: TEMPERATURE_SENSOR, HUMIDITY_SENSOR, LIGHT_SENSOR, POTENTIOMETER):
  - Available: 14, 15, 16, 17, 18, 19 (maps to A0-A5 on Arduino Uno).
- **Digital Pins** (for digital devices: LED, BUTTON, SERVO, LCD, BUZZER, MOTION_SENSOR, ULTRASONIC_SENSOR, RGB_LED, DISPLAY):
  - Available: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13.

**Notes**:
- Analog devices cannot use digital pins, and vice versa.
- Multi-pin devices (e.g., RGB_LED, LCD, ULTRASONIC_SENSOR) require the correct number of pins.
- Pin conflicts (e.g., reusing a pin) are caught during parsing with descriptive errors.

## DSL Syntax

The DSL syntax, defined in `SmartHomeStateMachine.g4`, is concise and declarative:

- **Device Declaration**:
  ```
  device <name> : <type> pin <pin1>, pin <pin2>;
  ```
  - Example: `device myLed : LED pin 13;`
  - Pins are optional for some devices; multiple pins for devices like RGB_LED or LCD.
- **State Declaration**:
  ```
  state <name> { <action1>, <action2>, ... }
  ```
  - Actions: Device methods (e.g., `myLed.on()`), delays (e.g., `delay(500)`), or variable assignments (e.g., `var = 10`).
  - Example: `state idle { myLed.off(), delay(1000) }`
- **Transition Declaration**:
  ```
  transition <source> -> <target> when <condition>;
  ```
  - Source can be a state name or `*` (all states).
  - Conditions use logical/arithmetic operators and device getters (e.g., `tempSensor.getTemperature() > 20`).
  - Example: `transition idle -> alert when motionSensor.isMotionDetected();`

**Supported Literals and Operators**:
- Literals: Numbers (e.g., `123`, `12.34`), strings (e.g., `"Hello"`), booleans (`true`, `false`).
- Operators: Logical (`&&`, `||`, `!`), comparison (`==`, `!=`, `<`, `>`, `<=`, `>=`), arithmetic (`+`, `-`, `*`, `/`, `%`).
- Comments: Single-line (`//`), multi-line (`/* */`).

## Code Generation

The `code_generator.py` module transforms the AST into Arduino C++ code, producing a complete `.ino` file:

1. **Device Handling**: Maps devices to pins/types, generates `pinMode()` calls in `setup()`.
2. **State Handling**: Creates state functions (e.g., `void state_idle() { ... }`) for actions like `digitalWrite()` or `delay()`.
3. **Transition Handling**: Generates a `checkTransitions()` function with `if-else` logic for conditions, grouped by source state.
4. **Helper Functions**: Includes necessary libraries (e.g., `<Servo.h>`, `<DHT.h>`) and defines sensor-specific functions (e.g., `float readTemperature(int pin)`).
5. **Code Assembly**: Produces a complete program with:
   - Enum for states (e.g., `enum State { IDLE, ALERT }`).
   - Global state variable (e.g., `State currentState = IDLE`).
   - `setup()`: Initializes pins, Serial (9600 baud), and device-specific setup (e.g., `servo.attach()`).
   - `loop()`: Runs `checkTransitions()` and calls the current state’s function, with a 200ms delay.

The generated code handles edge cases (e.g., clamping servo angles to 0-180, scaling brightness to 0-255) and includes Serial logging for debugging.

## Installation

1. **Install Python**: Requires Python 3.x.
2. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```
   - Dependencies: `antlr4-python3-runtime`, `networkx` (for AST visualization).
3. **Generate ANTLR Files**:
   ```
   antlr4 -Dlanguage=Python3 SmartHomeStateMachine.g4
   ```
   - Outputs lexer/parser to `gen/`.
4. **Install Graphviz** (optional, for AST visualization): Install Graphviz and add to PATH.

## Usage

Run the main script to parse a DSL file and generate Arduino code:

```
python main.py -i <input_dsl.txt> -o <output.ino>
```

- **Default Input**: `./test/test.txt`
- **Default Output**: `SmartHome.ino`
- **Optional Visualization**: Uncomment `show_ast(ast.root)` in `main.py` to visualize the AST (requires Graphviz).

## Sample Input and Output

### Sample Input 1: Motion and Temperature Control (`test/test.txt`)

```
device mainLED : LED pin 13;
device doorSensor : MOTION_SENSOR pin 2;
device tempSensor : TEMPERATURE_SENSOR pin 4;
device buzzer : BUZZER pin 8;

state idle {
    mainLED.off()
}

state alert {
    mainLED.blink(500),
    buzzer.beep(1000),
    delay(2000)
}

state comfortable {
    mainLED.on()
}

transition idle -> alert when doorSensor.isMotionDetected();
transition * -> alert when doorSensor.isMotionDetected();
transition alert -> idle when !doorSensor.isMotionDetected();
transition idle -> comfortable when tempSensor.getTemperature() > 20 && tempSensor.getTemperature() < 25;
transition idle -> comfortable when tempSensor.getTemperature() >= 20 || tempSensor.getTemperature() < tempSensor.getTemperature();
```

### Sample Output 1: Generated Arduino Code (excerpt)

```cpp
// Auto-generated Arduino code

enum State { IDLE, ALERT, COMFORTABLE };
State currentState = IDLE;

float readTemperature(int pin) {
  int v = analogRead(pin);
  float voltage = v * (5.0 / 1023.0);
  float value = voltage * 100.0; // LM35
  Serial.print("temperature: ");
  Serial.println(value);
  return value;
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
  pinMode(2, INPUT);
  pinMode(4, INPUT);
  pinMode(8, OUTPUT);
}

void state_idle() {
  digitalWrite(13, LOW);
}

void state_alert() {
  digitalWrite(13, !digitalRead(13)); delay(500);
  tone(8, 1000);
  delay(1000);
  noTone(8);
  delay(2000);
}

void state_comfortable() {
  digitalWrite(13, HIGH);
}

void checkTransitions() {
  switch(currentState) {
    case IDLE:
      if (readMotion(2)) currentState = ALERT;
      else if (readTemperature(4) > 20 && readTemperature(4) < 25) currentState = COMFORTABLE;
      else if (readTemperature(4) >= 20 || readTemperature(4) < readTemperature(4)) currentState = COMFORTABLE;
      break;
    case ALERT:
      if (!readMotion(2)) currentState = IDLE;
      break;
  }
}

void loop() {
  checkTransitions();
  switch(currentState) {
    case IDLE: state_idle(); break;
    case ALERT: state_alert(); break;
    case COMFORTABLE: state_comfortable(); break;
  }
  delay(200);
}
```

### Sample Input 2: Servo and RGB LED (`test/test2.txt`)

```
device myServo : SERVO pin 9;
device rgbLed : RGB_LED pin 10, pin 11, pin 12;

state init {
    myServo.moveServo(0),
    rgbLed.setColor(255, 0, 0)
}

state moving {
    myServo.sweepServo(0, 180, 1, 15)
}

transition init -> moving when true;
```

### Sample Output 2: Generated Arduino Code (excerpt)

```cpp
#include <Servo.h>

enum State { INIT, MOVING };
State currentState = INIT;

Servo myServo;

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
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  myServo.attach(9,1000,2000);
}

void state_init() {
  moveServo(myServo, 0);
  analogWrite(10, 255);
  analogWrite(11, 0);
  analogWrite(12, 0);
}

void state_moving() {
  sweepServo(myServo,0,180,1,15);
}

void checkTransitions() {
  switch(currentState) {
    case INIT:
      if (true) currentState = MOVING;
      break;
  }
}

void loop() {
  checkTransitions();
  switch(currentState) {
    case INIT: state_init(); break;
    case MOVING: state_moving(); break;
  }
  delay(200);
}
```

### Error Case Example: Invalid Pin

**Input**:
```
device myLed : LED pin 14;  // 14 is an analog pin
```

**Output (Error)**:
```
ValueError: Error: Device 'myLed' of type 'LED' is digital but has invalid digital pins: ['14']. Valid digital pins: ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
```