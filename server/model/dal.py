import re

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
    return id_to_name, name_to_id


date_names, date_ids = build_dicts("dates")
event_names, event_ids = build_dicts("events")
level_names, level_ids = build_dicts("levels")
match_names, match_ids = build_dicts("matches")
alliance_names, alliance_ids = build_dicts("alliances")
team_names, team_ids = build_dicts("teams")
station_names, station_ids = build_dicts("stations")
actor_names, actor_ids = build_dicts("actors")
task_names, task_ids = build_dicts("tasks")
measuretype_names, measuretype_ids = build_dicts("measuretypes")
phase_names, phase_ids = build_dicts("phases")
attempt_names, attempt_ids = build_dicts("attempts")
reason_names, reason_ids = build_dicts("reasons")
task_option_names, task_option_ids = build_dicts("task_options")
task_option_options = {key: re.sub(r"^[^-]+-", "", val, count=1)
                       for key, val in task_option_names.items()}


def rebuild_dicts():
    global date_names, date_ids, event_names, event_ids
    global level_names, level_ids, match_names, match_ids
    global alliance_names, alliance_ids, team_names, team_ids
    global station_names, station_ids, actor_names, actor_ids
    global task_names, task_ids, measuretype_names, measuretype_ids
    global phase_names, phase_ids, attempt_names, attempt_ids
    global reason_names, reason_ids, task_option_names, task_option_ids

    date_names, date_ids = build_dicts("dates")
    event_names, event_ids = build_dicts("events")
    level_names, level_ids = build_dicts("levels")
    match_names, match_ids = build_dicts("matches")
    alliance_names, alliance_ids = build_dicts("alliances")
    team_names, team_ids = build_dicts("teams")
    station_names, stations_ids = build_dicts("stations")
    actor_names, actor_ids = build_dicts("actors")
    task_names, task_ids = build_dicts("tasks")
    measuretype_names, measuretype_ids = build_dicts("measuretypes")
    phase_names, phase_ids = build_dicts("phases")
    attempt_names, attempt_ids = build_dicts("attempts")
    reason_names, reasons_ids = build_dicts("reasons")
    task_option_names, task_option_ids = build_dicts("task_options")