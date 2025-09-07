# Generated from C:/compiler_project/dev/SmartHomeDSL/SmartHomeStateMachine.g4 by ANTLR 4.13.2
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


    # Visit a parse tree produced by SmartHomeStateMachineParser#deviceName.
    def visitDeviceName(self, ctx:SmartHomeStateMachineParser.DeviceNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#pinDeclaration.
    def visitPinDeclaration(self, ctx:SmartHomeStateMachineParser.PinDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#deviceType.
    def visitDeviceType(self, ctx:SmartHomeStateMachineParser.DeviceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#stateDeclaration.
    def visitStateDeclaration(self, ctx:SmartHomeStateMachineParser.StateDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#stateName.
    def visitStateName(self, ctx:SmartHomeStateMachineParser.StateNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#action.
    def visitAction(self, ctx:SmartHomeStateMachineParser.ActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#deviceAction.
    def visitDeviceAction(self, ctx:SmartHomeStateMachineParser.DeviceActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#actionMethod.
    def visitActionMethod(self, ctx:SmartHomeStateMachineParser.ActionMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#getterMethod.
    def visitGetterMethod(self, ctx:SmartHomeStateMachineParser.GetterMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#delayAction.
    def visitDelayAction(self, ctx:SmartHomeStateMachineParser.DelayActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#delayParameter.
    def visitDelayParameter(self, ctx:SmartHomeStateMachineParser.DelayParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#variableAssignment.
    def visitVariableAssignment(self, ctx:SmartHomeStateMachineParser.VariableAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#variableName.
    def visitVariableName(self, ctx:SmartHomeStateMachineParser.VariableNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#transitionDeclaration.
    def visitTransitionDeclaration(self, ctx:SmartHomeStateMachineParser.TransitionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#allStates.
    def visitAllStates(self, ctx:SmartHomeStateMachineParser.AllStatesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#condition.
    def visitCondition(self, ctx:SmartHomeStateMachineParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#expression.
    def visitExpression(self, ctx:SmartHomeStateMachineParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#andExpression.
    def visitAndExpression(self, ctx:SmartHomeStateMachineParser.AndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#comparisonExpression.
    def visitComparisonExpression(self, ctx:SmartHomeStateMachineParser.ComparisonExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#arithmeticExpression.
    def visitArithmeticExpression(self, ctx:SmartHomeStateMachineParser.ArithmeticExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#term.
    def visitTerm(self, ctx:SmartHomeStateMachineParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#factor.
    def visitFactor(self, ctx:SmartHomeStateMachineParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SmartHomeStateMachineParser#deviceCall.
    def visitDeviceCall(self, ctx:SmartHomeStateMachineParser.DeviceCallContext):
        return self.visitChildren(ctx)



del SmartHomeStateMachineParser