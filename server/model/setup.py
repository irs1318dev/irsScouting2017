"""Creates tables in Scouting PostgreSQL database.

This module is used only for initially setting up a new PostgreSQL
database. It is not used during actual scouting. It contains several
functions that initially setup the database:
* `create_tables()` creates empty tables in the Postgresql server
database, using the classes defined in this module. Each class in this
module corresponds to one database table.
* `insert_dimension_data()` loads data that is essential for the
scouting system to function.
* `setup()` is a convenience function that runs both `create_tables()`
and `insert_dimension_data()`. Run `setup()` once, after creating the
database but before loading any FRC competition data.

To use this module:
1. create a new empty database.
2. Ensure the parameters in Model.connection.db_params correspond to
the database created in step #1.
3. Run `Server.model.setup_database.setup() in a Python console.

This database uses a star schema. The main table that contains the
scouting data is the *measures* table (it's the *fact* table per
star schema terminology). All tables linked to the *measures* table
provide data that desribes the facts listed in the *measures* table.
Per star schema terminology, these tables are dimension tables.

Further reading: https://en.wikipedia.org/wiki/Star_schema
"""

#todo(stacy.irwin) Add season dimension table

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint

import server.model.connection
from server.model.update import upsert, upsert_rows

Base = declarative_base()

# region Main Fact table (star schema)==================================
class Measure(Base):
    """Main fact table with scouting data collected at FRC competitions.
    """
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
    measuretype_id = Column(Integer, ForeignKey('measuretypes.id'),
                            primary_key=True)
    phase_id = Column(Integer, ForeignKey('phases.id'), primary_key=True)
    attempt_id = Column(Integer, ForeignKey('attempts.id'), primary_key=True)
    reason_id = Column(Integer, ForeignKey('reasons.id'), primary_key=True)
    capability = Column(Integer)
    attempts = Column(Integer)
    successes = Column(Integer)
    cycle_times = Column(Integer)

# endregion

# region Dimension Tables (star schema) ================================
class Date(Base):
    """Contains datetime stamps for every event stored in database.

    The datetime is stored as a string with a format of
    YYYY-MM-DDZHH:MM:SS.

    Linked to measures table via measures:date_id field.
    """
    __tablename__ = "dates"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    date = Column(String)


class Event(Base):
    """FIRST API event codes for each competition.

    For example, "waamv", "turing", "wasno".

    Linked to measures table via measures:event_id field.
    """
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    state = Column(String)
    type = Column(String)


class Level(Base):
    """Competition levels. Either "qual", "playoff", or "na".

    Linked to measures table via measures:level_id field.
    """
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Match(Base):
    """String specifying the match.

    Examples: "001-q", "q1.1", "s2.2", "f2", "na", or "pit"

    Linked to measures table via measures:match_id field.
    """
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Alliance(Base):
    """String specifying alliance. Either "red", "blue", or "na".

    Linked to measures table via measures:alliance_id field.
    """
    __tablename__ = "alliances"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Team(Base):
    """FRC Teams. "name" column contains 4-digit FRC number.

    Linked to measures table via measures:team_id field.
    """
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    long_name = Column(String, unique=True)
    city = Column(String)
    state = Column(String)
    region = Column(String)
    year_founded = Column(String)


