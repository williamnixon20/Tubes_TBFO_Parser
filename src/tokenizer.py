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
    (r"(?<!\=)\=(?!\=)", " EQ "),
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
    (r"\'.+\'", " STRING "),
    (r"\".+\"", " STRING "),
    (r"\n", ""),
    (r"\;", " "),
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


def destruct_expr(temp):
    curr_word = ""
    res = []
    for i in range(len(temp)):
        if i == 0:
            curr_word += temp[i]
        elif (temp[i] in list_operator and temp[i - 1] not in list_operator) or (
            temp[i] not in list_operator and temp[i - 1] in list_operator
        ):
            res.append(curr_word)
            curr_word = temp[i]
        else:
            curr_word += temp[i]
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
        if len(character) == 0 or len(character) == 1:
            continue
        list_token = []
        list_varname = []
        list_exp = []
        result = character
        for token in token_list:
            pattern, tag = token
            if tag.strip() == "EQ":
                result = re.sub(pattern, tag, result, 1)
            else:
                result = re.sub(pattern, tag, result)
        tempResult = result.split(" ")
        tempResult = [x for x in tempResult if x and x != "\n"]
        if tempResult[0] == "//":
            continue
        flag_varname = True
        flag_expression = False
        curr_word = ""
        amt = 0
        for i in range(len(tempResult)):
            flag = False
            if tempResult[i] == "//":
                break
            for token in token_list:
                pattern, tag = token
                if tag.strip() == tempResult[i]:
                    flag = True
                    break
            if flag_varname and not flag:
                curr_word += tempResult[i]
                if (
                    i == len(tempResult) - 1
                    or tempResult[i + 1] == "COMMA"
                    or tempResult[i + 1] == "RSB"
                ):
                    list_token = list_token[: len(list_token) - amt]
                    list_varname = list_varname[: len(list_varname) - amt]
                    list_exp.append(destruct_expr([x for x in curr_word]))
                    list_token.append("EXPR")
                    curr_word = ""
                    amt = 0
                else:
                    amt += 1
                    list_varname.append(tempResult[i])
                    tempResult[i] = "VAR_NAME"
                    list_token.append(tempResult[i])
            elif (
                tempResult[i] == "EQ"
                or tempResult[i] == "LP"
                or tempResult[i] == "COLON"
            ):
                flag_expression = True
                flag_varname = False
                list_varname = list_varname[: len(list_varname) - amt]
                list_token = list_token[: len(list_token) - amt + 1]
                if curr_word != "":
                    list_varname.append(curr_word)
                list_token.append(tempResult[i])
                curr_word = ""
            elif flag_expression and not flag:
                curr_word += tempResult[i]
                if i == len(tempResult) - 1:
                    list_exp.append(destruct_expr([x for x in curr_word]))
                    list_token.append("EXPR")
            elif flag_expression and tempResult[i] == "RP" and curr_word != "":
                list_exp.append(destruct_expr([x for x in curr_word]))
                list_token.append("EXPR")
                list_token.append(tempResult[i])
                curr_word = ""
            else:
                curr_word = ""
                list_token.append(tempResult[i])
                # tempResult.pop(i)
            # print(list_token)
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
    return list_token_fix, list_varname_fix, list_exp_fix
