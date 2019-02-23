import pandas as pd
import bokeh.models as bmodels
import bokeh.plotting as plt
import bokeh.palettes as bpalettes
import bokeh.transform as btransform
import bokeh.io
import bokeh.layouts as blt
import server.config as sc
import os

import server.model.connection as smc
import server.model.version as smv
import server.model.event as sme


def hatches_6t(match, num_matches=12):
    conn = smc.pool.getconn()
    cdsr = _hatches_6t_cds(match, num_matches, 'red', conn)
    cdsb = _hatches_6t_cds(match, num_matches, 'blue', conn)
    rteams = cdsr.column_names[1:]
    bteams = cdsb.column_names[1:]

    hatches = ['Total Hatches', 'csHatch', 'rocketHatch1',
               'rocketHatch2', 'rocketHatch3']
    plt_hatches = plt.figure(title='Six Team Hatches Placed: Match ' + match, x_range=hatches,
                             plot_width=700, plot_height=300)

    plt_hatches.vbar_stack(rteams, x=btransform.dodge('task', -0.17, range=plt_hatches.x_range), width=0.3,
                           source=cdsr,
                           color=bpalettes.Reds3, legend=[" " + x for x in rteams])
    plt_hatches.vbar_stack(bteams, x=btransform.dodge('task', 0.17, range=plt_hatches.x_range), width=0.3,
                           source=cdsb,
                           color=bpalettes.Blues3, legend=[" " + x for x in bteams])
    smc.pool.putconn(conn)
    return plt_hatches


def _hatches_6t_cds(match, num_matches, alliance, conn):

    sql = '''
        SELECT team, task, SUM(successes) AS hatches_placed FROM vw_measures 
        WHERE task IN ('rocketHatch1', 'rocketHatch2', 'rocketHatch3', 'csHatch')
        AND team IN (SELECT team FROM schedules
                     INNER JOIN status ON schedules.event_id=status.event_id 
                     WHERE schedules.event_id=status.event_id AND schedules.match=%s
                     AND alliance=%s)
        AND last_match <= %s
        GROUP BY team, task;
    '''
    dfh = pd.read_sql(sql, conn, params=[match, alliance, num_matches])
    dfh = dfh.set_index(['task', 'team'])
    dfh = dfh.unstack()
    dfh.columns = dfh.columns.droplevel()
    dfh = dfh.fillna(0)
    dfh.loc['Total Hatches', :] = list(dfh.sum())
    return bmodels.ColumnDataSource(dfh)


def cargo_6t(match, num_matches=12):
    conn = smc.pool.getconn()
    cdsr = _cargo_6t_cds(match, num_matches, 'red', conn)
    cdsb = _cargo_6t_cds(match, num_matches, 'blue', conn)
    rteams = cdsr.column_names[1:]
    bteams = cdsb.column_names[1:]

    cargo = ['Total Cargo', 'csCargo', 'rocketCargo1',
             'rocketCargo2', 'rocketCargo3']

    plt_cargo = plt.figure(title='Six Team Cargo Placed: Match ' + match, x_range=cargo,
                           plot_width=700, plot_height=300)

    plt_cargo.vbar_stack(rteams, x=btransform.dodge('task', -0.17, range=plt_cargo.x_range), width=0.3, source=cdsr,
                         color=bpalettes.Reds3, legend=[" " + x for x in rteams])
    plt_cargo.vbar_stack(bteams, x=btransform.dodge('task', 0.17, range=plt_cargo.x_range), width=0.3, source=cdsb,
                         color=bpalettes.Blues3, legend=[" " + x for x in bteams])
    smc.pool.putconn(conn)

    return plt_cargo


def _cargo_6t_cds(match, num_matches, alliance, conn):
    sql = '''
        SELECT team, task, SUM(successes) AS cargo_placed FROM vw_measures 
        WHERE task IN ('rocketCargo1', 'rocketCargo2', 'rocketCargo3', 'csCargo')
        AND team IN (SELECT team FROM schedules
                     INNER JOIN status ON schedules.event_id=status.event_id 
                     WHERE schedules.event_id=status.event_id AND schedules.match=%s
                     AND alliance=%s)
        AND last_match <= %s
        GROUP BY team, task;
    '''
    dfc = pd.read_sql(sql, conn, params=[match, alliance, num_matches])
    dfc = dfc.set_index(['task', 'team'])
    dfc = dfc.unstack()
    dfc.columns = dfc.columns.droplevel()
    dfc = dfc.fillna(0)
    dfc.loc['Total Cargo', :] = list(dfc.sum())
    return bmodels.ColumnDataSource(dfc)


def pages_6t(match, num_matches=12):
    os.chdir(sc.output_path('2019') + r'\sixteam')
    bokeh.io.output_file('sixteam' + match[0:3] + 'q.html')
    row = blt.row(hatches_6t(match, num_matches), cargo_6t(match, num_matches))
    title = 'Six Team Display: Match ' + match
    bokeh.io.save(row, title=title)

