import sys

import nltk
from nltk import CFG


# G2 is the final grammar.
# It keeps the same idea as G1, but removes left recursion.
GRAMMAR = CFG.fromstring("""
    Query -> 'SELECT' SelectList 'FROM' TableList WhereClause ';'

    WhereClause -> 'WHERE' Expr
    WhereClause ->

    SelectList -> Column SelectListTail
    SelectListTail -> ',' Column SelectListTail
    SelectListTail ->

    TableList -> Table TableListTail
    TableListTail -> ',' Table TableListTail
    TableListTail ->

    Column -> 'id' '.' 'id'
    Table -> 'id'

    Expr -> AndExpr ExprTail
    ExprTail -> 'OR' AndExpr ExprTail
    ExprTail ->

    AndExpr -> RelExpr AndExprTail
    AndExprTail -> 'AND' RelExpr AndExprTail
    AndExprTail ->

    RelExpr -> AddExpr RelExprTail
    RelExprTail -> '=' AddExpr RelExprTail
    RelExprTail -> '<' AddExpr RelExprTail
    RelExprTail ->

    AddExpr -> MulExpr AddExprTail
    AddExprTail -> '+' MulExpr AddExprTail
    AddExprTail ->

    MulExpr -> Primary MulExprTail
    MulExprTail -> '*' Primary MulExprTail
    MulExprTail ->

    Primary -> '(' Expr ')'
    Primary -> Column
    Primary -> 'num'
    Primary -> 'str'
""")


if len(sys.argv) != 2:
    print('Usage: python scripts/g2_tree.py "SELECT ... ;"')
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
