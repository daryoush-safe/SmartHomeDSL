grammar SmartHomeStateMachine;

// Parser Rules
program
    : (deviceDeclaration | stateDeclaration | transitionDeclaration)* EOF
    ;

// Device Declarations
deviceDeclaration
    : 'device' deviceName ':' deviceType ('pin' pinDeclaration)?';'
    ;

deviceName
    : IDENTIFIER
    ;

pinDeclaration
    : NUMBER
    ;

deviceType
    : IDENTIFIER
    ;

// State Declarations
stateDeclaration
    : 'state' stateName '{' (action (',' action)*)? '}'
    ;

stateName
    : IDENTIFIER
    ;

action
    : deviceAction
    | delayAction
    | variableAssignment
    ;

deviceAction : deviceName '.' actionMethod '(' (expression (',' expression)*)? ')'
             | deviceName '.' getterMethod '(' ')'
             ;

actionMethod :
    IDENTIFIER
    ;
getterMethod :
    IDENTIFIER
    ;

delayAction
    : 'delay' '(' delayParameter ')'
    ;

delayParameter
    : NUMBER
    ;

variableAssignment
    : variableName '=' expression
    ;

variableName
    : IDENTIFIER
    ;

// Transition Declarations
transitionDeclaration
    : 'transition' (stateName | allStates) '->' stateName 'when' condition ';'
    ;

allStates
    : '*'
    ;

condition
    : expression
    ;

expression
    : expression '||' andExpression
    | andExpression
    ;

andExpression
    : andExpression '&&' comparisonExpression
    | comparisonExpression
    ;

comparisonExpression
    : comparisonExpression ('==' | '!=' | '<' | '>' | '<=' | '>=') arithmeticExpression
    | arithmeticExpression
    ;

arithmeticExpression
    : arithmeticExpression ('+' | '-') term
    | term
    ;

term
    : term ('*' | '/' | '%') factor
    | factor
    ;

factor
    : '!' factor
    | '(' expression ')'
    | deviceCall
    | IDENTIFIER
    | NUMBER
    | STRING
    | BOOLEAN
    ;

deviceCall
    : deviceName '.' getterMethod '(' (expression (',' expression)*)? ')'
    ;

// Lexer Rules
// Keywords
DEVICE      : 'device';
STATE       : 'state';
TRANSITION  : 'transition';
WHEN        : 'when';
PIN         : 'pin';
ADDRESS     : 'address';
DELAY       : 'delay';

// Device Types (already defined in deviceType rule)

// Operators
ASSIGN      : '=';
ARROW       : '->';
DOT         : '.';
SEMICOLON   : ';';
COMMA       : ',';
LPAREN      : '(';
RPAREN      : ')';
LBRACE      : '{';
RBRACE      : '}';
COLON       : ':';

// Logical Operators
AND         : '&&';
OR          : '||';
NOT         : '!';

// Comparison Operators
EQ          : '==';
NE          : '!=';
LT          : '<';
GT          : '>';
LE          : '<=';
GE          : '>=';

// Arithmetic Operators
PLUS        : '+';
MINUS       : '-';
MULTIPLY    : '*';
DIVIDE      : '/';
MODULO      : '%';

// Literals
NUMBER      : [0-9]+ ('.' [0-9]+)?;
STRING      : '"' (~["\r\n] | '""')* '"';
BOOLEAN     : 'true' | 'false';
IDENTIFIER  : [a-zA-Z_][a-zA-Z0-9_]*;

// Whitespace and Comments
WS          : [ \t\r\n]+ -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;