import nltk
import sys
from nltk import CFG


# Final grammar used in the report.
# This is G2: ambiguity and left recursion were already removed.
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


# Each test has a sentence and the result I expect from the grammar.
# True means the sentence should be accepted.
# False means the sentence should be rejected.
TESTS = [
    ("SELECT id . id FROM id ;", True),
    ("SELECT id . id , id . id FROM id ;", True),
    ("SELECT id . id FROM id , id ;", True),
    ("SELECT id . id FROM id WHERE id . id = num ;", True),
    ("SELECT id . id FROM id , id WHERE id . id = num OR id . id = num ;", True),
    ("SELECT id . id , id . id FROM id , id WHERE id . id = id . id AND id . id < num ;", True),
    ("SELECT id . id FROM id WHERE id . id + num * num < num ;", True),
    ("SELECT id . id FROM id WHERE ( id . id = num ) AND id . id = str ;", True),
    ("SELECT FROM id ;", False),
    ("SELECT id . id id ;", False),
    ("SELECT id . id FROM ;", False),
    ("SELECT id . id FROM id WHERE ;", False),
    ("SELECT id . id FROM id WHERE id . id = ;", False),
    ("SELECT id FROM id ;", False),
    ("SELECT id . id FROM id WHERE id = num ;", False),
]


def parse_count(parser, sentence):
    """Return how many parse trees the parser finds for one sentence."""
    tokens = sentence.split()
    try:
        return len(list(parser.parse(tokens)))
    except ValueError:
        # NLTK raises ValueError when the sentence has a token outside the grammar.
        return 0


def main():
    parser = nltk.ChartParser(GRAMMAR)

    # If the user writes a sentence in the terminal, test only that sentence.
    if len(sys.argv) > 1:
        sentence = " ".join(sys.argv[1:]).strip()
        tree_count = parse_count(parser, sentence)
        actual_accept = tree_count > 0

        print(f"Input: {sentence}")
        print(f"Actual: {'ACCEPT' if actual_accept else 'REJECT'}")
        print(f"Parse trees: {tree_count}")
        return

    all_passed = True

    # Otherwise, run the full test list.
    for sentence, expected_accept in TESTS:
        tree_count = parse_count(parser, sentence)
        actual_accept = tree_count > 0
        passed = actual_accept == expected_accept
        all_passed = all_passed and passed

        print(f"Input: {sentence}")
        print(f"Expected: {'ACCEPT' if expected_accept else 'REJECT'}")
        print(f"Actual: {'ACCEPT' if actual_accept else 'REJECT'}")
        print(f"Parse trees: {tree_count}")
        print(f"Result: {'PASS' if passed else 'FAIL'}")
        print("-" * 60)

    if not all_passed:
        # Stop with an error if any test failed.
        sys.exit(1)


if __name__ == "__main__":
    main()
