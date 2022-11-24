import re

token_list = [
    # Brackets
    (r'\(', 'LB'),
    (r'\)', 'RB'),
    (r'\{', 'LCB'),
    (r'\}', 'RCB'),
    (r'\[', 'LSB'),
    (r'\]', 'RSB'),

    # Reserved
    (r'\bbreak\b', 'BREAK'),
    (r'\bdefault\b', 'DEFAULT'),
    (r'\bfor\b', 'FOR'),
    (r'\breturn\b', 'RETURN'),
    (r'\bvar\b', 'VAR'),
    (r'\bconst\b', 'CONST'),
    (r'\bdelete\b', 'DELETE'),
    (r'\bfunction\b', 'FUNCTION'),
    (r'\bswitch\b', 'SWITCH'),
    (r'\bwhile\b', 'WHILE'),
    (r'\bcase\b', 'CASE'),
    (r'\belse\b', 'ELSE'),
    (r'\bif\b', 'IF'),
    (r'\bthrow\b', 'THROW'),
    (r'\bcatch\b', 'CATCH'),
    (r'\bfalse\b', 'FALSE'),
    (r'\blet\b', 'LET'),
    (r'\btry\b', 'TRY'),
    (r'\bcontinue\b', 'CONTINUE'),
    (r'\bfinally\b', 'FINALLY'),
    (r'\bnull\b', 'NULL'),
    (r'\btrue\b', 'TRUE')
]

def generate_token():
    file = open('test.txt')
    characters = file.read()
    file.close()

    flag__varname = True
    flag__expression = False 
    tag = ''

    current_word = ''
    for char in characters:
        if char != ' ' and char != '\n':
            if char == '=':
                if flag__varname :
                    print('VAR_NAME', end=' ')
                flag__expression = True
                flag__varname = False
                current_word = ''
                print('EQ', end=' ')
                continue
            if char == ';' and current_word != '':
                print('EXPR', end=' ')
                flag__expression = False
                flag__varname = True
                current_word = ''
                continue

            current_word += char
        else:
            flag__pattern = False
            for token in token_list:
                pattern, tag = token
                regexp = re.compile(pattern)
                flag__pattern = regexp.match(current_word)
                if flag__pattern:
                    break
            if flag__pattern:
                print(tag, end=' ')
                continue
            if flag__varname:
                continue
        
generate_token()