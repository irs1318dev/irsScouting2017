import sqlalchemy

import server.model.connection


def upsert(table, col, val):
    """ Inserts value into database table, or updates if already exists.

    This function is intended for inertering values into dimension
    tables using a SQL INSERT query. Normally an error occurs when
    attempting to insert a value that already exists into a dabase
    column (assuming no duplicates are allowed). The ON CONFLICT DO
    UPDATE portion of the SQL statement tells the database server to
    overwrite the existing value instead of throwing an error. This
    type of statement is called an UPSERT.

    Using an UPSERT here allows the scouting system to add rows to
    dimension tables without having to determine if some or all of the
    data already exists.

    Args:
        table: Database table into which value should be inserted.
        col: Column into which value should be inserted
        val: Value to be inserted.
    """
    conn = server.model.connection.engine.connect()
    select = sqlalchemy.text(
        "INSERT INTO " + table + " (" + col + ") " +
        "VALUES (:val) "
        "ON CONFLICT " + "(" + col + ")" +
        " DO UPDATE "
        "SET " + col + " = :val RETURNING id; "
    )
    conn.execute(select, val=val)
    conn.close()


def upsert_range(table, col, n, template):
    """Insert a range of values containing integers from 1 to n.

    Inserts n rows into the database table, each containing the string
    passed in the `tempate` argument. The template argument should
    conform to the format string syntax required for the Python
    `str.format()` function. The template string can contain up to one
    field. The upsert_Range functionw will insert an integer into the
    location specified by the field.

    For example, calling
    `upsert_range("matches", "name", 150, "{0:0>3}-q")` will insert
    150 rows into the *matches* table. The value in the *name* column
    will be 001-q, 002-q, 003-1, ... through 150-q.

    Args:
        table: Database table into which value should be inserted.
        col: Column into which value should be inserted
        n: Positive integer.
        template: Python format string that accepts up to one parameter.
    """
    conn = server.model.connection.engine.connect()
    for i in range(1, n):
        name = template.format(i)
        sql = sqlalchemy.text(
            "INSERT INTO " + table + " (" + col + ") " +
            "VALUES (:name) "
            "ON CONFLICT (" + col + ") " +
            "DO UPDATE "
            "SET " + col + " = :name RETURNING id; "

        )
        conn.execute(sql, name=name)
    conn.close()


def add_many_cols(table, data) :
    conn = server.model.connection.engine.connect()

    # Buld string containing column names
    col_names = ""
    val_data = ""
    set_data = ""
    for col, _ in data.items():
        if col_names == "":
            col_names = col
            val_data = ':' + col
            set_data = col + '=:' + col
        else:
            col_names = col_names + ", " + col
            val_data = val_data + ", :" + col
            set_data = set_data + ", " + col + '=:' + col

    sql = sqlalchemy.text(
        "INSERT INTO " + table + " (" + col_names + ") " +
        "VALUES (" + val_data + ")"
        "ON CONFLICT (" + col_names + ") " +
        "DO UPDATE "
        "SET " + set_data + " ; "
    )
    conn.execute(sql, **data)
    conn.close()