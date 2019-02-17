import server.model.connection as smc
import server.model.event as sme



def test_view():
    """test assumes you have 2019 test_data event data
    """
    conn = smc.pool.getconn()
    curr = conn.cursor()
    sql = '''TABLE vw_measures;'''
    sme.EventDal.set_current_event('test_data', '2019')
    curr.execute(sql)
    a = curr.fetchone()

    assert a[1] == 'test_data'  # event column
    assert a[2] == '2019'  # season column
    assert a[3] == 'qual'  # level column

    sql = '''SELECT ver FROM status;'''
    curr.execute(sql)
    b = curr.fetchone()
    assert b[0] == '2019.01'
    curr.close()
    smc.pool.putconn(conn)
