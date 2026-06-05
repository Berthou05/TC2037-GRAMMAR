"""
Tests real SQL queries against two checks:
  1. Grammar  – does the query follow valid SQL structure?
  2. Schema   – do the table/column names exist in our database?

The grammar parser only understands generic tokens (id, num, str) instead of
real names, so we convert queries before parsing:
  "SELECT clients.name FROM clients WHERE clients.age < 30;"
  → "SELECT id . id FROM id WHERE id . id < num ;"
"""

import sys
import nltk
from g_final_tests import GRAMMAR, parse_count


# Our fake database: table names → valid column names
SCHEMA = {
    "clients": {"id", "name", "age", "city"},
    "orders":  {"id", "client_id", "total"},
}

# (query, grammar_should_pass, schema_should_pass)
TESTS = [
    ("SELECT clients.name, orders.total FROM clients, orders "
     "WHERE clients.id = orders.client_id AND orders.total < 1000;", True, True),
    ("SELECT clients.name FROM clients WHERE clients.age < 30;", True, True),
    ("SELECT clients.name FROM clients WHERE clients.city = 'Monterrey';", True, True),
    ("SELECT clients.email FROM clients;", True, False),   # 'email' not in schema
    ("SELECT clients FROM clients;", False, False),        # can't select a bare table name
]

KEYWORDS   = {"SELECT", "FROM", "WHERE", "OR", "AND"}
PUNCTUATION = [".", ",", ";", "(", ")", "=", "<", "+", "*"]


def split_query(query):
    """Split a query into tokens, treating punctuation as separate tokens."""
    for symbol in PUNCTUATION:
        query = query.replace(symbol, f" {symbol} ")
    return query.split()


def is_name(token):
    """Return True if the token looks like a table or column name (not a number or symbol)."""
    return token.replace("_", "").isalnum() and not token.isdigit()


def to_token_query(query):
    """
    Replace real names/values with generic tokens the grammar understands:
      keywords  → kept as-is   (SELECT, FROM, ...)
      numbers   → 'num'        (42, 1000)
      strings   → 'str'        ('Monterrey')
      names     → 'id'         (clients, total, client_id)
      symbols   → kept as-is   (. , ; < =)
    """
    result = []
    for token in split_query(query):
        upper = token.upper()
        if upper in KEYWORDS:               result.append(upper)
        elif token.isdigit():               result.append("num")
        elif token.startswith("'") and token.endswith("'"): result.append("str")
        elif is_name(token):                result.append("id")
        else:                               result.append(token)
    return " ".join(result)


def check_schema(query):
    """
    Return True if every table and table.column reference in the query
    exists in SCHEMA. Looks for tables in the FROM clause, then checks
    every 'table.column' pair found anywhere in the query.
    """
    tokens = split_query(query)

    # Collect table names listed after FROM (until WHERE or ;)
    tables, reading_from = set(), False
    for token in tokens:
        upper = token.upper()
        if upper == "FROM":             reading_from = True;  continue
        if upper in {"WHERE", ";"}:     reading_from = False
        if reading_from and token != ",": tables.add(token)

    if not tables or any(t not in SCHEMA for t in tables):
        return False

    # Validate every table.column pair
    for i in range(len(tokens) - 2):
        t, dot, col = tokens[i], tokens[i+1], tokens[i+2]
        if is_name(t) and dot == "." and is_name(col):
            if t not in tables or col not in SCHEMA[t]:
                return False

    return True


def print_result(query, token_query, tree_count, grammar_ok, schema_ok):
    print(f"Concrete input:    {query}")
    print(f"Tokenized input:   {token_query}")
    print(f"Syntax:            {'ACCEPT' if grammar_ok else 'REJECT'}")
    print(f"Schema dictionary: {'ACCEPT' if schema_ok else 'REJECT'}")
    print(f"Parse trees:       {tree_count}")


def main():
    parser = nltk.ChartParser(GRAMMAR)

    print("Schema dictionary:")
    for table, columns in SCHEMA.items():
        print(f"  {table}: {', '.join(sorted(columns))}")
    print()

    # If a query was passed on the command line, test just that one
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:]).strip()
        token_query = to_token_query(query)
        tree_count  = parse_count(parser, token_query)
        grammar_ok  = tree_count > 0
        schema_ok   = check_schema(query) if grammar_ok else False
        print_result(query, token_query, tree_count, grammar_ok, schema_ok)
        sys.exit(0)

    all_passed = True
    for query, expected_grammar, expected_schema in TESTS:
        token_query = to_token_query(query)
        tree_count  = parse_count(parser, token_query)
        grammar_ok  = tree_count > 0
        schema_ok   = check_schema(query) if grammar_ok else False
        passed      = (grammar_ok == expected_grammar) and (schema_ok == expected_schema)
        all_passed  = all_passed and passed

        print_result(query, token_query, tree_count, grammar_ok, schema_ok)
        print(f"Result: {'PASS' if passed else 'FAIL'}")
        print("-" * 60)

    if not all_passed:
        print("At least one concrete query test failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()