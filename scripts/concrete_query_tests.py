"""Small tests with real-looking SQL queries.

The grammar does not read names like clients or total. It reads id, num, and
str. This file shows the small step that changes real-looking queries into that
grammar format.
"""

import sys

import nltk

from g_final_tests import GRAMMAR, parse_count


# This is only an example schema. The grammar does not depend on it.
SCHEMA = {
    "clients": {"id", "name", "age", "city"},
    "orders": {"id", "client_id", "total"},
}


# Each test has: query, expected grammar result, expected schema result.
TESTS = [
    (
        "SELECT clients.name, orders.total FROM clients, orders "
        "WHERE clients.id = orders.client_id AND orders.total < 1000;",
        True,
        True,
    ),
    ("SELECT clients.name FROM clients WHERE clients.age < 30;", True, True),
    ("SELECT clients.name FROM clients WHERE clients.city = 'Monterrey';", True, True),
    ("SELECT clients.email FROM clients;", True, False),
    ("SELECT clients FROM clients;", False, False),
]


KEYWORDS = {"SELECT", "FROM", "WHERE", "OR", "AND"}
PUNCTUATION = [".", ",", ";", "(", ")", "=", "<", "+", "*"]


def split_query(query):
    """Add spaces around punctuation and split the query."""
    spaced_query = query

    for symbol in PUNCTUATION:
        spaced_query = spaced_query.replace(symbol, f" {symbol} ")

    return spaced_query.split()


def is_name(token):
    """Check if a token can be a table or column name."""
    return token.replace("_", "").isalnum() and not token.isdigit()


def to_token_query(query):
    """Change a real-looking query into the form used by the grammar."""
    token_query = []

    for token in split_query(query):
        upper_token = token.upper()

        if upper_token in KEYWORDS:
            token_query.append(upper_token)
        elif token.isdigit():
            token_query.append("num")
        elif token.startswith("'") and token.endswith("'"):
            token_query.append("str")
        elif is_name(token):
            token_query.append("id")
        else:
            token_query.append(token)

    return " ".join(token_query)


def check_schema(query):
    """Check if the real table and column names exist in SCHEMA."""
    tokens = split_query(query)
    tables = set()
    reading_from = False

    # First read the table names from the FROM part.
    for token in tokens:
        upper_token = token.upper()

        if upper_token == "FROM":
            reading_from = True
            continue

        if upper_token in {"WHERE", ";"}:
            reading_from = False

        if reading_from and token != ",":
            tables.add(token)

    if not tables:
        return False

    for table in tables:
        if table not in SCHEMA:
            return False

    # Then check every table.column pair.
    for position in range(len(tokens) - 2):
        table_name = tokens[position]
        middle_symbol = tokens[position + 1]
        column_name = tokens[position + 2]

        if is_name(table_name) and middle_symbol == "." and is_name(column_name):
            if table_name not in tables:
                return False
            if column_name not in SCHEMA[table_name]:
                return False

    return True


def print_result(query, token_query, tree_count, grammar_ok, schema_ok):
    """Print the result for one query."""
    print(f"Concrete input: {query}")
    print(f"Tokenized input: {token_query}")
    print(f"Syntax: {'ACCEPT' if grammar_ok else 'REJECT'}")
    print(f"Schema dictionary: {'ACCEPT' if schema_ok else 'REJECT'}")
    print(f"Parse trees: {tree_count}")

def main():
    parser = nltk.ChartParser(GRAMMAR)

    print("Schema dictionary:")
    for table, columns in SCHEMA.items():
        print(f"  {table}: {', '.join(sorted(columns))}")
    print()

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:]).strip()
        token_query = to_token_query(query)
        tree_count = parse_count(parser, token_query)
        grammar_ok = tree_count > 0
        schema_ok = check_schema(query) if grammar_ok else False

        print_result(query, token_query, tree_count, grammar_ok, schema_ok)
        sys.exit(0)

    all_passed = True

    for query, expected_grammar, expected_schema in TESTS:
        token_query = to_token_query(query)
        tree_count = parse_count(parser, token_query)
        grammar_ok = tree_count > 0
        schema_ok = check_schema(query) if grammar_ok else False
        passed = grammar_ok == expected_grammar and schema_ok == expected_schema
        all_passed = all_passed and passed

        print_result(query, token_query, tree_count, grammar_ok, schema_ok)
        print(f"Result: {'PASS' if passed else 'FAIL'}")
        print("-" * 60)

    if not all_passed:
        print("At least one concrete query test failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()