from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import ForeignKey

# Here is the connection string for our database.
engine = create_engine('postgresql://irs1318:steamworks@localhost:5432/scouting')

# Set up a database table
Base = declarative_base()

# Create a table



class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

Base.metadata.create_all(engine)

match_number = Match(id=1, name='match number 1')



class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

Base.metadata.create_all(engine)

level_qual = Level(name='Qualifications')
level_playoff = Level(name='Playoffs')


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

Base.metadata.create_all(engine)

station_red = Station(id=1, name='red1')
station_red = Station(id=2, name='red2')
station_red = Station(id=3, name='red3')
station_all = Station(name='na')
station_blue = Station(id=1, name='blue3')
station_blue = Station(id=2, name='blue2')
station_blue = Station(id=3, name='blue3')


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

# Tell the database server to create the table
Base.metadata.create_all(engine)

# Create a team object
tm_irs = Team(id=1318, name='Issaquah Robotics Society')

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

Base.metadata.create_all(engine)


class Phase(Base):
    __tablename__ = "phases"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

Base.metadata.create_all(engine)

auto = Phase(name='auto')
teleop = Phase(name='teleop')
final = Phase(name='final')


class Date(Base):
    __tablename__ = "dates"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

Base.metadata.create_all(engine)


class Alliance(Base):
    __tablename__ = "alliances"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

Base.metadata.create_all(engine)

red = Alliance(name='red')
blue = Alliance(name='blue')


class Task(Base):
    __tablename__ = "taskss"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

Base.metadata.create_all(engine)


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

Base.metadata.create_all(engine)


class Alliance(Base):
    __tablename__ = "alliances"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

Base.metadata.create_all(engine)


class Format(Base):
    __tablename__ = "formats"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

Base.metadata.create_all(engine)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    actor_id = Column(String, ForeignKey('actors.id'))
    task_id = Column(String, ForeignKey('tasks.id'))



class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    event_id= Column(String, ForeignKey('events.id'))
    match_id = Column(String, ForeignKey('matches.id'))
    team_id = Column(String, ForeignKey('teams.id'))
    level_id = Column(String, ForeignKey('levels.id'))
    date_id = Column(String, ForeignKey('dates.id'))
    alliance_id = Column(String, ForeignKey('alliances.id'))
    station_id = Column(String, ForeignKey('stations.id'))


Base.metadata.create_all(engine)


class Measure(Base):
    __tablename__ = "measures"

    id = Column(Integer, primary_key=True)
    team_id = Column(String, ForeignKey('teams.id'))#done
    event_id = Column(String, ForeignKey('events.id'))#done
    match_id = Column(String, ForeignKey('matches.id'))#done
    level_id = Column(String, ForeignKey('levels.id'))#done
    date_id = Column(String, ForeignKey('dates.id'))#partly done
    alliance_id = Column(String, ForeignKey('alliances.id'))#done
    station_id = Column(String, ForeignKey('stations.id'))#partly done
    actor_id = Column(String, ForeignKey('actors.id'))#done need to add
    task_id = Column(String, ForeignKey('tasks.id'))#done need to add
    format_id = Column(String, ForeignKey('formats.id'))#done need to add
    phase_id = Column(String, ForeignKey('phases.id'))#done




Base.metadata.create_all(engine)


# Create a session object that will allow us to talk to the database
Session = sessionmaker(bind=engine)
session = Session()


# Send the team object to the database.
session.add()
session.commit()