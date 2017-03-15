import psycopg2
import psycopg2.pool



class ConnectionPool(object):

    pool = psycopg2.pool.SimpleConnectionPool(minconn=1, maxconn=2,
                                            dbname='scouting', host='localhost', user='postgres',  password = 'irs1318')


    @staticmethod
    def get_conn(self):
        return pool.getconn()

    @staticmethod
    def put_conn(conn):
        return pool.putconn(conn)