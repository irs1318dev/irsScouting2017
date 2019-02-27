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


def oneteam_climb_df(team):
    conn = smc.pool.getconn()
    sql = '''
            SELECT match, COUNT(CASE WHEN capability='1' THEN 1 END) AS Climb1,
            COUNT(CASE WHEN capability='2' THEN 1 END) AS Climb2,
            COUNT(CASE WHEN capability='3' THEN 1 END) AS Climb3
            FROM vw_measures WHERE task='climb' AND team=%s
            GROUP BY match;

        '''
    raw_data_climb = pd.read_sql(sql, conn, params=[team])
    smc.pool.putconn(conn)
    return raw_data_climb


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


def shape_climb_data(team):
    # make match the index
    climb_data = oneteam_climb_df(team)
    df_cl = climb_data.set_index(['match'])
    cl_cds = bokeh.models.ColumnDataSource(df_cl)
    return cl_cds


def oneteam_plot(team, num_matches=12):
    measures = oneteam_df(team)
    matches = measures.match.unique()

    t1plot = plt.figure(x_range=matches, title="One Team Graph: " + team,
                        plot_height=350, plot_width=800,
                        toolbar_location='left',  tools="hover",
                        tooltips="$name: @$name")

    # Hatch panels
    hatch_tasks = ['getHatch', 'csHatch', 'rocketHatch1', 'rocketHatch2',
                   'rocketHatch3']
    hcds_all = get_cds_averages(measures, hatch_tasks)
    hatch_r = t1plot.vbar_stack(hatch_tasks,
                      x=btransform.dodge('match', -.14, range=t1plot.x_range),
                      width=0.25, source=hcds_all,
                      color=bpalettes.BuPu5)

    # Cargo
    cargo_tasks = ['getCargo', 'csCargo', 'rocketCargo1',
                             'rocketCargo2', 'rocketCargo3']
    ccds_all = get_cds_averages(measures, cargo_tasks)
    cargo_r = t1plot.vbar_stack(cargo_tasks,
                      x=btransform.dodge('match', .14, range=t1plot.x_range),
                      width=0.25, source=ccds_all,
                      color=bpalettes.Oranges5)

    # Climb
    climb_tasks = ['climb1', 'climb2', 'climb3']
    cl_cds = shape_climb_data(team)
    climb_r = t1plot.vbar_stack(climb_tasks,
                      x=btransform.dodge('match', .41, range=t1plot.x_range),
                      width=0.25, source=cl_cds,
                      color=bpalettes.Viridis3)

    hatch_items = [(x, [hatch_r[hatch_tasks.index(x)]]) for x in hatch_tasks]
    cargo_items = [(x, [cargo_r[cargo_tasks.index(x)]]) for x in cargo_tasks]
    climb_items = [(x, [climb_r[climb_tasks.index(x)]]) for x in climb_tasks]
    legend = bmodels.Legend(items=hatch_items + cargo_items + climb_items,
                            location=(0, 0))

    t1plot.add_layout(legend, 'right')
    return t1plot


def pages_1t(teams):
    os.chdir(server.config.output_path('2019') + r'/oneteam')

    for team in teams:
        bokeh.io.output_file('1t{0}.html'.format(team))
        graph = oneteam_plot(team)
        title = 'One Team Display: Match ' + team
        bokeh.io.save(graph, title=title)

