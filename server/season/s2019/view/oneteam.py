import pandas as pd
import bokeh.plotting
import bokeh.models as bmodels
import bokeh.plotting as plt
import bokeh.palettes as bpalettes
import bokeh.transform as btransform
import bokeh.io

import server.model.connection as smc


def onet_g(team, num_matches):
    conn = smc.pool.getconn()

    data = _onet_d(team, conn)

    hatches = data.query('task == ["getHatch", "csHatch", "rocketHatch1",'
                         '"rocketHatch2", "rocketHatch3"]')
    hatches = hatches.drop(['attempts'], axis=1)
    pivot_hatch = hatches.pivot(
        index='match', columns='task', values='successes').fillna(0)
    bhtasks = ['csHatch', 'getHatch', 'rocketHatch1', 'rocketHatch2',
               'rocketHatch3']
    _addcol(pivot_hatch, bhtasks)
    cds_hatches = bmodels.ColumnDataSource(pivot_hatch)
    htasks = cds_hatches.column_names[1:]
    matches = cds_hatches.data['match']

    cargo = data.query('task == ["getCargo", "csCargo", "rocketCargo1",'
                       '"rocketCargo2", "rocketCargo3"]')
    cargo = cargo.drop(['attempts'], axis=1)
    pivot_cargo = cargo.pivot(
        index='match', columns='task', values='successes').fillna(0)
    bctasks = ['csCargo', 'getCargo', 'rocketCargo1',
               'rocketCargo2', 'rocketCargo3']
    _addcol(pivot_hatch, bctasks)
    cds_cargo = bmodels.ColumnDataSource(pivot_cargo)
    ctasks = cds_cargo.column_names[1:]

    t1plot = plt.figure(x_range=matches, title="One Team Graph: " + team,
                        plot_height=350, plot_width=700)

    t1plot.vbar_stack(htasks,
                      x=btransform.dodge('match', -.17, range=t1plot.x_range),
                      width=0.3, source=cds_hatches,
                      color=bpalettes.BuPu5,
                      legend=[" " + x for x in htasks])
    t1plot.vbar_stack(ctasks,
                      x=btransform.dodge('match', .17, range=t1plot.x_range),
                      width=0.3, source=cds_cargo,
                      color=bpalettes.Oranges5,
                      legend=[" " + x for x in ctasks])
    return t1plot


def _onet_d(team, conn):
    sql = '''
        SELECT match, task, successes, attempts FROM vw_measures 
        WHERE team IN (SELECT team FROM schedules
                     INNER JOIN status ON schedules.event_id=status.event_id 
                     WHERE schedules.event_id=status.event_id AND schedules.team=%s)

    '''
    raw_data = pd.read_sql(sql, conn, params=[team])
    return raw_data


def _addcol(df, colnames):
    for colname in colnames:
        if colname not in df:
            df[colname] = 0


def pages_1t(team):
    bokeh.io.output_file('oneteam.html')
    graph = onet_g(team)
    title = 'One Team Display: Match ' + team
    bokeh.io.save(graph, title=title)

