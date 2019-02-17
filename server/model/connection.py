"""Provides connections to the PostgreSQL database.

This module provides connections to the PostgreSQL database server via
both the sqlalchemy and pscyopg2 packages. The sqlalchemy engine and
pyscopg2 connection pool objects are created as soon as connection.py
is imported.


Module Attributes
-----------------

`server.model.connection.engine`:
    A sqlalchemy engine object that is
    necessary to connect to the Postgresql server via the sqlalchemy
    package. The engine object functions as a connection pool, creating,
    providing, re-using, and disposing of database connections. Use the
    server.model.connection.engine object for all scouting system
    database connections. Sqlalchemy supports higher-level operations and
    works with Pandas dataframes.

`server.model.connection.pool`:
    This module also facilitates database operations using the
    psycopg2 Python package. The `server.model.connection.pool`
    attribute is a pyscopg2 connection pool object that manages
    database connections similarly to sqlalchemy engine objects.
    Unless you have a specific reason, use the sqlalchemy engine
    object instead the psycopg2 object for database connections. The
    psycopg package is used sparingly in the scouting system,
    but there are some database operations that are simpler to
    complete with psycopg2 than sqlalchemy. For example The psycopg2
    package is used to create a test database for unit testing.

`server.model.connection.db_params`
    Production database connection parameters are also stored in this
    module, in the db_params attribute. Both the the sqlalchemy
    engine (`server.model.connection.engine`) and psycopg2 connection
    pool (`server.model.connection.pool`) are initialized with these
    parameters the first time this module is implemented by the
    scouting system. There should not be any other references to
    production database connection parameters anywhere else in the
    scouting system -- this enables the IRS to change database
    connection parameters by changing only this module. The keys for
    the connections.db_params dictionary are:
        minconn: Number of database connections when psycopg2
            connection.pool is first initialized.
        maxconn: Maximum number of database connections that will be
            available in psycopg2 connection.pool.
        username: Database account username
        password: Database account password
        dbname: Database name
        host: Hostname of computer running database server.
        port: port number on which database server is running.


Module Functions
----------------

`server.model.connection.create_conn_string()`: Creates a sqlalchemy
connection string.

`server.model.connection.reset_engine(conn_string)`: Resets the
sqlalchemy engine object that is available via the
server.model.connection attribute with the new database parameters
passed in the conn_string argument. Use the `create_conn_string()`
function to create the conn_string argument.

`server.model.connection.set_pool()`: Creates a new psycopg2 connection
pool and make it available vie the server.model.connection.pool
attribute.

`server.model.connection.reset_pool()`: Resets the pgsql connection
pool with different database parameters.


Examples
--------

    # Usage of sqlalchemy database engine
    import server.model.connection as smc
    db_connection = smc.engine.connect()
    # ... do database stuff ...
    db_connection.close()  #Releases connection back to pool

    # Usage of psycopg2 connection pool
    import Server.model.connection as smc
    db_connection = smc.pool.getconn()
    # ... do database stuff...
    smc.pool.putconn(db_connection)  #Releases connection.

    # Reset sqlalchemy database engine
    conn_str_ts = smc.create_conn_string(dbname="test_database",
                                         user="irs_tester",
                                         password="irs_test_pw")
    smc.reset_engine(conn_string_ts)
    conn = smc.engine.connect()

    # Reset psycopg2 connection pool with new default parameters
    smc.set_pool(username="postgres", password="otherPW")
    db_connection2 = smc.pool.getconn()

References
----------
    Sqlalchemy: http://docs.sqlalchemy.org/en/latest/
    http://initd.org/psycopg/docs/pool.html

"""

import psycopg2.pool
import sqlalchemy

# todo(stacy) Move password and username to auth.py.
# todo(stacy) Move connection settings to server.conf.py

db_params = {"minconn": 1,
             "maxconn": 5,
             "user": "irs1318",
             "password": "irs1318",
             "dbname": "scouting",
             "host": "localhost",
             "port": "5432"}


def create_conn_string(user=db_params["user"],
                       password=db_params["password"],
                       dbname=db_params["dbname"],
                       host=db_params["host"],
                       port=db_params["port"]):
    """Creates a sqlalchemy connection string.

    Args:
        user: Database account username
        password: Database account password
        dbname: Database name
        host: Hostname of computer running database server.
        port: port number on which database server is running.

    Returns: Connection string in the format of
        {db_name}://{user}:{password}@{host}:{port}/{dbname}

    Example string:
        'postgresql://irs1318:irs1318@localhost:5432/scouting'
    """
    return ("postgresql" + "://" + user + ":" + password +
            "@" + host + ":" + port + "/" + dbname)


engine = sqlalchemy.create_engine(create_conn_string())


def reset_engine(conn_string):
    """Creates new sqlalchemy engine from parameters in conn_string arg.

    By default, server.model.connection.engine connects to the
    production scouting database. This function will dispose of the
    default engine and create a new engine using whatever
    parameters are passed in the conn_string argument.

    Args:
        conn_string: A string containing database parameters such as
        username, database name, host, etc. See the documentation for
        server.model.connection.create_conn_string for more detail.
    """
    global engine
    if engine is not None:
        engine.dispose()
    engine = sqlalchemy.create_engine(conn_string)


# Create psycopg2 connection pool
def set_pool(minconn=db_params["minconn"], maxconn=db_params["maxconn"],
             dbname=db_params["dbname"], host=db_params["host"],
             user=db_params["user"], password=db_params["password"]):
    """Internal function for creating a connection pool.

    Args: Same as connection.reset_pool
    """
    return psycopg2.pool.SimpleConnectionPool(minconn, maxconn,
                                              dbname=dbname,
                                              host=host, user=user,
                                              password=password)


pool = set_pool()


def reset_pool(minconn=db_params["minconn"], maxconn=db_params["maxconn"],
             dbname=db_params["dbname"], host=db_params["host"],
             user=db_params["user"], password=db_params["password"]):
    global pool
    pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn,
                                              dbname=dbname,
                                              host=host, user=user,
                                              password=password)

