from grammar.cnf import getGrammar
from cyk import cyk
from tokenizer import generate_token

import argparse


def check():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = parser.parse_args()

    grammar = getGrammar("grammar/cfg.txt")
    tokens, varnames, expressions = generate_token(args.file.name)
    print(tokens)
    print("======================VERDICT=========================")

    tokens = [x.lower() for x in tokens]
    print(tokens)
    cyk(tokens, grammar)


if __name__ == "__main__":
    check()
