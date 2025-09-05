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
        if len(node.children) > 2:
            if int(node.children[-1].value) <= 13:
                pin = node.children[-1].value
            else:
                pin = f"A{int(node.children[-1].value) - 14}"
        self.devices[name] = (dev_type, pin)

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

        # LED / DIGITAL_OUTPUT
        if dev_type in ["LED", "DIGITAL_OUTPUT"]:
            if action == "on":
                return f"digitalWrite({pin}, HIGH);"
            elif action == "off":
                return f"digitalWrite({pin}, LOW);"
            elif action == "toggle":
                return f"digitalWrite({pin}, !digitalRead({pin}));"
            elif action == "blink":
                delay_ms = args[0] if args else "500"
                return f"digitalWrite({pin}, !digitalRead({pin})); delay({delay_ms});"

        if dev_type == "RGB_LED":
            if action == "setColor":
                r, g, b = args if len(args) == 3 else ("255", "255", "255")
                return f"analogWrite({pin}, {r}); // Simplified RGB (expand for multiple pins)"

        # BUTTON / DIGITAL_INPUT
        if dev_type in ["BUTTON", "DIGITAL_INPUT"]:
            return f"// {dev} actions handled via getters"

        # RELAY
        if dev_type == "RELAY":
            return f"digitalWrite({pin}, {'HIGH' if action == 'on' else 'LOW'});"

        # SERVO
        if dev_type == "SERVO":
            if action == "move":
                angle = args[0] if args else "90"
                return f"{dev}.write({angle});"
            return f"// Servo needs Servo.h attached and servo.attach({pin});"

        # LCD / DISPLAY
        if dev_type in ["LCD", "DISPLAY"]:
            if action == "display":
                text = args[0] if args else "\"\""
                return f"{dev}.print({text});"

        # BUZZER
        if dev_type == "BUZZER":
            if action == "beep":
                freq = args[0] if args else "1000"
                return f"tone({pin}, {freq});"
            elif action == "off":
                return f"noTone({pin});"

        # PWM_OUTPUT / ANALOG_OUTPUT
        if dev_type in ["PWM_OUTPUT", "ANALOG_OUTPUT"]:
            if action in ["write", "setBrightness", "fade"]:
                val = args[0] if args else "128"
                return f"analogWrite({pin}, {val});"

        return f"// Unknown device action {dev}.{action}"

    # --------------------------
    # Delay
    # --------------------------
    def _translate_delay_action(self, node):
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
        if dev in self.devices.keys():
            if meth == "getTemperature":
                return f"readTemperature({dev})"
            elif meth == "getLight":
                return f"readLight({dev})"

            raise ValueError(f"method {meth} is not define.")
        else:
            raise ValueError(f"device {dev} is not define.")

    # --------------------------
    # Code Assembly
    # --------------------------
    def _assemble_code(self):
        setup_code = []
        out_code = []
        servo_setup = []
        includes = []
        helpers = []

        for name, (dev_type, pin) in self.devices.items():
            if dev_type in ("LED", "RELAY", "BUZZER", "DIGITAL_OUTPUT"):
                setup_code.append(f"pinMode({pin}, OUTPUT);")
            elif dev_type in ("BUTTON", "MOTION_SENSOR", "DIGITAL_INPUT"):
                setup_code.append(f"pinMode({pin}, INPUT);")
            elif dev_type == "SERVO":
                includes.append("#include <Servo.h>")
                servo_setup.append(f"{name}.attach({pin});")
                helpers.append(f"Servo {name};")
            elif dev_type == "LCD":
                includes.append("#include <LiquidCrystal.h>")
                helpers.append(f"LiquidCrystal {name}(12, 11, 5, 4, 3, 2); // Adjust pins")
            elif dev_type == "TEMPERATURE_SENSOR":
                out_code.append(f"const int {name} = {pin};")
            elif dev_type == "LIGHT_SENSOR":
                out_code.append(f"const int {name} = {pin};")
            elif dev_type in ("TEMPERATURE_SENSOR", "HUMIDITY_SENSOR", "LIGHT_SENSOR", "POTENTIOMETER", "ANALOG_INPUT"):
                setup_code.append(f"// {dev_type} on pin {pin}")

        # Add helper sensor functions
        helpers.append("""
float readTemperature(int pin) {
  int v = analogRead(pin);
  float voltage = v * (5.0 / 1023.0);
  float value =  voltage * 100.0; // LM35
  Serial.println("measured temperature: ");
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
  Serial.println("measured light: ");
  Serial.println(value);
  return value; // 0 (dark) to 1023 (bright)
}
""")

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
