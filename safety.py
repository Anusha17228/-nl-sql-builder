import re

BLOCKED_KEYWORDS = [
    "drop",
    "delete",
    "update",
    "insert",
    "alter",
    "truncate",
    "create",
    "replace",
    "attach",
    "pragma"
]


def validate_sql(sql):
    sql = sql.strip().lower()

    if not sql.startswith("select"):
        return False, "Only SELECT queries allowed."

    for word in BLOCKED_KEYWORDS:
        if re.search(rf"\b{word}\b", sql):
            return False, f"Unsafe keyword detected: {word}"

    if ";" in sql[:-1]:
        return False, "Multiple SQL statements blocked."

    return True, "Safe query"