import re
import os

token_list = [
    # Brackets
    (r"\(", " LP "),
    (r"\)", " RP "),
    (r"\{", " CL "),
    (r"\}", " CB "),
    (r"\[", " LSB "),
    (r"\]", " RSB "),
    # Operators
    (r"(?<![-+!~*/%<>&|=])\=(?![-+!~*/%<>&|=])", " EQ "),
    (r"\,", " COMMA "),
    (r"\:", " COLON "),
    # Reserved
    (r"\bbreak\b", " BREAK "),
    (r"\bdefault\b", " DEFAULT "),
    (r"\bfor\b", " FOR "),
    (r"\breturn\b", " RETURN "),
    (r"\bvar\b", " VAR "),
    (r"\bconst\b", " CONST "),
    (r"\bdelete\b", " DELETE "),
    (r"\bfunction\b", " FUNCTION "),
    (r"\bswitch\b", " SWITCH "),
    (r"\bwhile\b", " WHILE "),
    (r"\bcase\b", " CASE "),
    (r"\belse\b", " ELSE "),
    (r"\bif\b", " IF "),
    (r"\bthrow\b", " THROW "),
    (r"\bcatch\b", " CATCH "),
    (r"\bfalse\b", " FALSE "),
    (r"\blet\b", " LET "),
    (r"\btry\b", " TRY "),
    (r"\bcontinue\b", " CONTINUE "),
    (r"\bfinally\b", " FINALLY "),
    (r"\bnull\b", " NULL "),
    (r"\btrue\b", " TRUE "),
    (r"\'.+?\'", " STRING "),
    (r"\".+?\"", " STRING "),
    (r"\n", ""),
    (r"[ ]*\/\/.+", ""),
    # (r"\/\/.+", ""),
    (r"\;(?!.+)", " "),
    (r"\;", " SEMI_COL "),
]

list_token_capitalized = [
    (r"\bBREAK\b", " Break "),
    (r"\bDEFAULT\b", " Default "),
    (r"\bFOR\b", " For "),
    (r"\bRETURN\b", " Return "),
    (r"\bVAR\b", " Var "),
    (r"\bCONST\b", " Const "),
    (r"\bDELETE\b", " Delete "),
    (r"\bFUNCTION\b", " Function "),
    (r"\bSWITCH\b", " Switch "),
    (r"\bWHILE\b", " While "),
    (r"\bCASE\b", " Case "),
    (r"\bELSE\b", " Else "),
    (r"\bIF\b", " If "),
    (r"\bTHROW\b", " Throw "),
    (r"\bCATCH\b", " Catch "),
    (r"\bFALSE\b", " False "),
    (r"\bLET\b", " Let "),
    (r"\bTRY\b", " Try "),
    (r"\bCONTINUE\b", " Continue "),
    (r"\bFINALLY\b", " Finally "),
    (r"\bNULL\b", " Null "),
    (r"\bTRUE\b", " True "),
    (r"\bSTRING\b", " String "),
]

list_operator = [
    "!",
    "~",
    "-",
    "+",
    "++",
    "--",
    "+",
    "-",
    "*",
    "**",
    "/",
    "%",
    ">>",
    "<<",
    ">>>",
    "==",
    "===",
    "!=",
    "!==",
    ">",
    "<",
    "<=",
    ">=",
    "&&",
    "||",
    "??",
    "?",
    ":",
    "&",
    "|",
    "~",
    "^",
    "=",
    "+=",
    "-=",
    "*=",
    "**=",
    "/=",
    "%=",
    ">>=",
    "<<=",
    ">>>=",
]

def destruct_expr(strlist):
    # print(strlist)
    res = []
    for j in range(len(strlist)):
        curr_word = ''
        temp = strlist[j]
        for i in range(len(strlist[j])):
            if i == 0:
                curr_word += temp[i]
            elif (temp[i] in list_operator and temp[i - 1] not in list_operator) or (temp[i] not in list_operator and temp[i - 1] in list_operator):
                if curr_word != '':
                    res.append(curr_word)
                curr_word = temp[i]
            else:
                curr_word += temp[i]
        if curr_word != '':
            res.append(curr_word)
    return res


