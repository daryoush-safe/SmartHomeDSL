from gen.SmartHomeStateMachineListener import SmartHomeStateMachineListener
from gen.SmartHomeStateMachineParser import SmartHomeStateMachineParser
from required_code_collection.astTree import AST
from required_code_collection.make_ast_subtree import make_ast_subtree


class CustomListener(SmartHomeStateMachineListener):
    def __init__(self):
        # Rules where we override default AST handling
        self.overridden_rules = [
            'program',
            'stateDeclaration',
            'transitionDeclaration',
            'deviceDeclaration',
            'deviceAction',
            'delayAction',
        ]

        # Rules with binary operators (handled specially in AST)
        self.binary_operator_list = [
            'expression',
            'variableAssignment',
            'andExpression',
            'comparisonExpression',
            'arithmeticExpression',
            'term'
        ]

        # Rules that create a new scope or block
        self.scoped_rules = [
            'program',
            'stateDeclaration',
            'transitionDeclaration',
            'deviceDeclaration',
        ]
        # all possible devices

        self.devices = {
            "LED": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["on", "off", "toggle", "blink", "setBrightness"],
                "expected_pins": 1,
                "method_args": {
                    "on": {"count": 0},
                    "off": {"count": 0},
                    "toggle": {"count": 0},
                    "blink": {
                        "count": 1,
                        "args": [
                            {"type": "int", "range": [1, 1000]},
                        ]
                    },
                    "setBrightness": {
                        "count": 1,
                        "args": [
                            {"type": "int", "range": [0, 255]},
                        ],
                    },
                },
            },
            "BUTTON": {
                "device_type": "digital",
                "getter_methods": ["isPressed"],
                "action_methods": [],
                "expected_pins": 1,
                "method_args": {
                    "isPressed": {"count": 0},
                },
            },
            "SERVO": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["moveServo", "sweepServo"],
                "expected_pins": 1,
                "method_args": {
                    "moveServo": {
                        "count": 1,
                        "args": [
                            {"type": "int", "range": [0, 180]},
                        ],
                    },
                    "sweepServo": {
                        "count": 4,
                        "args": [
                            {"type": "int", "range": [0, 180]},   # start_andle
                            {"type": "int", "range": [0, 180]},   # end_angle
                            {"type": "int", "range": [1, 180]},   # step
                            {"type": "int", "range": [1, 1000]},  # delay_ms
                        ],
                    },
                },
            },
            # TODO
            "LCD": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["display"],
                "expected_pins": 6,
                "method_args": {
                    "display": {
                        "count": 1,
                        "args": [
                            {"type": "string"},
                        ],
                    },
                },
            },
            "BUZZER": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["off", "beep"],
                "expected_pins": 1,
                "method_args": {
                    "off": {"count": 0},
                    "beep": {
                        "count": 1,
                        "args": [
                            {"type": "int", "range": [1, 1000]},
                        ],
                    },
                },
            },
            "TEMPERATURE_SENSOR": {
                "device_type": "analog",
                "getter_methods": ["getTemperature"],
                "action_methods": [],
                "expected_pins": 1,
                "method_args": {
                    "getTemperature": {"count": 0},
                },
            },
            "HUMIDITY_SENSOR": {
                "device_type": "analog",
                "getter_methods": ["getHumidity"],
                "action_methods": [],
                "expected_pins": 1,
                "method_args": {
                    "getHumidity": {"count": 0},
                },
            },
            "MOTION_SENSOR": {
                "device_type": "digital",
                "getter_methods": ["isMotionDetected"],
                "action_methods": [],
                "expected_pins": 1,
                "method_args": {
                    "isMotionDetected": {"count": 0},
                },
            },
            "LIGHT_SENSOR": {
                "device_type": "analog",
                "getter_methods": ["getLight"],
                "action_methods": [],
                "expected_pins": 1,
                "method_args": {
                    "getLight": {"count": 0},
                },
            },
            "ULTRASONIC_SENSOR": {
                "device_type": "digital",
                "getter_methods": ["getDistance"],
                "action_methods": [],
                "expected_pins": 2,
                "method_args": {
                    "getDistance": {"count": 0},
                },
            },
            "RGB_LED": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["setColor"],
                "expected_pins": 3,
                "method_args": {
                    "setColor": {
                        "count": 3,
                        "args": [
                            {"type": "int", "range": [0, 255]},
                            {"type": "int", "range": [0, 255]},
                            {"type": "int", "range": [0, 255]},
                        ],
                    },
                },
            },
            "POTENTIOMETER": {
                "device_type": "analog",
                "getter_methods": ["readPotentiometer"],
                "action_methods": [],
                "expected_pins": 1,
                "method_args": {
                    "readPotentiometer": {"count": 0},
                },
            },
            "DISPLAY": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["display"],
                "expected_pins": 6,
                "method_args": {
                    "display": {
                        "count": 1,
                        "args": [
                            {"type": "string"},
                        ],
                    },
                },
            },
        }

        # key: device name, value: device type
        self.devices_lookup = {}
        # declared states
        self.states_lookup = ['*']
        # declared pins
        self.pins_lookup = []

        # list of analog pins for analog devices
        self.analog_pins = [
            '14', '15', '16', '17', '18', '19',
        ]
        
        # list of digital pins for digital devices
        self.digital_pins = [
            '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
        ]

        self.rule_names = []
        self.ast = AST()

    def exitEveryRule(self, ctx):
        rule_name = self.rule_names[ctx.getRuleIndex()]
        if rule_name in self.scoped_rules:
            ctx.compound = True
        if rule_name not in self.overridden_rules:
            if rule_name in self.binary_operator_list and ctx.getChildCount() > 1:
                make_ast_subtree(self.ast, ctx, ctx.getChild(1).getText())
            else:
                make_ast_subtree(self.ast, ctx, rule_name)

    def exitProgram(self, ctx):
        make_ast_subtree(self.ast, ctx, "program", keep_node=True)

    def exitDeviceDeclaration(self, ctx: SmartHomeStateMachineParser.DeviceDeclarationContext):
        device_name = ctx.getChild(1).getText()
        device_type = ctx.getChild(3).getText()

        if device_name in self.devices_lookup:
            raise ValueError(f"Device {device_name} is already declared.")

        if device_type not in self.devices:
            raise ValueError(f"Error: Device type '{device_type}' is not supported. "
                             f"Supported devices: {list(self.devices.keys())}")

        declared_pins = []
        for i in range(4, ctx.getChildCount()):
            child = ctx.getChild(i)

            if hasattr(child, 'getText') and child.getText().isdigit():
                if child.getText() in self.pins_lookup:
                    raise ValueError(f"Pin {child.getText()} is already assigned.")
                self.pins_lookup.append(child.getText())
                declared_pins.append(child.getText())

        expected_pins = self.devices[device_type].get("expected_pins", 0)
        if len(declared_pins) != expected_pins:
            raise ValueError(
                f"Error: Device '{device_name}' of type '{device_type}' requires {expected_pins} pins, but {len(declared_pins)} were provided.")

        device_config = self.devices[device_type]
        device_pin_type = device_config["device_type"]

        if declared_pins:
            if device_pin_type == "analog":
                invalid_pins = [pin for pin in declared_pins if pin not in self.analog_pins]
                if invalid_pins:
                    raise ValueError(f"Error: Device '{device_name}' of type '{device_type}' is analog "
                                     f"but has invalid analog pins: {invalid_pins}. "
                                     f"Valid analog pins: {self.analog_pins}")

            elif device_pin_type == "digital":
                invalid_pins = [pin for pin in declared_pins if pin not in self.digital_pins]
                if invalid_pins:
                    raise ValueError(f"Error: Device '{device_name}' of type '{device_type}' is digital "
                                     f"but has invalid digital pins: {invalid_pins}. "
                                     f"Valid digital pins: {self.digital_pins}")

        make_ast_subtree(self.ast, ctx, "device_dec", keep_node=True)
        self.devices_lookup[ctx.getChild(1).getText()] = ctx.getChild(3).getText()

    def exitStateDeclaration(self, ctx:SmartHomeStateMachineParser.StateDeclarationContext):
        make_ast_subtree(self.ast, ctx, "state_dec", keep_node=True)
        self.states_lookup.append(ctx.getChild(1).getText())

    def exitTransitionDeclaration(self, ctx:SmartHomeStateMachineParser.TransitionDeclarationContext):
        if ((ctx.getChild(1).getText() not in self.states_lookup) or
            (ctx.getChild(3).getText() not in self.states_lookup)):
            raise ValueError("State not declared.")
        make_ast_subtree(self.ast, ctx, "transition_dec", keep_node=True)

    def exitDelayAction(self, ctx:SmartHomeStateMachineParser.DelayActionContext):
        make_ast_subtree(self.ast, ctx, "delay_action", keep_node=True)

    def exitDeviceAction(self, ctx:SmartHomeStateMachineParser.DeviceActionContext):
        device_name = ctx.getChild(0).getText()
        method_name = ctx.getChild(2).getText()

        if device_name not in self.devices_lookup.keys():
            raise ValueError(f"Error: Device not declared")

        method_config = self.devices[self.devices_lookup[device_name]]["method_args"].get(method_name,
                                                                                          {"count": 0, "args": []})
        expected_arg_count = method_config["count"]
        argument = ctx.getChildCount() - 5
        comma_length = argument // 2
        actual_arg_count = argument - comma_length

        if actual_arg_count != expected_arg_count:
            raise ValueError(
                f"Error: Method '{method_name}' on device '{device_name}' expects {expected_arg_count} arguments, but {actual_arg_count} were provided.")

        if actual_arg_count == 0:
            return

        method_args = method_config.get("args", [])
        for i in range(actual_arg_count):
            arg_text = ctx.getChild(2 * i + 4).getText()
            arg_type = method_args[i].get("type")
            arg_range = method_args[i].get("range")

            try:
                if arg_type == "int":
                    arg_value = int(arg_text)
                elif arg_type == "float":
                    arg_value = float(arg_text)
                else:
                    continue

                if arg_range and (arg_value < arg_range[0] or arg_value > arg_range[1]):
                    raise ValueError(
                        f"Error: Argument {i + 1} of '{method_name}' on device '{device_name}' must be in range {arg_range}, got {arg_value}.")
            except ValueError:
                raise ValueError(
                    f"Error: Argument {i + 1} of '{method_name}' on device '{device_name}' must be a valid {arg_type}, got '{arg_text}'.")

        make_ast_subtree(self.ast, ctx, "device_action", keep_node=True)

    def exitDeviceType(self, ctx:SmartHomeStateMachineParser.DeviceTypeContext):
        device = ctx.getChild(0).getText()
        if device not in self.devices.keys():
            raise ValueError(f"Error: Device type '{device}' is not supported. "
                            f"Available types are: {', '.join(self.devices.keys())}")


    def exitDeviceCall(self, ctx:SmartHomeStateMachineParser.DeviceCallContext):
        device_name = ctx.getChild(0).getText()
        method_name = ctx.getChild(2).getText()

        method_config = self.devices[self.devices_lookup[device_name]]["method_args"].get(method_name, {"count": 0, "args": []})
        expected_arg_count = method_config["count"]
        argument = ctx.getChildCount() - 5
        comma_length = argument // 2
        actual_arg_count = argument - comma_length

        if actual_arg_count != expected_arg_count:
            raise ValueError(
                f"Error: Method '{method_name}' on device '{device_name}' expects {expected_arg_count} arguments, but {actual_arg_count} were provided.")

        if actual_arg_count == 0:
            return

        method_args = method_config.get("args", [])
        for i in range(actual_arg_count):
            arg_text = ctx.getChild(2 * i + 4)
            arg_type = method_args[i].get("type")
            arg_range = method_args[i].get("range")

            try:
                if arg_type == "int":
                    arg_value = int(arg_text)
                elif arg_type == "float":
                    arg_value = float(arg_text)
                else:
                    continue

                if arg_range and (arg_value < arg_range[0] or arg_value > arg_range[1]):
                    raise ValueError(
                        f"Error: Argument {i + 1} of '{method_name}' on device '{device_name}' must be in range {arg_range}, got {arg_value}.")
            except ValueError:
                raise ValueError(
                    f"Error: Argument {i + 1} of '{method_name}' on device '{device_name}' must be a valid {arg_type}, got '{arg_text}'.")

    def exitGetterMethod(self, ctx:SmartHomeStateMachineParser.GetterMethodContext):
        method = ctx.getChild(0).getText()
        device = ctx.parentCtx.getChild(0).getText()
        if device not in self.devices_lookup.keys():
            raise ValueError(f"Error: Device not declared")
        if method not in self.devices[self.devices_lookup[device]]["getter_methods"]:
            raise ValueError(f"Error: Getter method '{method}' is not supported for '{self.devices_lookup[device]}'. ")

    def exitActionMethod(self, ctx:SmartHomeStateMachineParser.GetterMethodContext):
        method = ctx.getChild(0).getText()
        device = ctx.parentCtx.getChild(0).getText()
        if device not in self.devices_lookup.keys():
            raise ValueError(f"Error: Device not declared")
        if method not in self.devices[self.devices_lookup[device]]["action_methods"]:
            raise ValueError(f"Error: Action method '{method}' is not supported for '{self.devices_lookup[device]}'. ")
