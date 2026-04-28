import nltk
import sys
from nltk import CFG
from nltk.parse import ChartParser

def read_sentence():
    if len(sys.argv) != 2:
        print('Usage: python scripts/g0_tree.py "SELECT ... ;"')
        raise SystemExit(1)
    return sys.argv[1].strip()

# Ambiguous base grammar G0
grammar = CFG.fromstring("""
    Query -> 'SELECT' SelectList 'FROM' TableList WhereClause ';'

    WhereClause -> 'WHERE' Expr

    SelectList -> SelectList ',' Column
    SelectList -> Column

    TableList -> TableList ',' Table
    TableList -> Table

    Column -> 'id' '.' 'id'
    Table -> 'id'

    Expr -> Expr 'OR' Expr
    Expr -> Expr 'AND' Expr
    Expr -> Expr '=' Expr
    Expr -> Expr '<' Expr
    Expr -> Expr '+' Expr
    Expr -> Expr '*' Expr
    Expr -> '(' Expr ')'
    Expr -> Column
    Expr -> 'num'
    Expr -> 'str'
""")

parser = ChartParser(grammar)

sentence = read_sentence()
tokens = sentence.split()

trees = list(parser.parse(tokens))

print("Tested string:")
print(sentence)
print()
print("Number of parse trees:", len(trees))

for i, tree in enumerate(trees, start=1):
    print(f"\\nParse tree {i}:")
    print(tree)
    tree.pretty_print()
