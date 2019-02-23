import server.model.connection as smc
import server.season.s2019.view.oneteam as oneteam


def test_get_cds():
    conn = smc.pool.getconn()
    meas_df = oneteam.onet_d('3223', conn)
    tasks = ['getHatch', 'csHatch', 'rocketHatch1', 'rocketHatch2',
               'rocketHatch3']
    print(oneteam.get_cds_averages(meas_df, tasks, 4).column_names)

    smc.pool.putconn(conn)