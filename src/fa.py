import re

class __FA:
    def __init__(self, name: str, startState: str, finalState: str, transition):
        self.name = name
        self.startState = startState
        self.finalState = finalState
        self.transition = transition

    def evaluate(self, inputs: str):
        currentState = self.startState
        for symbol in inputs:
            # print(self.name, currentState, symbol)
            currentState = self.transition(currentState, symbol)
            if not currentState:
                break
        return currentState in self.finalState

    def evalAll(self, arrInputs):
        for inputs in arrInputs:
            if not self.evaluate(inputs):
                return False
        return True


def __isAlpha(symbol: str):
    return ('a' <= symbol <= 'z') or ('A' <= symbol <= 'Z')


def __isDigit(symbol: str):
    return ('0' <= symbol <= '9')

def __isString(symbol: str):
    return re.search("\'.+\'", symbol) or re.search("\".+\"", symbol)

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
    prefixUnaryOp = ['!', '~', '-', '+']
    incrementDecrement = ['++', '--']
    binaryOp = ['+', '-', '*', '**', '/', '%', '>>', '<<',
                '>>>', '==', '===', '!=', '!==', '>', '<', '<=', '>=', '&&', '||', '??', '&', '|', '~', '^']
    assignmentOp = ['=', '+=', '-=', '*=',
                    '**=', '/=', '%=', '>>=', '<<=', '>>>=']
    print("EXPRESSION", "STATE", state, "SYMBOL", symbol)
    if state == 'q0':
        if isVariable(symbol):
            return 'q1'
        else:
            return __transitionFAExp('q3', symbol)
    elif state == 'q1':
        if symbol in assignmentOp:
            return 'q2'
        else:
            return __transitionFAExp('q8', symbol)
    elif state == 'q2':
        if isVariable(symbol):
            return 'q1'
        else:
            return __transitionFAExp('q3', symbol)
    elif state == 'q3':
        if symbol in incrementDecrement:
            return 'q7'
        elif symbol in prefixUnaryOp:
            return 'q5'
        elif isVariable(symbol):
            return 'q6'
        elif isNumber(symbol) or __isString(symbol):
            return 'q4'
    elif state == 'q4':
        return __transitionFAExp('q8', symbol)
    elif state == 'q5':
        if isVariable(symbol):
            return 'q6'
        elif isNumber(symbol) or __isString(symbol):
            return 'q4'
    elif state == 'q6':
        if symbol in incrementDecrement:
            return 'q10'
        else:
            return __transitionFAExp('q8', symbol)
    elif state == 'q7':
        if isVariable(symbol):
            return 'q6'
    elif state == 'q8':
        if symbol == '?':
            return 'q12'
        elif symbol == '??':
            return 'q11'
        elif symbol in binaryOp:
            return 'q9'
    elif state == 'q9':
        return __transitionFAExp('q3', symbol)
    elif state == 'q10':
        if symbol == '?':
            return 'q12'
        elif symbol in binaryOp:
            return 'q9'
    elif state == 'q11':
        return __transitionFAExp('q3', symbol)
    elif state == 'q12':
        if isVariable(symbol):
            return 'q18'
        else:
            return __transitionFAExp('q13', symbol)
    elif state == 'q13':
        if symbol in incrementDecrement:
            return 'q17'
        elif symbol in prefixUnaryOp:
            return 'q15'
        elif isVariable(symbol):
            return 'q16'
        elif isNumber(symbol) or __isString(symbol):
            return 'q14'
    elif state == 'q14':
        if symbol == ':':
            return 'q0'
        else:
            return __transitionFAExp('q21', symbol)
    elif state == 'q15':
        if isVariable(symbol):
            return 'q16'
        elif isNumber(symbol) or __isString(symbol):
            return 'q14'
    elif state == 'q16':
        if symbol == ':':
            return 'q0'
        elif symbol in incrementDecrement:
            return 'q22'
        else:
            return __transitionFAExp('q21', symbol)
    elif state == 'q17':
        if isVariable(symbol):
            return 'q16'
    elif state == 'q18':
        if symbol == ':':
            return 'q0'
        elif symbol in assignmentOp:
            return 'q19'
        else:
            return __transitionFAExp('q21', symbol)
    elif state == 'q19':
        if isVariable(symbol):
            return 'q18'
        else:
            return __transitionFAExp('q13', symbol)
    elif state == 'q20':
        return __transitionFAExp('q13', symbol)
    elif state == 'q21':
        if symbol == '??':
            return 'q23'
        elif symbol in binaryOp:
            return 'q20'
    elif state == 'q22':
        if symbol == ':':
            return 'q0'
        elif symbol in binaryOp:
            return 'q20'
    elif state == 'q23':
        return __transitionFAExp('q13', symbol)


__faVAR = __FA("VARIABLE", 'q0',
               ['qf'], __transitionFAVariable)
__faNUM = __FA("NUMBER", 'q0', ['q1', 'q4'], __transitionFANumber)
__faEXP = __FA("EXPRESSION", 'q0',
               ['q1', 'q4', 'q6'], __transitionFAExp)


def isVariable(inputs: str):
    verdict = __faVAR.evaluate(inputs)
    if (verdict):
        print("VARIABLE", inputs, "OK")
    else:
        print("VARIABLE", inputs, "NOT OK")

    return verdict


def isNumber(inputs: str):
    verdict = __faNUM.evaluate(inputs)
    if (verdict):
        print("NUMBER", inputs, "OK")
    else:
        print("NUMBER", inputs, "NOT OK")

    return verdict


def isExpression(inputs: str):
    return __faEXP.evaluate(inputs)


def evalAllVariable(arrInputs: str):
    return __faVAR.evalAll(arrInputs)


def evalAllNumber(arrInputs: str):
    return __faNUM.evalAll(arrInputs)


def evalAllExpression(arrInputs: str):
    return __faEXP.evalAll(arrInputs)


def fa(varnames, expressions):
    if (evalAllVariable(varnames)):
        print("VARIABLE OK")
    else:
        print("VARIABLE NOT OK")
    print("\n")
    if (evalAllExpression(expressions)):
        print("EXPRESSION OK")
    else:
        print("EXPRESSION NOT OK")