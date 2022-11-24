from fa import fa
from faVariable import faVariable


def __transitionFANumber(state, symbol):
    if state == 'q0':
        if '0' <= symbol <= '9':
            return 'qf'
    elif state == 'qf':
        if '0' <= symbol <= '9':
            return 'qf'
        elif symbol == '.':
            return 'q0'


def faNumber(inputs):
    startState = 'q0'
    finalState = ['qf']
    return fa(startState, finalState, __transitionFANumber, inputs)


def __transitionFAExpression(state, symbol):
    unaryPrefixOperator = ['++', '--', '!', '~', '-', '+']
    unaryPostfixOperator = ['++', '--']
    # TODO: LIST OPERATOR
    operator = ['+', '-', '/', '>>']
    assignOperator = [op + '=' for op in operator]
    assignOperator.append('=')
    if state == 'q0':
        if symbol in unaryPrefixOperator:
            return 'q1'
        elif faVariable(symbol):
            return 'q3'
        elif faNumber(symbol):
            return 'q4'
    elif state == 'q1':
        if faNumber(symbol):
            return 'q2'
    elif state == 'q2':
        return 'qd'
    elif state == 'q3':
        if symbol in unaryPostfixOperator:
            return 'q5'
        elif symbol in operator:
            return 'q6'
        elif symbol in assignOperator:
            return 'q0'
    elif state == 'q4':
        if symbol in unaryPostfixOperator:
            return 'q5'
        elif symbol in operator:
            return 'q6'
    elif state == 'q5':
        if symbol in operator:
            return 'q6'
    elif state == 'q6':
        if faVariable(symbol):
            return 'q3'
        elif faNumber(symbol):
            return 'q4'


def faExpression(inputs):
    startState = 'q0'
    finalState = ['q2', 'q3', 'q4', 'q5']
    return fa(startState, finalState, __transitionFAExpression, inputs)


print(faExpression(['apa', '++', 'yey']))
