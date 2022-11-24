str = "a<<<ba??b"
list_operator = ['!', '~', '-', '+', '++', '--', '-', '*', '**', '/', '%', '>>', '<<', '>>>', '==', '===', '!=', '!==', '>', '<', '<=', '>=', '&&', '||', '??', '?', ':', '&', '|', '~', '^', '=', '+=', '-=', '*=', '**=', '/=', '%=', '>>=', '<<=', '>>>=']
temp = [x for x in str]
curr_word = ''
res = []
for i in range(len(temp)):
    if i == 0:
        curr_word += temp[i]
    elif (temp[i] in list_operator and temp[i - 1] not in list_operator) or (temp[i] not in list_operator and temp[i - 1] in list_operator):
        res.append(curr_word)
        curr_word = temp[i]
    else:
        curr_word += temp[i]
res.append(curr_word)
print(res)