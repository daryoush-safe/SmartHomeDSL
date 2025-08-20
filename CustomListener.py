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
        ]

        # Rules that create a new scope or block
        self.scoped_rules = [
            'program',
            'stateDeclaration',
            'transitionDeclaration',
            'deviceDeclaration',
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

    def exitDeviceDeclaration(self, ctx:SmartHomeStateMachineParser.DeviceDeclarationContext):
        make_ast_subtree(self.ast, ctx, "device_dec", keep_node=True)

    def exitStateDeclaration(self, ctx:SmartHomeStateMachineParser.StateDeclarationContext):
        make_ast_subtree(self.ast, ctx, "state_dec", keep_node=True)

    def exitTransitionDeclaration(self, ctx:SmartHomeStateMachineParser.TransitionDeclarationContext):
        make_ast_subtree(self.ast, ctx, "transition_dec", keep_node=True)

    def exitDelayAction(self, ctx:SmartHomeStateMachineParser.DelayActionContext):
        make_ast_subtree(self.ast, ctx, "delay_action", keep_node=True)

    def exitDeviceAction(self, ctx:SmartHomeStateMachineParser.DeviceActionContext):
        make_ast_subtree(self.ast, ctx, "device_action", keep_node=True)