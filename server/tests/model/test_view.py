import server.model.connection as smc
import server.model.event as sme



def test_view():
    """test assumes you have 2019 test_data event data
    """
    sql = '''TABLE graph;'''
    conn = smc.pool.getconn()
    sme.EventDal.set_current_event('test_data', '2019')
    curr = conn.cursor()
    curr.execute(sql)
    a = curr.fetchone()
    assert a[1] == 'test_data'  # event column
    assert a[2] == '2019'  # season column
    assert a[3] == 'qual'  # level column
