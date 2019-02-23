import os

import pandas as pd
import bokeh.plotting
import bokeh.models as bmodels
import bokeh.plotting as plt
import bokeh.palettes as bpalettes
import bokeh.transform as btransform
import bokeh.io

import server.model.connection as smc
import server.config


def oneteam_df(team):
    conn = smc.pool.getconn()
    sql = '''
        SELECT match, task, successes, attempts, last_match
            FROM vw_measures
            WHERE team = %s;
    '''
    raw_data = pd.read_sql(sql, conn, params=[team])
    smc.pool.putconn(conn)
    return raw_data


def addcol(df, colnames):
    for colname in colnames:
        if colname not in df:
            df[colname] = 0
    return df


def get_cds_averages(measures, tasks, num_matches=12):
    # Filter to most recent matches and add num_matches column
    measures = measures[measures.last_match <= num_matches].copy(True)
    measures['num_matches'] = measures.last_match.max()

    # Eliminate unwanted tasks
    measures = measures[measures.task.isin(tasks)]

    # Calculate average successes
    measures['successes_avg'] = measures.successes / measures.num_matches

    # Convert tasks into columns and remove Nan
    pivot_df = measures.pivot(index='match', columns='task', values='successes')
    pivot_df.fillna(0, inplace=True)


    # Check for missing columns
    pivot_df = addcol(pivot_df, tasks)

    cds = bmodels.ColumnDataSource(pivot_df)
    return cds


def oneteam_plot(team, num_matches=12):
    measures = oneteam_df(team)
    matches = measures.match.unique()
    hatch_tasks = ['getHatch', 'csHatch', 'rocketHatch1', 'rocketHatch2',
               'rocketHatch3']
    cds_all = get_cds_averages(measures, hatch_tasks)

    t1plot = plt.figure(x_range=matches, title="One Team Graph: " + team,
                        plot_height=350, plot_width=700)


def onet_g(team, num_matches=12):


    data = _onet_d(team, conn)

    # Generate Hatches Data Source
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

    # Generate Cargo Data Source
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








def pages_1t(team):
    os.chdir(server.config.output_path('2019') + r'/oneteam')
    bokeh.io.output_file('oneteam.html')
    graph = onet_g(team)
    title = 'One Team Display: Match ' + team
    bokeh.io.save(graph, title=title)

