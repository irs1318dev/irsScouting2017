import scouting.db
import scouting.db_dimensiondata
import scouting.load_data


def run():
    scouting.db.create_tables()
    scouting.db_dimensiondata.insert_data()
    scouting.load_data.load_game_sheet()


def event(setevent):
    scouting.load_data.insert_sched(setevent, '2017', 'qual')
    scouting.load_data.insert_MatchResults(setevent, '2017', 'qual')
