import sys

import nltk
from nltk import CFG


# G0 is the first grammar. It shows the two problems:
# ambiguity and left recursion.
GRAMMAR = CFG.fromstring("""
    Query -> 'SELECT' SelectList 'FROM' TableList WhereClause ';'

    WhereClause -> 'WHERE' Expr
    WhereClause ->

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


if len(sys.argv) != 2:
    print('Usage: python scripts/g0_tree.py "SELECT ... ;"')
    sys.exit(1)

sentence = sys.argv[1].strip()
parser = nltk.ChartParser(GRAMMAR)
trees = list(parser.parse(sentence.split()))

print("Tested string:")
print(sentence)
print()
print("Number of parse trees:", len(trees))

for tree_number, tree in enumerate(trees, start=1):
    print(f"\nParse tree {tree_number}:")
    print(tree)
    tree.pretty_print()
