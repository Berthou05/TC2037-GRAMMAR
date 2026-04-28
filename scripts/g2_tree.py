import nltk
import sys
from nltk import CFG

def read_sentence():
    if len(sys.argv) != 2:
        print('Usage: python scripts/g2_tree.py "SELECT ... ;"')
        raise SystemExit(1)
    return sys.argv[1].strip()

grammar = CFG.fromstring("""
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

parser = nltk.ChartParser(grammar)

sentence = read_sentence()
tokens = sentence.split()

print("Tested string:")
print(sentence)
print()
trees = list(parser.parse(tokens))
print("Number of parse trees:", len(trees))

for i, tree in enumerate(trees, start=1):
    print(f"\nParse tree {i}:")
    print(tree)
    tree.pretty_print()
