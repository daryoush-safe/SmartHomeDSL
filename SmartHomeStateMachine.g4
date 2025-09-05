grammar SmartHomeStateMachine;

// Parser Rules
program
    : (deviceDeclaration | stateDeclaration | transitionDeclaration)* EOF
    ;

// Device Declarations
deviceDeclaration
    : 'device' deviceName ':' deviceType ('pin' pinDeclaration)? (',' 'pin' pinDeclaration)*';'
    ;

deviceName
    : IDENTIFIER
    ;

pinDeclaration
    : NUMBER
    ;

deviceType
    : 'LED'
    | 'BUTTON'
//    | 'SENSOR'
    | 'RELAY'
    | 'SERVO'
    | 'LCD'
    | 'BUZZER'
    | 'TEMPERATURE_SENSOR'
    | 'HUMIDITY_SENSOR'
    | 'MOTION_SENSOR'
    | 'LIGHT_SENSOR'
    | 'ULTRASONIC_SENSOR'
//    | 'RGB_LED'
    | 'STEPPER_MOTOR'
    | 'PWM_OUTPUT'
    | 'DIGITAL_INPUT'
    | 'DIGITAL_OUTPUT'
    | 'ANALOG_INPUT'
    | 'ANALOG_OUTPUT'
    | 'POTENTIOMETER'
    | 'DISPLAY'
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

actionMethod : 'on' | 'off' | 'toggle' | 'set' | 'write' | 'move' | 'display'
             | 'beep' | 'fade' | 'blink' | 'setColor' | 'setBrightness'
             ;

getterMethod : 'read' | 'getDistance' | 'getTemperature' | 'getHumidity'
             | 'isPressed' | 'isMotionDetected' | 'getLight'
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