def generate_token(file_name):
    file = open(file_name)
    characters = file.readlines()
    file.close()
    list_token_fix = []
    list_varname_fix = []
    list_exp_fix = []
    for character in characters:
        print(character)
        # if len(character) == 0 or len(character) == 1:
        #     continue
        list_token = []
        list_varname = []
        list_exp = []
        result = character.strip()
        for token in list_token_capitalized:
            pattern, tag = token
            result = re.sub(pattern, tag, result)
        for token in token_list:
            pattern, tag = token
            if tag.strip() == "EQ":
                result = re.sub(pattern, tag, result, 1)
            else:
                result = re.sub(pattern, tag, result)
        tempResult = result.split(" ")
        tempResult = [x for x in tempResult if x and x != "\n"]
        print("TEMPRES", tempResult)
        # if len(character) > 1 and tempResult[0] == "//":
        #     continue
        flag_varname = True
        flag_expression = False
        flag_quest = False
        curr_word = ""
        amt = 0
        # print(tempResult)
        for i in range(len(tempResult)):
            flag = False
            if tempResult[i] == "//":
                break
            for token in token_list:
                pattern, tag = token
                if tag.strip() == tempResult[i]:
                    flag = True
                    break
            if flag_varname and (not flag or tempResult[i] == 'FALSE' or tempResult[i] == 'TRUE' or tempResult[i] == 'STRING' or tempResult[i] == 'NULL'):
                curr_word += tempResult[i] + " "
                if (
                    i == len(tempResult) - 1
                    or tempResult[i + 1] == "COMMA"
                    or tempResult[i + 1] == "RSB"
                ):
                    list_token = list_token[: len(list_token) - amt]
                    list_varname = list_varname[: len(list_varname) - amt]
                    if i == 0 or (i != 0 and (tempResult[i - 1] != 'VAR' and tempResult[i - 1] != 'CONST' and tempResult[i - 1] != 'LET')) :
                        list_token.append("EXPR")
                        print("curr", curr_word)
                        list_exp.append(destruct_expr(
                        curr_word.split(" ")))
                    else:
                        list_varname.append(tempResult[i])
                        list_token.append("VAR_NAME")
                    curr_word = ""
                    amt = 0
                elif tempResult[i] == '?':
                    flag_expression = True
                    flag_varname = False
                    flag_quest = True
                    print("((((((((((LIST TOKEN", list_token)
                    list_token = list_token[:len(list_token) - amt]
                    list_varname = list_varname[:len(list_varname) - amt]
                    # # temp_list_varname = list_varname[len(list_varname) - amt:]
                    # if curr_word != "":
                    #     print("__________YY", curr_word.split())
                    #     list_exp = list_exp[:len(list_exp) - amt]
                    #     list_exp.append(destruct_expr(curr_word.split(" ")))
                else:
                    amt += 1
                    print("________FDFD", curr_word.split())
                    list_varname.append(tempResult[i])
                    tempResult[i] = "VAR_NAME"
                    list_token.append(tempResult[i])
            elif (
                tempResult[i] == "EQ"
                or tempResult[i] == "LP"
                # or tempResult[i] == "COLON"
                or tempResult[i] == "CASE"
            ):
                list_token = list_token[: len(list_token) - amt + 1]
                print("cw1", curr_word.split())
                if curr_word != "":
                    list_varname = list_varname[: len(list_varname) - amt]
                    if (flag_expression):
                        print("YEAAAAAAAAAAAAAAA")
                        list_token.append("VAR_NAME")
                    list_varname.append(curr_word.rstrip())
                list_token.append(tempResult[i])
                curr_word = ""
                flag_expression = True
                flag_varname = False
            elif flag_expression and not flag:
                curr_word += tempResult[i] + " "
                amt+=1
                print("YEs", curr_word)
                if i == len(tempResult) - 1 or tempResult[i + 1] == 'RSB':
                    if flag_quest:
                        list_token = list_token[:len(list_token) - amt - 1]
                        list_exp = list_exp[:len(list_exp) - amt - 1]
                    list_exp.append(destruct_expr(curr_word.split(" ")))
                    list_token.append("EXPR")
                elif tempResult[i] == '?' :
                    flag_quest = True
                    print("((((((((((LIST TOKEN", list_token)
                    # list_token = list_token[:len(list_token) - amt]
                    list_varname = list_varname[:len(list_varname) - amt]
                    # # temp_list_varname = list_varname[len(list_varname) - amt:]
                    # if curr_word != "":
                    #     print("__________YY", curr_word.split())
                    #     list_exp = list_exp[:len(list_exp) - amt]
                    #     list_exp.append(destruct_expr(curr_word.split(" ")))
            elif flag_expression and (tempResult[i] == "RP" or tempResult[i] == 'COMMA' or tempResult[i] == 'SEMI_COL'):
                print("CWWW", curr_word.split())
                if curr_word != "":
                    list_exp.append(destruct_expr(curr_word.split(" ")))
                    list_token.append("EXPR")
                    if tempResult[i] != ';':
                        list_token.append(tempResult[i])
                else:
                    list_token.append(tempResult[i]);
                curr_word = ""
                print("YESSS")
                if flag_quest:
                    print("YESSS")
                    list_token = list_token[:len(list_token) - amt]
                    list_exp = list_exp[:len(list_exp) - amt - 1]
                if  tempResult[i] == 'RP':
                    flag_expression = False
                    flag_varname = True
            else:
                if not flag_expression:
                    print("==============", tempResult[i])
                    if flag and i == len(tempResult) - 1 and tempResult[i] != 'CL' and tempResult[i] != 'CB' and tempResult[i] != 'RP' and tempResult[i] != 'RSB' and tempResult[i] != 'LP' and tempResult[i] != 'LSB' and tempResult[i] != 'BREAK' and tempResult[i] != 'CONTINUE' and tempResult[i] != 'RETURN' and tempResult[i] != 'COLON':
                        list_token = list_token[:len(list_token) - amt]
                        list_varname = list_varname[:len(list_varname) - amt]
                        curr_word = curr_word.rstrip() +  tempResult[i]
                        list_token.append("VAR_NAME")
                        list_varname.append(curr_word.rstrip())
                    elif tempResult[i] == 'STRING':
                        amt+=1
                        curr_word += curr_word.rstrip() + tempResult[i]
                        list_token.append(tempResult[i])
                    if tempResult[i] != 'STRING':
                        curr_word = ""
                        list_token.append(tempResult[i])
                else:
                    curr_word += tempResult[i] + " "
                    temp_curr_word = curr_word.split()
                    if temp_curr_word[0] == "LET" or temp_curr_word[0] == "VAR" or temp_curr_word[0] == "CONST":
                        list_token.append(temp_curr_word[0])
                        curr_word =  ""
                    print("BEL", curr_word.split())
                    if i == len(tempResult) - 1 and tempResult[i] != "COLON":
                        list_token.append("EXPR")
                        list_exp.append(destruct_expr(curr_word.split()))
                    elif tempResult[i] == "COLON"and not flag_quest:
                        temp_expr = curr_word.split()
                        list_exp.append(destruct_expr(temp_expr[:-1]))
                        list_token.append("EXPR")
                        list_token.append(tempResult[i])
                # tempResult.pop(i)
            print(list_token)
        print(list_token)
        list_token_fix.extend(list_token)
        list_exp_fix.extend(list_exp)
        list_varname_fix.extend(list_varname)
    path = os.getcwd()
    # print(path)
    file_write_token = open(path + "/out/tokenResult.txt", "w")
    for token in list_token_fix:
        file_write_token.write(str(token) + " ")
    file_write_token.close()
    file_write_varname = open(path + "/out/varnameResult.txt", "w")
    for varname in list_varname_fix:
        file_write_varname.write(str(varname) + " ")
    file_write_varname.close()
    file_write_exp = open(path + "/out/expResult.txt", "w")
    for exp in list_exp_fix:
        file_write_exp.write(str(exp) + " ")
    file_write_exp.close()
    print(list_token_fix, list_varname_fix, list_exp_fix)
    return list_token_fix, list_varname_fix, list_exp_fix

generate_token('../test/test.js')
