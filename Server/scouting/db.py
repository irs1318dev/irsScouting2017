from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint


# ========== Database Connection ==============================================
connection_string = 'postgresql://irs1318:irs1318@localhost:5432/scouting'
engine = create_engine(connection_string)

def getdbengine():
    return engine


# ========== Table Definitions ================================================
Base = declarative_base()


class Date(Base):
    __tablename__ = "dates"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    date = Column(String)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    state = Column(String)
    type = Column(String)


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Alliance(Base):
    __tablename__ = "alliances"

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


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    type = Column(String)
    display_name = Column(String)


class MeasureType(Base):
    __tablename__ = "measuretypes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Phase(Base):
    __tablename__ = "phases"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Reason(Base):
    __tablename__ = "reasons"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    actor = Column(String)
    task = Column(String, unique=True)
    claim = Column(String)
    auto = Column(String)
    teleop = Column(String)
    finish = Column(String)


class TaskOptions(Base):
    __tablename__ = "task_options"

    id = Column(Integer, primary_key=True)
    task_name = Column(String)
    type = Column(String)
    option_name = Column(String)
    __table_args__ = (UniqueConstraint('task_name', 'type', 'option_name'),)


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    date = Column('date', String)
    event = Column('event', String)
    level = Column('level', String)
    match = Column('match', String)
    alliance = Column('alliance', String)
    team = Column('team', String)
    station = Column('station', String)


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
    attempt_id = Column(Integer, ForeignKey('attempts.id'), primary_key=True)
    reason_id = Column(Integer, ForeignKey('reasons.id'), primary_key=True)
    capability = Column(Integer)
    attempts = Column(Integer)
    successes = Column(Integer)
    cycle_times = Column(Integer)


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    event = Column('event', String)
    match = Column('match', String)


class Match_Result(Base):
    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True)



def create_tables():
    engine = getdbengine()
    Base.metadata.create_all(engine)
