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

        # List of analog device types
        self.analog_devices = [
            'TEMPERATURE_SENSOR',
            'LIGHT_SENSOR',
            'MOTION_SENSOR',
            'ULTRASONIC_SENSOR',
            'HUMIDITY_SENSOR',
        ]

        # list of analog pins for analog devices
        self.analog_pins = [
            '14', '15', '16', '17', '18', '19',
        ]

        # List of digital device types
        self.digital_devices = [
            'LED',
            'BUTTON',
            'SENSOR',
            'RELAY',
            'SERVO',
            'LCD',
            'BUZZER',
            'RGB_LED',
            'STEPPER_MOTOR',
            'PWM_OUTPUT',
            'DIGITAL_INPUT',
            'DIGITAL_OUTPUT',
            'ANALOG_INPUT',
            'ANALOG_OUTPUT',
            'POTENTIOMETER',
            'DISPLAY',
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
        if ctx.getChildCount() > 4:
            device_type = ctx.getChild(3).getText()
            pin_number = None
            for i in range(ctx.getChildCount()):
                if ctx.getChild(i).getText() == 'pin' and i + 1 < ctx.getChildCount():
                    pin_number = ctx.getChild(i + 1).getText()
                    break

            if pin_number is not None:
                if (device_type in self.analog_devices and pin_number not in self.analog_pins):
                    raise ValueError(
                        f"Analog device '{device_type}' is not compatible with pin '{pin_number}'. Use analog pins: {', '.join(self.analog_pins)}")

                elif (device_type in self.digital_devices and pin_number not in self.digital_pins):
                    raise ValueError(
                        f"Digital device '{device_type}' is not compatible with pin '{pin_number}'. Use digital pins: {', '.join(self.digital_pins)}")

        make_ast_subtree(self.ast, ctx, "device_dec", keep_node=True)

    def exitStateDeclaration(self, ctx:SmartHomeStateMachineParser.StateDeclarationContext):
        make_ast_subtree(self.ast, ctx, "state_dec", keep_node=True)

    def exitTransitionDeclaration(self, ctx:SmartHomeStateMachineParser.TransitionDeclarationContext):
        make_ast_subtree(self.ast, ctx, "transition_dec", keep_node=True)

    def exitDelayAction(self, ctx:SmartHomeStateMachineParser.DelayActionContext):
        make_ast_subtree(self.ast, ctx, "delay_action", keep_node=True)

    def exitDeviceAction(self, ctx:SmartHomeStateMachineParser.DeviceActionContext):
        make_ast_subtree(self.ast, ctx, "device_action", keep_node=True)