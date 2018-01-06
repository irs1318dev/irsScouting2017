"""Provides connections to the PostgreSQL database.

This module provides connections to the PostgreSQL database server via
both the pscyopg2 package and the sqlalchemy package. The pyscopg2
connection pool and sqlalchemy engine objects are created as soon as
connection.py is imported.

The database connection parameters are available via the Python
dictionary, `Server.connection.db_params`.

The keys for the connections.db_params dictionary are:
    minconn: Number of database connections when psycopg2
        connection.pool is first initialized.
    maxconn: Maximum number of database connections that will be
        available in psycopg2 connection.pool.
    username: Database account username
    password: Database account password
    dbname: Database name
    host: Hostname of computer running database server.
    port: port number on which database server is running.

Examples:
    # Usage of sqlalchemy database engine
    db_connection = Server.model.connection.engine.connect()
    # ... do database stuff ...
    db_connection.close()  #Releases connection back to pool

    # Basic useage of psycopg2 connection pool
    import Server.connection
    db_connection = Server.connection.pool.getconn()
    # ... do database stuff...
    Server.connection.pool.putconn(db_connection)  #Releases connection.


    # Reset psycopg2 connection pool with new default parameters
    Server.connection.reset_pool(username="postgres", password="otherPW")
    db_connection2 = Server.connection.pool.getconn()

References:
    Sqlalchemy:
    http://initd.org/psycopg/docs/pool.html

"""

import psycopg2.pool
import sqlalchemy

db_params = {"minconn": 1,
             "maxconn": 2,
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
    global engine
    if engine is not None:
        engine.dispose()
    engine = sqlalchemy.create_engine(conn_string)
    return engine


# Create psycopg2 connection pool
pool = None


def _set_pool(minconn=db_params["minconn"], maxconn=db_params["maxconn"],
              dbname=db_params["dbname"], host=db_params["host"],
              user=db_params["user"], password=db_params["password"]):
    """Internal function for creating a connection pool.

    Args: Same as connection.reset_pool
    """
    global pool
    pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn, dbname=dbname,
                                              host=host, user=user,
                                              password=password)


_set_pool()


def reset_pool(minconn=db_params["minconn"], maxconn=db_params["maxconn"],
               dbname=db_params["dbname"], host=db_params["host"],
               user=db_params["user"], password=db_params["password"]):
    """Closes all existing pool connections and creates a new pool.

    The reset_pool function allows users to create a new connection pool
    with parameters other than the default parameters specified in
    connection.db_params.

    WARNING: This function will close all existing database connections!

    Args:
        minconn:
            Number of database connections when connection.pool is
            first initialized.
        maxconn:
            Maximum number of database connections that will be
            available in connection.pool.
        user:
            Database account username
        password:
            Databvase account password
        dbname:
            Database name
        host:
            Hostname of computer running database server.
    """
    if pool is not None:
        pool.closeall()
    del pool
    _set_pool(minconn, maxconn, dbname, host, user, password)
