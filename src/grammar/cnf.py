global_dict = {}

def checkUnitProductions(grammar):
    global global_dict
    temp = []
    for rule in grammar:
        if len(rule) == 2 and not rule[1][0].islower():
            temp.append(rule)
            global_dict[rule[0]].append(rule[1:])
    return temp


def makeTwoVariables(grammar, unitProductions):
    temp = []
    idx = 0
    for rule in grammar:
        if rule in unitProductions:
            continue
        while len(rule) > 3:
            temp.append([f"{rule[0]}{idx}", rule[1], rule[2]])
            rule = [rule[0]] + [f"{rule[0]}{idx}"] + rule[3:]
            idx += 1
        if rule:
            global_dict[rule[0]].append(rule[1:])
            temp.append(rule)
    return temp


def handleUnitProductions(unitProductions):
    temp = []
    idx = 0
    while idx < len(unitProductions):
        rule = unitProductions[idx]
        if (rule[1]) in global_dict:
            for item in global_dict[rule[1]]:
                new_rule = [rule[0]] + item
                if len(new_rule) > 2 or new_rule[1][0].islower():
                    temp.append(new_rule)
                else:
                    unitProductions.append(new_rule)
                global_dict[new_rule[0]].append(new_rule[1:])
        idx += 1
    return temp


def getGrammar(file):
    global global_dict
    
    new_file = open(file, "r")
    lines = new_file.readlines()
    grammar = [_.replace("->", "").split() for _ in lines]

    for rule in grammar:
        if len(rule) != 0 and rule[0] not in global_dict:
            global_dict[rule[0]] = []

    unitProductions = checkUnitProductions(grammar)
    newRules = makeTwoVariables(grammar, unitProductions)
    unitProductionRules = handleUnitProductions(unitProductions)

    res = []
    for rule in newRules:
        res.append(rule)
    for rule in unitProductionRules:
        res.append(rule)

    map = {}
    for rule in res:
        rule_var = str(rule[0])
        if rule_var not in map:
            map[rule_var] = []
        temp_arr = []
        for i in range(1, len(rule)):
            temp_arr.append(rule[i])
        map[rule_var].append(temp_arr)

    return map
