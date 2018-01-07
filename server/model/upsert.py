"""Provides utility functions for inserting data into scouting database.

The functions in this module take advantage of a relatively new feature
in Structured Query Language (SQL) known as "Upsert". Upsert statements
are a compination of a SQL UPDATE statement in INSERT statement. With
an UPDATE statement, if the data we're trying to write to the database
is already in the database, the databaase server will often throw  an
error due to uniqueness constraints on the data. By using the upsert
feature, the function will update the existing data instead of throwing
an error. Note that the word "UPSERT" does not actually appear in the
SQL statement -- the upserte functionality comes from the "ON CONFLICT"
portion of the SQL statement.

Module Functions
----------------
`server.module.upsert.upsert`: Inserts or updates a single field in a
single row of a database table.
`server.module.upsert.upsert_rows`: Inserts or updates a single field in
multiple rows of a database table.
`server.module.upsert.upsert_cols`: Inserts or updates multiple fields
(i.e., columns) in a single row of a database table.
"""
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

    Note that upsert only works if there are unique contstraints on
    affected fields.

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


def upsert_rows(table, col, n, template):
    """Insert a range of values containing integers from 1 to n.

    Inserts n rows into the database table, each containing the string
    passed in the `tempate` argument. The template argument should
    conform to the format string syntax required for the Python
    `str.format()` function. The template string can contain up to one
    field. The upsert_Range functionw will insert an integer into the
    location specified by the field.

    Note that upsert only works if there are unique contstraints on
    affected fields.

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


def upsert_cols(table, data):
    """Adds a row to a table, simultaneously updating several columns.

    The data argument is a Python dictionary that specifies what will
    be inserted into the database table. The dictionary is of the form:
    {"column1 name": "column1 value", "column2 name": "column2 value"}

    If the row already exists in the database, this funciton will
    update the row (instead of throwing an error).

    Note that upsert only works if there are unique contstraints on
    affected fields.

    Args:
        table: The name of the table into which data will be inserted.
        data: A Python dictionary where the key is the column nama and
            the dictionary value is the value that will be inserted into
            the database column.
    """
    conn = server.model.connection.engine.connect()

    # Build string containing column names
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
