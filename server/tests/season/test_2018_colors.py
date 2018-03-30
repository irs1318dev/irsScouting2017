<<<<<<< HEAD
=======
import pandas
import sqlalchemy

import server.model.connection as sm_connection
import server.model.event as sm_event
>>>>>>> 3a5c55acd167d6b0f8d658b9541dcc8f8704ed86
import server.season.s2018.api_measures as s2018api
import server.model.dal as sm_dal
import server.model.setup as sm_setup


<<<<<<< HEAD
def test_colors():
    s2018api.download_platform_color()
    # print(sm_dal.task_ids)
    # sm_setup.load_game_sheet("2018")
=======
# def test_colors():
#     event_id = sm_event.EventDal.set_current_event("wamou", "2018")
#     s2018api.download_platform_color()
#
#     sql = sqlalchemy.text(
#         "SELECT matches.name, tasks.name AS task, "
#         "  task_options.option_name AS value "
#         "FROM measures INNER JOIN tasks ON measures.task_id = tasks.id "
#         "  INNER JOIN matches ON measures.match_id = matches.id "
#         "  INNER JOIN task_options ON measures.capability = task_options.id "
#         "WHERE tasks.name = 'assignColors' AND measures.event_id = :evt_id;"
#     ).bindparams(evt_id=event_id)
#
#     conn = sm_connection.engine.connect()
#     df = pandas.read_sql(sql, conn)
#
#     assert df.shape == (78, 3)
#
#     unique_values = df["value"].unique()
#     assert len(unique_values) == 4
#     assert 'BBB' in unique_values
#     assert 'RBR' in unique_values
#     assert 'BRB' in unique_values
#     assert 'RRR' in unique_values
#
#     conn.close()
>>>>>>> 3a5c55acd167d6b0f8d658b9541dcc8f8704ed86
