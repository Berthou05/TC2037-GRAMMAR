import sys

import nltk
from nltk import CFG


# G1 fixes ambiguity by separating operator levels.
# It still has left recursion, so it is not the final grammar.
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

    Expr -> Expr 'OR' AndExpr
    Expr -> AndExpr

    AndExpr -> AndExpr 'AND' RelExpr
    AndExpr -> RelExpr

    RelExpr -> RelExpr '=' AddExpr
    RelExpr -> RelExpr '<' AddExpr
    RelExpr -> AddExpr

    AddExpr -> AddExpr '+' MulExpr
    AddExpr -> MulExpr

    MulExpr -> MulExpr '*' Primary
    MulExpr -> Primary

    Primary -> '(' Expr ')'
    Primary -> Column
    Primary -> 'num'
    Primary -> 'str'
""")


if len(sys.argv) != 2:
    print('Usage: python scripts/g1_tree.py "SELECT ... ;"')
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
