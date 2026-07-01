import sqlite3


def extract_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

    tables = cursor.fetchall()
    schema = {}

    for table in tables:
        table_name = table[0]

        cursor.execute(
            f"PRAGMA table_info({table_name})"
        )

        columns = cursor.fetchall()

        schema[table_name] = []

        for col in columns:
            schema[table_name].append({
                "name": col[1],
                "type": col[2]
            })

    conn.close()
    return schema


def execute_query(db_path, sql):
    conn = sqlite3.connect(db_path)

    try:
        cursor = conn.cursor()
        cursor.execute(sql)

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        conn.close()

        return rows, columns, None

    except Exception as e:
        conn.close()
        return None, None, str(e)