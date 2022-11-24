from fa import fa


def __transitionFAVariable(state, symbol):
    if state == 'q0':
        if ('a' <= symbol <= 'z') or ('A' <= symbol <= 'Z') or (symbol == '$') or (symbol == '_'):
            return 'qf'
        else:
            return 'qd'
    elif state == 'qf':
        if ('a' <= symbol <= 'z') or ('A' <= symbol <= 'Z') or (symbol == '$') or (symbol == '_') or ('0' <= symbol <= '9'):
            return 'qf'
        else:
            return 'qd'


def faVariable(inputs):
    startState = 'q0'
    finalState = ['qf']
    return fa(startState, finalState, __transitionFAVariable, inputs)
