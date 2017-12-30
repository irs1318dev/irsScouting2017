import pytest
import psycopg2
import psycopg2.pool
import psycopg2.extensions
import sqlalchemy

import Server.model.connection


# Ensure PostgreSQL server running before starting this test

def test_psycopg2_pool():
    # Test assumes minconn = 1 and maxconn = 2
    conn1 = Server.model.connection.pool.getconn()
    assert isinstance(conn1, psycopg2.extensions.connection)
    assert conn1.dsn == ("user=irs1318 password=xxx "
                         "dbname=scouting host=localhost")

    conn2 = Server.model.connection.pool.getconn()
    assert isinstance(conn2, psycopg2.extensions.connection)

    # Requesting another connection causes error because maxconn = 2
    with pytest.raises(psycopg2.pool.PoolError):
        conn3 = Server.model.connection.pool.getconn()
        del conn3

    # Can get another connection if put one away first
    Server.model.connection.pool.putconn(conn1)
    conn3 = Server.model.connection.pool.getconn()
    assert isinstance(conn3, psycopg2.extensions.connection)

    Server.model.connection.pool.closeall()
    assert Server.model.connection.pool.closed


def test_sqlalchemy_engine():
    assert Server.model.connection.engine.name == "postgresql"
    assert "measures" in Server.model.connection.engine.table_names()
    conn1 = Server.model.connection.engine.connect()
    assert isinstance(conn1, sqlalchemy.engine.base.Connection)

    assert not conn1.closed
    conn1.close()
    assert conn1.closed
