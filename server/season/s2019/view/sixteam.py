import os
import os.path

import pandas as pd
import bokeh.models as bmodels
import bokeh.plotting as plt
import bokeh.palettes as bpalettes
import bokeh.transform as btransform
import bokeh.models.widgets as bmw
import bokeh.io
import bokeh.layouts as blt

import server.model.connection as smc
import server.config as sc
import server.model.event as sme
import server.view.bokeh


def cds_new_6t(alliance, match, meas, sched, tasks, num_m, num_matches=12):
    teams = sched.query('match=="{}" & alliance=="{}"'.format(match, alliance))['team']
    dfm_6t = meas[meas.team.isin(teams)]
    dfm_nm = dfm_6t.query('last_match <= {}'.format(num_matches)).copy(deep=True)
    dfm_nm['num_matches'] = dfm_nm.last_match.max()
    df_task = dfm_nm[dfm_nm.task.isin(tasks)][
        ['team', 'task', 'successes', "num_matches"]]
    for team in teams:
        for task in tasks:
            if df_task.query('team=="{}" & task=="{}"'.format(team, task)).shape[0] == 0:
                n = num_m.query('team=="{}"'.format(team)).iat[0, 1]
                new_row = pd.DataFrame({'team': [team], 'task': [task], 'successes': [0], 'num_matches': [n]})
                # df_task.iloc[df_task.shape[0]+1, :] = [team, tasks[0], 0, n]
                df_task = df_task.append(new_row)
                print(df_task)
        # if team not in df_task.team:
        #     n = num_m.query('team=="{}"'.format(team)).iat[0, 1]
        #     df_task = df_task.append([team, tasks[0], 0, n])
    # for task in tasks:
    #     if task not in df_task.task:
    #         for team in teams:
    #             n = num_m.query('team=="{}"'.format(team)).iat[0, 1]
    #             # df_task.iloc[-1, :] = [team, task, 0, n]
    #             df_task = df_task.append([team, task, 0, n])
    #             print()
    #             # print("Adding Task:===", team, task, 0, n)
    df_sum = df_task.groupby(['task', 'team']).agg({'successes': 'sum', 'num_matches': 'max'})
    df_sum['avg_successes'] = df_sum.successes / df_sum.num_matches
    df_unstack = df_sum.unstack().loc[:, 'avg_successes']
    df_f = df_unstack.fillna(0)
    df_f.loc['Total', :] = list(df_f.sum())
    return bmodels.ColumnDataSource(df_f)


def get_df_6t():
    conn = smc.pool.getconn()
    sql = '''
            SELECT * FROM vw_measures;

        '''
    dfm = pd.read_sql(sql, conn)
    sql2 = '''
        SELECT schedules.* FROM schedules
                 INNER JOIN status ON schedules.event_id=status.event_id 
                 WHERE schedules.event_id=status.event_id;
    '''
    df_sched = pd.read_sql(sql2, conn)
    sql3 = '''
        SELECT * FROM vw_num_matches;
    '''
    df_num_matches = pd.read_sql(sql3, conn)
    smc.pool.putconn(conn)
    return dfm, df_sched, df_num_matches



# def plot_6t(match):
#
#     h_tasks = ['csHatch', 'rocketHatch1',
#                'rocketHatch2', 'rocketHatch3']
#     c_tasks = ['csCargo', 'rocketCargo1',
#                 'rocketCargo2', 'rocketCargo3']
#     meas, sched = get_df_6t()
#     cds_rh = cds_new_6t("red", match, meas, sched, h_tasks)
#     return cds_rh


