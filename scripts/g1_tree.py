import nltk
import sys
from nltk import CFG

def read_sentence():
    if len(sys.argv) != 2:
        print('Usage: python scripts/g1_tree.py "SELECT ... ;"')
        raise SystemExit(1)
    return sys.argv[1].strip()

# Grammar G1: ambiguity removed through operator precedence
# This grammar still contains left recursion, but expressions are no longer ambiguous.

grammar = CFG.fromstring("""
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

parser = nltk.ChartParser(grammar)

sentence = read_sentence()
tokens = sentence.split()

trees = list(parser.parse(tokens))

print("Tested string:")
print(sentence)
print()
print("Number of parse trees:", len(trees))

for i, tree in enumerate(trees, start=1):
    print(f"\nParse tree {i}:")
    print(tree)
    tree.pretty_print()
