import sqlalchemy
import server.model.connection


def build_dicts(dim_table):
    """Returns dictionaries for cross-referencing ID fields to values.

    Args:
        dim_table: (str) Name of dimension table in scouting database.

    Returns: A tuple containing two dictionaries. The keys of the first
    dictionary are the values in the table's *name* column and the
    values are the integer from the ID column for the same row. The
    second dictionary has ID values for keys and the values are from
    the *name* column.
    """
    name_to_id = {}
    id_to_name = {}
    conn = server.model.connection.engine.connect()

    if dim_table.lower() == "task_options":
        sql = sqlalchemy.text("SELECT id, task_name||'-'||option_name "
                              "as name FROM task_options")
    else:
         sql = sqlalchemy.text("SELECT id, name FROM " + dim_table)

    dim_res = conn.execute(sql)
    for row in dim_res:
        name_to_id[row["name"]] = row["id"]
        id_to_name[row["id"]] = row["name"]

    dim_res.close()
    conn.close()
    return name_to_id, id_to_name



