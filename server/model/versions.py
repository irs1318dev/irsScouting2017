import sqlalchemy as sa

# import server.model
import server.model.connection as smc


def add_seasons():
    """
    Date Created: 2/2/18

    Purpose: Makes it so data is only received from one specified year
    Sets season to 2017
    Use in cases where season column does not exist and or if it is
    unpopulated
    :return:
    """
    conn = smc.engine.connect()

    select = sa.text("ALTER TABLE events ADD COLUMN season varchar(4);")

    conn.execute(select)
    was = sa.text("UPDATE events SET season = 2017;")
    conn.execute(was)
    conn.close()


add_seasons()


