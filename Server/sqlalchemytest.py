from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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


class Phase(Base):
    __tablename__ = "phases"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

Base.metadata.create_all(engine)

auto = Phase(name='auto')
teleop = Phase(name='teleop')
final = Phase(name='final')


class Measure(Base):
    __tablename__ = "measures"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id')) #done
    event_id = Column(Integer, ForeignKey('events.id')) #not done
    match_id = Column(Integer, ForeignKey('matches.id')) #done
    level_id = Column(Integer, ForeignKey('levels.id')) #done
    date_id = Column(Integer, ForeignKey('dates.id')) #not done
    alliance_id = Column(Integer, ForeignKey('alliances.id')) #not done
    station_id = Column(Integer, ForeignKey('stations.id')) #partly done
    actor_id = Column(Integer, ForeignKey('actors.id')) #not done
    task_id = Column(Integer, ForeignKey('tasks.id')) #not done
    format_id = Column(Integer, ForeignKey('formats.id')) #not done
    phase_id = Column(Integer, ForeignKey('phases.id')) #done


Base.metadata.create_all(engine)

# Create a session object that will allow us to talk to the database
Session = sessionmaker(bind=engine)
session = Session()


# Send the team object to the database.
session.add(match_number)
session.commit()