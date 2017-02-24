from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy import ForeignKey

# ========== Database Connection ==============================================
connection_string = 'postgresql://irs1318:irs1318@localhost:5432/scouting'


def getdbengine():
    return create_engine(connection_string)


# ========== Table Definitions ================================================
Base = declarative_base()


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    state = Column(String)
    type = Column(String)


class Phase(Base):
    __tablename__ = "phases"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Date(Base):
    __tablename__ = "dates"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    date = Column(String)


class Alliance(Base):
    __tablename__ = "alliances"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Reason(Base):
    __tablename__ = "reasonss"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    type = Column(String)
    display_name = Column(String)


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class MeasureType(Base):
    __tablename__ = "measuretypes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    long_name = Column(String, unique=True)
    city = Column(String)
    state = Column(String)
    region = Column(String)
    year_founded = Column(String)


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    event = Column(String,'event')
    match = Column(String, 'match')
    team = Column(String,'team')
    level = Column(String,'level')
    date = Column(String, 'date')
    alliance = Column(String,'alliance')
    station = Column(String,'station')
    match_status = Column(String, 'match_status')
    tablet_status = Column(String, 'tablet_status')

class Measure(Base):
    __tablename__ = "measures"

    date_id = Column(Integer, ForeignKey('dates.id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), primary_key=True)
    level_id = Column(Integer, ForeignKey('levels.id'), primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'), primary_key=True)
    alliance_id = Column(Integer, ForeignKey('alliances.id'), primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), primary_key=True)
    station_id = Column(Integer, ForeignKey('stations.id'), primary_key=True)
    actor_id = Column(Integer, ForeignKey('actors.id'), primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True)
    measuretype_id = Column(Integer, ForeignKey('measuretypes.id'), primary_key=True)
    phase_id = Column(Integer, ForeignKey('phases.id'), primary_key=True)
    attempt_id = Column(Integer, ForeignKey('attempt.id'), primary_key=True)
    reason_id = Column(Integer, ForeignKey('reason.id'), primary_key=True)
    capability = Column(Integer)
    attempts = Column(Integer)
    successes = Column(Integer)
    cycle_time = Column(Integer)



def createTables():
    engine = getdbengine()
    Base.metadata.create_all(engine)



def loadMasterData():
    engine = getdbengine()
    conn = engine.connect()
    for i in range(1, 201):
        match = "match " + str(i)
        select = text(
            "INSERT INTO matches(name) "
            "VALUES (:name) "
            "ON CONFLICT (name) "
            "DO "
                "UPDATE "
                    "SET name = :name WHERE $name;"

        )
        conn.execute(select, name=match)



# ====================== Add Data to Tables =================================

# Session = sessionmaker(bind=engine)
# session = Session()


#match_number = Match(id=1, name='match number 1')

#level_qual = Level(name='Qualifications')
#level_playoff = Level(name='Playoffs')


 #session.add_all([level_playoff, level_qual])

#session.commit()

# All dimensions tables have id(serial), name (unique)
#
# class Station(Base):
#     __tablename__ = "stations"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#
#
# station_red = Station(id=1, name='red1')
# station_red = Station(id=2, name='red2')
# station_red = Station(id=3, name='red3')
# station_all = Station(name='na')
# station_blue = Station(id=1, name='blue3')
# station_blue = Station(id=2, name='blue2')
# station_blue = Station(id=3, name='blue3')
#
#
# class Team(Base):
#     __tablename__ = "teams"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#
# # Tell the database server to create the table
#
# # Create a team object
# tm_irs = Team(id=1318, name='Issaquah Robotics Society')
#    region, state, city
#
#
# class Event(Base):
#     __tablename__ = "events"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#       #state and type(district, championships)
#
#
# class Phase(Base):
#     __tablename__ = "phases"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#
#
# auto = Phase(name='auto')
# teleop = Phase(name='teleop')
# post = Phase(name='post')
# prep = Phase(name='prep')
# na = Phase(name='na')
#
#
# class Date(Base):
#     __tablename__ = "dates"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#
#
#
# class Alliance(Base):
#     __tablename__ = "alliances"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#
#
# red = Alliance(name='red')
# blue = Alliance(name='blue')
#
#
# class Game(Base):
#     __tablename__ = "games"
#
#     id = Column(Integer, primary_key=True)
#     actor_id = Column(String, ForeignKey('actors.id'))
#     task_id = Column(String, ForeignKey('tasks.id'))
#
#
#


#
#
# Create a session object that will allow us to talk to the database

#
# # Send the team object to the database.
# session.add()
# session.commit()