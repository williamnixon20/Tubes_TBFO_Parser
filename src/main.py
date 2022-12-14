from grammar.cnf import getGrammar
from cyk import cyk

# from tokenizer import generate_token
from tokenizer import generate_token
from fa import fa

import argparse


def check(filename):
    grammar = getGrammar("grammar/cfg.txt")
    tokens, varnames, expressions = generate_token(filename)
    print("======================HASIL=========================")
    print(filename)
    tokens = [x.lower() for x in tokens]
    cyk_res = cyk(tokens, grammar)
    fa_res, fa_res2 = fa(varnames, expressions)
    if cyk_res and fa_res and fa_res2:
        print("ACCEPTED")
    else:
        print("REJECTED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = parser.parse_args()
    check(args.file.name)