class Station(Base):
    """Station within alliance to which a team is assigned.

    Can be set to "na", "1", "2", or "3".

    Linked to measures table via measures:station_id field.
    """
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Actor(Base):
    """Entity to which measure (i.e., datapoint) is assigned.

    **Possible Values**
    robot: measures related to robot performance during a match
    drive_team: measures related to drive team performance
    human_player: measures related to the human player
    alliance: measures related to an entire alliance
    team: measures related to an entire team

    Linked to measures table via measures:actor_id field.
    """
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Task(Base):
    """Tasks are the specific items that are measured.

    Tasks are specific to a single game and vary from season to season.
    For example, Steamworks (2017) had tasks such as "placeGear" and
    "teleopFuelPoints".

    Linked to measures table via measures:task_id field.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    type = Column(String)
    display_name = Column(String)


class MeasureType(Base):
    """Describes the type of data stored in the Measure table.

    Examples: "count", "percentage", "boolean", "enum", "cycletime"

    Linked to measures table via measures:measuretype_id field.
    """
    __tablename__ = "measuretypes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Phase(Base):
    """Describes competition phase to which measure applies.

    Linked to measures table via measures:phase_id field.

    Examples: "claim", "teleop", "finish", "auto"
    """
    __tablename__ = "phases"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Attempt(Base):
    """Not sure what this is used for.

    Can be string of integers 1 - 30 or "summary". Only "summary" value
    was used in 2017.

    Linked to measures table via measures:attempt_id field.
    """
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Reason(Base):
    """Not sure what this is ueed for.

    Can be "dropped", "blocked", "defended" or "na". Only "na" used in
    2017.

    Linked to measures table via measures:reason_id field.
    """
    __tablename__ = "reasons"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

# endregion

# region Tables for managing user interface ============================


class Status(Base):
    """Stores the current event and match.

    Used by the scouting system user interface.
    """
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    event = Column('event', String)
    match = Column('match', String)


class TaskOptions(Base):
    """This table is used to configure the user interface.

    This table provides options for user interface selection boxes on
    the corresponding Android application. It is not linked to any
    other tables in the database.
    """
    __tablename__ = "task_options"

    id = Column(Integer, primary_key=True)
    task_name = Column(String)
    type = Column(String)
    option_name = Column(String)
    __table_args__ = (UniqueConstraint('task_name', 'type', 'option_name'),)

# endregion

# region Tables that customize system for different seasons ============


class Game(Base):
    """List all tasks applying to a specific game for a single season.

    This table is not linked to any other tables in the scouting
    database.
    """
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    actor = Column(String)
    task = Column(String, unique=True)
    claim = Column(String)
    auto = Column(String)
    teleop = Column(String)
    finish = Column(String)

# endregion

# region Other Tables (perhaps unused) =================================


class Schedule(Base):
    """Contains the schedule downloaded from the FIRST API.

    This table is not linked to any other tables in the database.
    """
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    date = Column('date', String)
    event = Column('event', String)
    level = Column('level', String)
    match = Column('match', String)
    alliance = Column('alliance', String)
    team = Column('team', String)
    station = Column('station', String)


class MatchResult(Base):
    """This table was not used in 2017.

    Not sure what this table was intended for. Might have been for
    storing official match scores.
    """
    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True)

# endregion

# region Functions for initializing database ===========================

def create_tables(engine=server.model.connection.engine):
    Base.metadata.create_all(engine)


def initialize_dimension_data(engine=server.model.connection.engine):
    """Loads initial dimension data into database.

    The dimension data loaded by this function is essential for the
    scouting system to operate and must be loaded before recording
    any competition data (but after creating the tables with
    `create_tables()`.
    """
    upsert("levels", "name", "na", engine)
    upsert("levels", "name", "qual", engine)
    upsert("levels", "name", "playoff", engine)

    upsert_rows("matches", "name", 150, "{0:0>3}-q", engine)
    upsert("matches", "name", "na", engine)
    upsert("matches", "name", "q1.1", engine)
    upsert("matches", "name", "q1.2", engine)
    upsert("matches", "name", "q1.3", engine)
    upsert("matches", "name", "q2.1", engine)
    upsert("matches", "name", "q2.2", engine)
    upsert("matches", "name", "q2.3", engine)
    upsert("matches", "name", "q3.1", engine)
    upsert("matches", "name", "q3.2", engine)
    upsert("matches", "name", "q3.3", engine)
    upsert("matches", "name", "s1.1", engine)
    upsert("matches", "name", "s1.2", engine)
    upsert("matches", "name", "s1.3", engine)
    upsert("matches", "name", "s2.1", engine)
    upsert("matches", "name", "s2.2", engine)
    upsert("matches", "name", "s2.3", engine)
    upsert("matches", "name", "f1", engine)
    upsert("matches", "name", "f2", engine)
    upsert("matches", "name", "f3", engine)

    upsert("alliances", "name", "na", engine)
    upsert("alliances", "name", "blue", engine)
    upsert("alliances", "name", "red", engine)

    upsert("dates", "name", "na", engine)

    # teams imported from schedule
    upsert("teams", "name", 'na', engine)

    upsert("stations", "name", "na", engine)
    upsert("stations", "name", "1", engine)
    upsert("stations", "name", "2", engine)
    upsert("stations", "name", "3", engine)

    upsert("actors", "name", "na", engine)
    upsert("actors", "name", "drive_team", engine)
    upsert("actors", "name", "robot", engine)
    upsert("actors", "name", "pilot", engine)
    upsert("actors", "name", "human_player", engine)
    upsert("actors", "name", "alliance", engine)
    upsert("actors", "name", "team", engine)

    # tasks imported from game
    upsert("tasks", "name", 'na', engine)

    upsert("measuretypes", "name", "na", engine)
    upsert("measuretypes", "name", "count", engine)
    upsert("measuretypes", "name", "percentage", engine)
    upsert("measuretypes", "name", "boolean", engine)
    upsert("measuretypes", "name", "enum", engine)
    upsert("measuretypes", "name", "attempt", engine)
    upsert("measuretypes", "name", "cycletime", engine)

    upsert("phases", "name", "na", engine)
    upsert("phases", "name", "claim", engine)
    upsert("phases", "name", "auto", engine)
    upsert("phases", "name", "teleop", engine)
    upsert("phases", "name", "finish", engine)

    upsert("attempts", "name", "summary", engine)
    upsert_rows("attempts", "name", 31, "{0:0>2}", engine)

    upsert("reasons", "name", "na", engine)
    upsert("reasons", "name", "dropped", engine)
    upsert("reasons", "name", "blocked", engine)
    upsert("reasons", "name", "defended", engine)


def setup(engine=server.model.connection.engine):
    """Creates tables and inserts initial dimension data.

    Args:
        engine: database engine. Optional. Default is production
            scouting database.
    """
    create_tables(engine)
    initialize_dimension_data(engine)

# endregion
