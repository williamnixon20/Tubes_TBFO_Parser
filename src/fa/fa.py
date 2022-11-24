class __FA:
    def __init__(self, name, startState: str, finalState, transition):
        self.name = name
        self.startState = startState
        self.finalState = finalState
        self.transition = transition

    def evaluate(self, inputs: str):
        currentState = self.startState
        for symbol in inputs:
            print(self.name, currentState, symbol)
            currentState = self.transition(currentState, symbol)
            if not currentState:
                break
        return currentState in self.finalState


def __isAlpha(symbol: str):
    return ('a' <= symbol <= 'z') or ('A' <= symbol <= 'Z')


def __isDigit(symbol: str):
    return ('0' <= symbol <= '9')


def __transitionFAVariable(state: str, symbol: str):
    if state == 'q0':
        if __isAlpha(symbol) or (symbol == '$') or (symbol == '_'):
            return 'qf'
        else:
            return 'qd'
    elif state == 'qf':
        if __isAlpha(symbol) or (symbol == '$') or (symbol == '_') or __isDigit(symbol):
            return 'qf'
        elif symbol == '.':
            return 'q0'
        else:
            return 'qd'


def __transitionFANumber(state: str, symbol: str):
    if state == 'q0':
        if __isDigit(symbol):
            return 'q1'
        elif symbol == '.':
            return 'q2'
    elif state == 'q1':
        if __isDigit(symbol):
            return 'q1'
        elif symbol == '.':
            return 'q3'
    elif state == 'q2':
        if __isDigit(symbol):
            return 'q4'
    elif state == 'q3':
        if __isDigit(symbol):
            return 'q4'
    elif state == 'q4':
        if __isDigit(symbol):
            return 'q4'


def __transitionFAExp(state: str, symbol: str):
    prefixUnaryOp = ['++', '--', '!', '~', '-', '+']
    postfixUnaryOp = ['++', '--']
    binaryOp = ['+', '-', '*', '/', '%', '>>', '<<', '>>>']
    assignmentOp = ['='] + [op + '=' for op in binaryOp]

    if state == 'q0':
        if isVariable(symbol):
            return 'q2'
        elif isNumber(symbol):
            return 'q3'
        elif symbol in prefixUnaryOp:
            return 'q1'
    elif state == 'q1':
        if isNumber(symbol):
            return 'q3'
        elif isVariable(symbol):
            return 'q2'
    elif state == 'q2':
        if symbol in postfixUnaryOp:
            return 'q4'
        elif symbol == '?':
            return 'q5'
        elif symbol in assignmentOp:
            return 'q0'
    elif state == 'q3':
        if symbol in postfixUnaryOp:
            return 'q4'
        elif symbol in binaryOp:
            return 'q0'
        elif symbol == '?':
            return 'q5'
    elif state == 'q4':
        if symbol in binaryOp:
            return 'q0'
    elif state == 'q5':
        if isVariable(symbol):
            return 'q7'
        elif isNumber(symbol):
            return 'q8'
        elif symbol in prefixUnaryOp:
            return 'q6'
    elif state == 'q6':
        if isNumber(symbol):
            return 'q8'
        elif isVariable(symbol):
            return 'q7'
    elif state == 'q7':
        if symbol in postfixUnaryOp:
            return 'q9'
        elif symbol == ':':
            return 'q0'
        elif symbol in assignmentOp:
            return 'q5'
    elif state == 'q8':
        if symbol in postfixUnaryOp:
            return 'q9'
        elif symbol == ':':
            return 'q0'
    elif state == 'q9':
        if symbol == ':':
            return 'q0'


def isVariable(inputs: str):
    startState = 'q0'
    finalStates = ['qf']
    faVariable = __FA("VARIABLE", startState,
                      finalStates, __transitionFAVariable)
    return faVariable.evaluate(inputs)


def isNumber(inputs: str):
    startState = 'q0'
    finalStates = ['q1', 'q4']
    faNumber = __FA("NUMBER", startState, finalStates, __transitionFANumber)
    return faNumber.evaluate(inputs)


def isExpression(inputs: str):
    startState = 'q0'
    finalStates = ['q2', 'q3', 'q4']
    faExpression = __FA("EXPRESSION", startState,
                        finalStates, __transitionFAExp)
    return faExpression.evaluate(inputs)


print(isExpression(
    ['29083', '?', '!', '129083', ':', '213232', '=', '29389287']))
