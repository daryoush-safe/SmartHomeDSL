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
                "action_methods": ["on", "off", "toggle", "blink", "fade", "setBrightness"],
            },
            "BUTTON": {
                "device_type": "digital",
                "getter_methods": ["isPressed", "read"],
                "action_methods": [],
            },
            "SENSOR": {
                "device_type": "analog",
                "getter_methods": ["read"],
                "action_methods": [],
            },
            "RELAY": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["on", "off", "toggle"],
            },
            "SERVO": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["move", "set"],
            },
            "LCD": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["display", "set"],
            },
            "BUZZER": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["on", "off", "beep"],
            },
            "TEMPERATURE_SENSOR": {
                "device_type": "analog",
                "getter_methods": ["getTemperature", "read"],
                "action_methods": [],
            },
            "HUMIDITY_SENSOR": {
                "device_type": "analog",
                "getter_methods": ["getHumidity", "read"],
                "action_methods": [],
            },
            "MOTION_SENSOR": {
                "device_type": "digital",
                "getter_methods": ["isMotionDetected", "read"],
                "action_methods": [],
            },
            "LIGHT_SENSOR": {
                "device_type": "analog",
                "getter_methods": ["read", "getLight"],
                "action_methods": [],
            },
            "ULTRASONIC_SENSOR": {
                "device_type": "digital",
                "getter_methods": ["getDistance", "read"],
                "action_methods": [],
            },
            "RGB_LED": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["setColor", "on", "off", "fade", "blink", "setBrightness"],
            },
            "STEPPER_MOTOR": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["move", "set"],
            },
            "PWM_OUTPUT": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["write", "set"],
            },
            "DIGITAL_INPUT": {
                "device_type": "digital",
                "getter_methods": ["read"],
                "action_methods": [],
            },
            "DIGITAL_OUTPUT": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["write", "on", "off", "toggle"],
            },
            "ANALOG_INPUT": {
                "device_type": "analog",
                "getter_methods": ["read"],
                "action_methods": [],
            },
            "ANALOG_OUTPUT": {
                "device_type": "analog",
                "getter_methods": [],
                "action_methods": ["write"],
            },
            "POTENTIOMETER": {
                "device_type": "analog",
                "getter_methods": ["read"],
                "action_methods": [],
            },
            "DISPLAY": {
                "device_type": "digital",
                "getter_methods": [],
                "action_methods": ["display", "set"],
            },
        }

        # key: device name, value: device type
        self.devices_lookup = {}
        # declared states
        self.states_lookup = ['*']

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

        declared_pins = []
        for i in range(4, ctx.getChildCount()):
            child = ctx.getChild(i)
            if hasattr(child, 'getText') and child.getText().isdigit():
                declared_pins.append(child.getText())

        if device_type not in self.devices:
            raise ValueError(f"Error: Device type '{device_type}' is not supported. "
                             f"Supported devices: {list(self.devices.keys())}")

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
        if ctx.getChild(0).getText() not in self.devices_lookup.keys():
            raise ValueError(f"Error: Device not declared")
        make_ast_subtree(self.ast, ctx, "device_action", keep_node=True)

    def exitDeviceType(self, ctx:SmartHomeStateMachineParser.DeviceTypeContext):
        device = ctx.getChild(0).getText()
        if device not in self.devices.keys():
            raise ValueError(f"Error: Device type '{device}' is not supported. "
                            f"Available types are: {', '.join(self.devices.keys())}")

    def exitGetterMethod(self, ctx:SmartHomeStateMachineParser.GetterMethodContext):
        method = ctx.getChild(0).getText()
        device = ctx.parentCtx.getChild(0).getText()
        if device not in self.devices_lookup.keys() :
            raise ValueError(f"Error: Device not declared")
        if method not in self.devices[self.devices_lookup[device]]["getter_methods"] :
            raise ValueError(f"Error: Getter method '{method}' is not supported for '{self.devices_lookup[device]}'. ")

    def exitActionMethod(self, ctx:SmartHomeStateMachineParser.GetterMethodContext):
        method = ctx.getChild(0).getText()
        device = ctx.parentCtx.getChild(0).getText()
        if device not in self.devices_lookup.keys() :
            raise ValueError(f"Error: Device not declared")
        if method not in self.devices[self.devices_lookup[device]]["action_methods"] :
            raise ValueError(f"Error: Action method '{method}' is not supported for '{self.devices_lookup[device]}'. ")
