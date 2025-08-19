# Generated from C:/compiler_project/SmartHomeStateMachine.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SmartHomeStateMachineParser import SmartHomeStateMachineParser
else:
    from SmartHomeStateMachineParser import SmartHomeStateMachineParser

# This class defines a complete generic visitor for a parse tree produced by SmartHomeStateMachineParser.

class SmartHomeStateMachineVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SmartHomeStateMachineParser#program.
    def visitProgram(self, ctx:SmartHomeStateMachineParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#deviceDeclaration.
    def visitDeviceDeclaration(self, ctx:SmartHomeStateMachineParser.DeviceDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#deviceType.
    def visitDeviceType(self, ctx:SmartHomeStateMachineParser.DeviceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#stateDeclaration.
    def visitStateDeclaration(self, ctx:SmartHomeStateMachineParser.StateDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#actionList.
    def visitActionList(self, ctx:SmartHomeStateMachineParser.ActionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#action.
    def visitAction(self, ctx:SmartHomeStateMachineParser.ActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#deviceAction.
    def visitDeviceAction(self, ctx:SmartHomeStateMachineParser.DeviceActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#deviceMethod.
    def visitDeviceMethod(self, ctx:SmartHomeStateMachineParser.DeviceMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#delayAction.
    def visitDelayAction(self, ctx:SmartHomeStateMachineParser.DelayActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#variableAssignment.
    def visitVariableAssignment(self, ctx:SmartHomeStateMachineParser.VariableAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#transitionDeclaration.
    def visitTransitionDeclaration(self, ctx:SmartHomeStateMachineParser.TransitionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#condition.
    def visitCondition(self, ctx:SmartHomeStateMachineParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#expression.
    def visitExpression(self, ctx:SmartHomeStateMachineParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#deviceCall.
    def visitDeviceCall(self, ctx:SmartHomeStateMachineParser.DeviceCallContext):
        return self.visitChildren(ctx)



del SmartHomeStateMachineParser