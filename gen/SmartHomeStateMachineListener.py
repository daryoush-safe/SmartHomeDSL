# Generated from C:/University/compiler/SmartHomeDSL/SmartHomeStateMachine.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SmartHomeStateMachineParser import SmartHomeStateMachineParser
else:
    from SmartHomeStateMachineParser import SmartHomeStateMachineParser

# This class defines a complete listener for a parse tree produced by SmartHomeStateMachineParser.
class SmartHomeStateMachineListener(ParseTreeListener):

    # Enter a parse tree produced by SmartHomeStateMachineParser#program.
    def enterProgram(self, ctx:SmartHomeStateMachineParser.ProgramContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#program.
    def exitProgram(self, ctx:SmartHomeStateMachineParser.ProgramContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#deviceDeclaration.
    def enterDeviceDeclaration(self, ctx:SmartHomeStateMachineParser.DeviceDeclarationContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#deviceDeclaration.
    def exitDeviceDeclaration(self, ctx:SmartHomeStateMachineParser.DeviceDeclarationContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#deviceName.
    def enterDeviceName(self, ctx:SmartHomeStateMachineParser.DeviceNameContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#deviceName.
    def exitDeviceName(self, ctx:SmartHomeStateMachineParser.DeviceNameContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#pinDeclaration.
    def enterPinDeclaration(self, ctx:SmartHomeStateMachineParser.PinDeclarationContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#pinDeclaration.
    def exitPinDeclaration(self, ctx:SmartHomeStateMachineParser.PinDeclarationContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#deviceType.
    def enterDeviceType(self, ctx:SmartHomeStateMachineParser.DeviceTypeContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#deviceType.
    def exitDeviceType(self, ctx:SmartHomeStateMachineParser.DeviceTypeContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#stateDeclaration.
    def enterStateDeclaration(self, ctx:SmartHomeStateMachineParser.StateDeclarationContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#stateDeclaration.
    def exitStateDeclaration(self, ctx:SmartHomeStateMachineParser.StateDeclarationContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#actionList.
    def enterActionList(self, ctx:SmartHomeStateMachineParser.ActionListContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#actionList.
    def exitActionList(self, ctx:SmartHomeStateMachineParser.ActionListContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#action.
    def enterAction(self, ctx:SmartHomeStateMachineParser.ActionContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#action.
    def exitAction(self, ctx:SmartHomeStateMachineParser.ActionContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#deviceAction.
    def enterDeviceAction(self, ctx:SmartHomeStateMachineParser.DeviceActionContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#deviceAction.
    def exitDeviceAction(self, ctx:SmartHomeStateMachineParser.DeviceActionContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#deviceMethod.
    def enterDeviceMethod(self, ctx:SmartHomeStateMachineParser.DeviceMethodContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#deviceMethod.
    def exitDeviceMethod(self, ctx:SmartHomeStateMachineParser.DeviceMethodContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#delayAction.
    def enterDelayAction(self, ctx:SmartHomeStateMachineParser.DelayActionContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#delayAction.
    def exitDelayAction(self, ctx:SmartHomeStateMachineParser.DelayActionContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#variableAssignment.
    def enterVariableAssignment(self, ctx:SmartHomeStateMachineParser.VariableAssignmentContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#variableAssignment.
    def exitVariableAssignment(self, ctx:SmartHomeStateMachineParser.VariableAssignmentContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#transitionDeclaration.
    def enterTransitionDeclaration(self, ctx:SmartHomeStateMachineParser.TransitionDeclarationContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#transitionDeclaration.
    def exitTransitionDeclaration(self, ctx:SmartHomeStateMachineParser.TransitionDeclarationContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#condition.
    def enterCondition(self, ctx:SmartHomeStateMachineParser.ConditionContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#condition.
    def exitCondition(self, ctx:SmartHomeStateMachineParser.ConditionContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#expression.
    def enterExpression(self, ctx:SmartHomeStateMachineParser.ExpressionContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#expression.
    def exitExpression(self, ctx:SmartHomeStateMachineParser.ExpressionContext):
        pass


    # Enter a parse tree produced by SmartHomeStateMachineParser#deviceCall.
    def enterDeviceCall(self, ctx:SmartHomeStateMachineParser.DeviceCallContext):
        pass

    # Exit a parse tree produced by SmartHomeStateMachineParser#deviceCall.
    def exitDeviceCall(self, ctx:SmartHomeStateMachineParser.DeviceCallContext):
        pass



del SmartHomeStateMachineParser