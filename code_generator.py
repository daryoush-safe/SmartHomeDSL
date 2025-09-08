import sys
from required_code_collection.astTree import AST
from collections import defaultdict


def joiner(list, tab=False):
    if tab:
        return "\n\t".join(list)
    else:
        return "\n".join(list)


class CodeGenerator:
    def __init__(self, ast: AST):
        self.ast = ast
        self.devices = {}
        self.states = {}
        self.transitions = []

    def generate(self):
        self._parse_program(self.ast)
        return self._assemble_code()

    def _parse_program(self, node):
        for child in node.children:
            if child.value == "device_dec":
                self._handle_device(child)
            elif child.value == "state_dec":
                self._handle_state(child)
            elif child.value == "transition_dec":
                self._handle_transition(child)

    def _handle_device(self, node):
        # Example: device mainLED : LED pin 13;
        name = node.children[0].value
        dev_type = node.children[1].value
        pin_list = []
        if len(node.children) > 2:
            for i in range(2, len(node.children)):
                if int() <= 13:
                    pin_list.append(node.children[i].value)
                else:
                    pin_list.append(f"A{int(node.children[i].value) - 14}")
        self.devices[name] = (dev_type, pin_list)

    def _handle_state(self, node):
        state_name = node.children[0].value
        actions = []
        for action_node in node.children[1:]:
            if action_node.value == "device_action":
                actions.append(self._translate_device_action(action_node))
            elif action_node.value == "delay_action":
                actions.append(self._translate_delay_action(action_node))
        self.states[state_name] = actions

    def _handle_transition(self, node):
        src = node.children[0].value
        dst = node.children[1].value
        condition_node = node.children[2]
        condition = self._calc_con(condition_node)
        self.transitions.append((src, dst, condition))

    # --------------------------
    # Device Actions
    # --------------------------
    def _translate_device_action(self, node):
        dev = node.children[0].value
        action = node.children[1].value
        args = [c.value for c in node.children[2:]]
        dev_type, pin = self.devices[dev]

        # LED
        if dev_type in ["LED"]:
            if action == "on":
                return f"digitalWrite({pin[0]}, HIGH);"
            elif action == "off":
                return f"digitalWrite({pin[0]}, LOW);"
            elif action == "toggle":
                return f"digitalWrite({pin[0]}, !digitalRead({pin[0]}));"
            elif action == "blink":
                delay_ms = args[0] if args else "500"
                return f"digitalWrite({pin[0]}, !digitalRead({pin[0]})); delay({delay_ms});"
            elif action == "setBrightness":
                light = int(args[0]) if args else 255
                if light > 100 :
                    light = 100
                elif light < 0:
                    light = 0
                light = round((light / 100) * 255)
                return f"analogWrite({pin[0]}, {light});"

        if dev_type == "RGB_LED":
            if action == "setColor":
                r, g, b = args if len(args) == 3 else ("255", "255", "255")
                return f"analogWrite({pin[0]}, {r});\n  analogWrite({pin[1]}, {g});\n  analogWrite({pin[2]}, {b});"

        # BUTTON
        if dev_type in ["BUTTON"]:
            return f"// {dev} actions handled via getters"

        # SERVO
        if dev_type == "SERVO":
            if action == "moveServo":
                angle = args[0] if args else "90"
                return f"moveServo({dev}, {angle});"
            if action == "sweepServo":
                start_angle = args[0] if len(args) > 0 else "0"
                end_angle   = args[1] if len(args) > 1 else "180"
                step        = args[2] if len(args) > 2 else "1"
                delay_ms    = args[3] if len(args) > 3 else "15"
                return f"sweepServo({dev},{start_angle},{end_angle},{step},{delay_ms});"
            return f"// Servo needs Servo.h attached and servo.attach({pin});"

        # LCD / DISPLAY
        if dev_type in ["LCD", "DISPLAY"]:
            if action == "display":
                text = args[0] if args else "\"\""
                return f"lcd.clear();\n  lcd.print(\"{text}\");"

        # BUZZER
        if dev_type == "BUZZER":
            if action == "beep":
                ms = args[0] if args else "1000"
                return f"tone({pin[0]}, {1000});\n  delay({ms});\n  noTone({pin[0]});"
            elif action == "off":
                return f"noTone({pin[0]});"


    # --------------------------
    # Delay
    # --------------------------
    @staticmethod
    def _translate_delay_action(node):
        ms = node.children[0].value
        return f"delay({ms});"

    # --------------------------
    # Expressions (Conditions)
    # --------------------------
    def _calc_con(self, node):
        res = ""
        if len(node.children) >= 2:
            if node.children[0].value == "deviceCall":
                res += self._device_call(node.children[0])
            else:
                res += self._calc_con(node.children[0])

        res += (" " + node.value + "")

        if len(node.children) >= 2:
            if node.children[1].value == "deviceCall":
                res += self._device_call(node.children[1])
            else:
                res += self._calc_con(node.children[1])

        return res

    def _device_call(self, node):
        dev = node.children[0].value
        meth = node.children[1].value
        device, pin = self.devices[dev]
        if dev in self.devices.keys():
            if meth == "getTemperature":
                return f"readTemperature({pin[0]})"
            elif meth == "getLight":
                return f"readLight({pin[0]})"
            elif meth == "getDistance":
                return f"readDistance({pin[0]}, {pin[1]})"
            elif meth == "isMotionDetected":
                return f"readMotion({pin[0]})"
            elif meth == 'getHumidity':
                return f"readHumidity({dev})"
            elif meth == 'readPotentiometer':
                return f"readPotentiometer({pin[0]})"
            elif meth == 'isPressed':
                return f"isPressed({pin[0]})"

    # --------------------------
    # Code Assembly
    # --------------------------
    def _assemble_code(self):
        setup_code = []
        out_code = []
        servo_setup = []
        includes = []
        helpers = []
        used_devices = set()

        for name, (dev_type, pin) in self.devices.items():
            used_devices.add(dev_type)

            if dev_type in ("LED", "RELAY", "BUZZER", "DIGITAL_OUTPUT"):
                setup_code.append(f"pinMode({pin[0]}, OUTPUT);")
            elif dev_type in ("MOTION_SENSOR", "DIGITAL_INPUT"):
                setup_code.append(f"pinMode({pin[0]}, INPUT);")
            elif dev_type == "BUTTON":
                setup_code.append(f"pinMode({pin[0]}, INPUT_PULLUP);")
            elif dev_type == "SERVO":
                if "#include <Servo.h>" not in includes:
                    includes.append("#include <Servo.h>")
                servo_setup.append(f"{name}.attach({pin[0]},1000,2000);")
                helpers.append(f"Servo {name};")
            elif dev_type == "LCD":
                if "#include <LiquidCrystal.h>" not in includes:
                    includes.append("#include <LiquidCrystal.h>")
                helpers.append(f"LiquidCrystal {name}({pin[0]}, {pin[1]}, {pin[2]}, {pin[3]}, {pin[4]}, {pin[5]}); // Adjust pins")
                setup_code.append(f"{name}.begin(16, 2);  // Initialize 16x2 LCD")
            elif dev_type in ("TEMPERATURE_SENSOR", "LIGHT_SENSOR", "MOTION_SENSOR", "POTENTIOMETER"):
                # out_code.append(f"const int {name} = {pin};")
                setup_code.append(f"pinMode({pin[0]}, INPUT);")
            elif dev_type == "ULTRASONIC_SENSOR":
                setup_code.append(f"pinMode({pin[0]}, OUTPUT);")
                setup_code.append(f"pinMode({pin[1]}, INPUT);")
            elif dev_type == "HUMIDITY_SENSOR":
                if "#include <DHT.h>" not in includes:
                    includes.append("#include <DHT.h>")
                helpers.append(f"DHT {name}({pin[0]}, DHT11);")
                setup_code.append(f"{name}.begin(); // Initialize DHT11 sensor")
            elif dev_type in ("TEMPERATURE_SENSOR", "POTENTIOMETER", "ANALOG_INPUT","BUTTON"):
                setup_code.append(f"// {dev_type} on pin {pin}")

        # Add helper sensor functions
        helper_functions = []

        if "TEMPERATURE_SENSOR" in used_devices:
            helper_functions.append("""
float readTemperature(int pin) {
  int v = analogRead(pin);
  float voltage = v * (5.0 / 1023.0);
  float value = voltage * 100.0; // LM35
  Serial.print("temperature: ");
  Serial.println(value);
  return value;
}""")

        if "POTENTIOMETER" in used_devices:
            helper_functions.append("""
float readPotentiometer(int pin) {
  int value = analogRead(pin);
  Serial.print("Potentiometer Value: ");
  Serial.println(value);
  return value;
}""")

        if "HUMIDITY_SENSOR" in used_devices:
            helper_functions.append("""
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
}""")

        if "SERVO" in used_devices:
            helper_functions.append("""
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
}""")

        if "BUTTON" in used_devices:
            helper_functions.append("""
bool isPressed(int pin) {
  if (digitalRead(pin) == LOW) {
    return true;
  } else {
    return false;
  }
}""")

        if "LIGHT_SENSOR" in used_devices:
            helper_functions.append("""
float readLight(int pin) {
  int value = analogRead(pin);
  Serial.print("light: ");
  Serial.println(value);
  return value; // 0 (dark) to 1023 (bright)
}""")

        if "ULTRASONIC_SENSOR" in used_devices:
            helper_functions.append("""
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
}""")

        if "MOTION_SENSOR" in used_devices:
            helper_functions.append("""
bool readMotion(int pirPin) {
int motion = digitalRead(pirPin);
if (motion == HIGH) {
Serial.println("Motion Detected!");
return true;
} else {
Serial.println("No Motion");
return false;
}
}""")

        # Add all used helper functions to helpers list
        if helper_functions:
            helpers.append('\n'.join(helper_functions))

        states_code = []
        for state, actions in self.states.items():
            body = "\n  ".join(actions)
            states_code.append(f"void state_{state}() {{\n  {body}\n}}")

        # ---- Group transitions by source ----
        grouped_transitions = defaultdict(list)
        for src, dst, cond in self.transitions:
            grouped_transitions[src].append((dst, cond))

        transition_code = ["void checkTransitions() {", "  switch(currentState) {"]

        for src, rules in grouped_transitions.items():
            transition_code.append(f"    case {src.upper()}:")
            for i, (dst, cond) in enumerate(rules):
                if i == 0:
                    transition_code.append(f"      if ({cond}) currentState = {dst.upper()};")
                else:
                    transition_code.append(f"      else if ({cond}) currentState = {dst.upper()};")
            transition_code.append("      break;")

        transition_code.append("  }")
        transition_code.append("}")

        return f"""
// Auto-generated Arduino code
{chr(10).join(includes)}

enum State {{ {", ".join(s.upper() for s in self.states.keys())} }};
State currentState = {list(self.states.keys())[0].upper()};

{chr(10).join(helpers)}

{joiner(out_code)}
void setup() {{
Serial.println("Starting Program ...");
Serial.begin(9600);
{joiner(setup_code)}
{joiner(servo_setup)}
}}

{joiner(states_code)}

{joiner(transition_code)}

void loop() {{
  checkTransitions();
  switch(currentState) {{
    {"".join(f"case {s.upper()}: state_{s}(); break;" for s in self.states.keys())}
  }}
  delay(200);
}}
"""


# -------------------------------
# CLI entrypoint
# -------------------------------
if __name__ == "__main__":
    import json
    from required_code_collection.astTree import AST

    if len(sys.argv) < 3:
        print("Usage: python code_generator.py <ast.json> <output.ino>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        ast_dict = json.load(f)
    ast = AST.from_dict(ast_dict)

    gen = CodeGenerator(ast)
    code = gen.generate()

    with open(sys.argv[2], "w") as f:
        f.write(code)
