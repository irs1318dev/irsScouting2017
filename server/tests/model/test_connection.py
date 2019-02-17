"""Tests code in server.model.connection.py
"""
import psycopg2
import psycopg2.pool
import psycopg2.extensions
import sqlalchemy

import server.model.connection
import server.tests.conf as conf


# Ensure PostgreSQL server running before starting this test

def test_psycopg2_pool():
    # Test assumes minconn = 1 and maxconn = 2
    conn1 = server.model.connection.pool.getconn()
    assert isinstance(conn1, psycopg2.extensions.connection)
    test_dsn = ("user=" + conf.user + " password=xxx"
                " dbname=" + conf.db + " host=" + conf.host)
    assert conn1.dsn == test_dsn
    server.model.connection.pool.putconn(conn1)


def test_sqlalchemy_engine():
    assert server.model.connection.engine.name == "postgresql"
    assert "measures" in server.model.connection.engine.table_names()
    conn1 = server.model.connection.engine.connect()
    assert isinstance(conn1, sqlalchemy.engine.base.Connection)

    assert not conn1.closed
    conn1.close()
    assert conn1.closed
