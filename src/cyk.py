from grammar.cnf import getGrammar
import copy

tokens = ""
grammar = ""
matrix_dp = []


def process_terminals(token_index):
    global matrix_dp
    for token_left, productions in grammar.items():
        for production in productions:
            ## Bukan Terminal
            if len(production) != 1:
                continue
            ## Terminal, tapi tidak sama dengan token
            if production[0] != tokens[token_index]:
                continue
            ## Add to matrix
            matrix_dp[token_index][token_index].add(token_left)


def process_previous(prev_token_idx, length_dp, token_idx):
    global matrix_dp
    for token_left, productions in grammar.items():
        for production in productions:
            ## Skip terminal
            if len(production) == 1:
                continue
            ## Tidak bisa menyambung state sekarang
            if production[0] not in matrix_dp[prev_token_idx][length_dp]:
                continue
            if production[1] not in matrix_dp[length_dp + 1][token_idx]:
                continue
            ## Add to matrix
            matrix_dp[prev_token_idx][token_idx].add(token_left)


def cyk(tokens_arg, grammar_arg):
    global tokens, grammar, matrix_dp

    tokens = tokens_arg
    grammar = grammar_arg
    token_length = len(tokens)

    matrix_row = []
    matrix_dp = []
    for temp in range(token_length):
        matrix_row.append(set([]))

    for temp in range(token_length):
        matrix_dp.append(copy.deepcopy(matrix_row))

    for token_idx in range(0, token_length):
        process_terminals(token_idx)
        for prev_token_idx in range(token_idx, -1, -1):
            for length_dp in range(prev_token_idx, token_idx):
                process_previous(prev_token_idx, length_dp, token_idx)
        print("Progress: {}/{}".format(token_idx, token_length))
    if "VALID" in matrix_dp[0][token_length - 1]:
        print("CYK berhasil menvalidasi string.")
        return True
    else:
        print("CYK gagal menvalidasi program.")
        return False


if __name__ == "__main__":
    grammar = getGrammar("cfg.txt")
    print("======================VERDICT=========================")
    token = [
        "IF",
        "LP",
        "FALSE",
        "RP",
        "CL",
        "IF",
        "LP",
        "EXPR",
        "RP",
        "CL",
        "EXPR",
        "EXPR",
        "FOR",
        "LP",
        "VAR_NAME",
        "EQ",
        "EXPR",
        "SEMI_COL",
        "EXPR",
        "SEMI_COL",
        "EXPR",
        "RP",
        "CL",
        "CONTINUE",
        "CB",
        "EXPR",
        "CB",
        "EXPR",
        "CB",
        "EXPR",
    ]
    # token = [
    #     "FUNCTION",
    #     "VAR_NAME",
    #     "LP",
    #     "EXPR",
    #     "COMMA",
    #     "EXPR",
    #     "RP",
    #     "CL",
    #     "RETURN",
    #     "FOR",
    #     "LP",
    #     "VAR_NAME",
    #     "EQ",
    #     "EXPR",
    #     "SEMI_COL",
    #     "EXPR",
    #     "SEMI_COL",
    #     "EXPR",
    #     "RP",
    #     "CL",
    #     "BREAK",
    #     "CB",
    #     "CB",
    # ]
    tokens = [x.lower() for x in token]
    cyk(tokens, grammar)