def hatches_6t(match, num_matches=12):
    # conn = smc.pool.getconn()
    hatches = ['csHatch', 'rocketHatch1',
               'rocketHatch2', 'rocketHatch3']
    meas, sched, num_m = get_df_6t()
    cdsr = cds_new_6t("red", match, meas, sched, hatches, num_m, num_matches)
    cdsb = cds_new_6t("blue", match, meas, sched, hatches, num_m, num_matches)
    rteams = cdsr.column_names[1:]
    bteams = cdsb.column_names[1:]

    hatch_cols = ['Total', 'csHatch', 'rocketHatch1',
               'rocketHatch2', 'rocketHatch3']

    plt_hatches = plt.figure(title='Six Team Hatches Placed: Match ' + match, x_range=hatch_cols,
                             plot_width=700, plot_height=300)

    plt_hatches.vbar_stack(rteams, x=btransform.dodge('task', -0.17, range=plt_hatches.x_range), width=0.3,
                           source=cdsr,
                           color=bpalettes.Reds3, legend=[" " + x for x in rteams])
    plt_hatches.vbar_stack(bteams, x=btransform.dodge('task', 0.17, range=plt_hatches.x_range), width=0.3,
                           source=cdsb,
                           color=bpalettes.Blues3, legend=[" " + x for x in bteams])
    # smc.pool.putconn(conn)
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
    # conn = smc.pool.getconn()
    # cdsr = _cargo_6t_cds(match, num_matches, 'red', conn)
    # cdsb = _cargo_6t_cds(match, num_matches, 'blue', conn)
    meas, sched, num_m = get_df_6t()
    cargo = ['csCargo', 'rocketCargo1',
             'rocketCargo2', 'rocketCargo3']
    cdsr = cds_new_6t("red", match, meas, sched, cargo, num_m, num_matches)
    cdsb = cds_new_6t("blue", match, meas, sched, cargo, num_m, num_matches)
    rteams = cdsr.column_names[1:]
    bteams = cdsb.column_names[1:]

    cargo_cols = ['Total', 'csCargo', 'rocketCargo1',
             'rocketCargo2', 'rocketCargo3']

    plt_cargo = plt.figure(title='Six Team Cargo Placed: Match ' + match, x_range=cargo_cols,
                           plot_width=700, plot_height=300)

    plt_cargo.vbar_stack(rteams, x=btransform.dodge('task', -0.17, range=plt_cargo.x_range), width=0.3, source=cdsr,
                         color=bpalettes.Reds3, legend=[" " + x for x in rteams])
    plt_cargo.vbar_stack(bteams, x=btransform.dodge('task', 0.17, range=plt_cargo.x_range), width=0.3, source=cdsb,
                         color=bpalettes.Blues3, legend=[" " + x for x in bteams])
    # smc.pool.putconn(conn)

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


def pages_6t(matches, num_matches=12):
    os.chdir(os.path.join(sc.output_path('2019'), 'sixteam'))
    for match in matches:
        bokeh.io.output_file('6t' + match + '.html')
        div_top = bmw.Div(text='''
            <H1>Match {} Six Team Chart</H1>
        '''.format(match))
        div_all = bmw.Div(text='<h3>All Matches</h3>')
        row_all = blt.row(hatches_6t(match, num_matches), cargo_6t(match, num_matches))
        div_l3 = bmw.Div(text='<h3>Last 3 Matches</h3>')
        row_l3 = blt.row(hatches_6t(match, 3), cargo_6t(match, 3))

        col = blt.Column(div_top, div_all, row_all, div_l3, row_l3)
        title = 'Six Team Display: Match ' + match
        # LocalResource needed to load JS and CSS files from local folder
        res = server.view.bokeh.LocalResource(
            os.path.join(sc.output_path('2019'), 'static'))
        bokeh.io.save(col, title=title, resources=res)


def next3(team):
    current = sme.EventDal.get_current_match()
    team_sched = sme.EventDal.team_match(team)
    pages_6t([x for x in team_sched if x > current][:3])


def index_page():
    sixteam_folder = os.path.join(sc.output_path('2019'), 'sixteam')
    last_match = sme.EventDal.get_previous_match()
    file_names = os.listdir(sixteam_folder)
    file_data = [(f_name, 'Match {}'.format(f_name[2:-5])) for f_name in file_names if f_name[-5:] == '.html']
    links = ['<li><a href="sixteam/{}">{}</a></li>'.format(f_data[0], f_data[1]) for f_data in file_data]

    html = '<html><head><link rel="stylesheet" href="list-nav.css"><title>IRS Scouting Data</title></head>'
    html = html + '''<ul id="list-nav">
	<li><a href="./index.html">Six Team</a></li>
	<li><a href="./pointschart.html">Points Chart</a></li>
	<li><a href="./rankingtable.html">Ranking Table</a></li>
	<li><a href="./oneteam_index.html">One Team</a></li>
</ul><body><br><br><h1>IRS Scouting Data</h1>h2>Updated at match: ''' +\
                   sme.EventDal.get_previous_match() + '</h2><ul>'

    html = html + ''.join(links)
    html = html + '</ul><h3>One team charts</h3><a href="oneteam_index.html">Oneteam charts</a>'
    html = html + '</ul><h3>Ranking Table</h3><a href="rankingtable.html">Ranking Table</a>'
    html = html + '<h3>Points Chart</h3><a href="pointschart.html">Points Chart</a></body></html>'
    os.chdir(sc.output_path('2019'))
    index_file = open("index.html", "w")
    index_file.write(html)
    index_file.close()
    return html
