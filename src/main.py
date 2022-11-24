from grammar.cnf import getGrammar
from cyk import cyk
import argparse


def check():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("file", type=argparse.FileType("r"))
    # args = parser.parse_args()

    grammar = getGrammar("grammar/cfg.txt")
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


if __name__ == "__main__":
    check()
