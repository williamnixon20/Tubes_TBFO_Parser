str = "a<<<ba??b ab"
strlist = str.split(" ")
print(strlist)
list_operator = ['!', '~', '-', '+', '++', '--', '-', '*', '**', '/', '%', '>>', '<<', '>>>', '==', '===', '!=', '!==', '>', '<', '<=', '>=', '&&', '||', '??', '?', ':', '&', '|', '~', '^', '=', '+=', '-=', '*=', '**=', '/=', '%=', '>>=', '<<=', '>>>=']
res = []
for j in range(len(strlist)):
    curr_word = ''
    temp = strlist[j]
    for i in range(len(strlist[j])):
        if i == 0:
            curr_word += temp[i]
        elif (temp[i] in list_operator and temp[i - 1] not in list_operator) or (temp[i] not in list_operator and temp[i - 1] in list_operator):
            res.append(curr_word)
            curr_word = temp[i]
        else:
            curr_word += temp[i]
    res.append(curr_word)
print(res)