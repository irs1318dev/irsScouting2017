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


def pages_6t(matches, num_matches=12):
    os.chdir(os.path.join(sc.output_path('2019'), 'sixteam'))
    for match in matches:
        bokeh.io.output_file('6t' + match + '.html')
        row = blt.row(hatches_6t(match, num_matches), cargo_6t(match, num_matches))
        div = bmw.Div(text='''
            <H1>Match {} Six Team Chart</H1>
        '''.format(match))
        col = blt.Column(div, row)
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
    file_names = os.listdir(sixteam_folder)
    file_data = [(f_name, 'Match {}'.format(f_name[2:-5])) for f_name in file_names if f_name[-5:] == '.html']
    links = ['<li><a href="sixteam/{}">{}</a></li>'.format(f_data[0], f_data[1]) for f_data in file_data]
    html = '<html><head><link rel="stylesheet" href="list-nav.css"><title>IRS Scouting Data</title></head>'
    html = html + '''<ul id="list-nav">
	<li><a href="./index.html">Six Team</a></li>
	<li><a href="./pointschart.html">Points Chart</a></li>
	<li><a href="./rankingtable.html">Ranking Table</a></li>
	<li><a href="./oneteam_index.html">One Team</a></li>
</ul><body><br><br><h1>IRS Scouting Data</h1><ul>
'''

    html = html + ''.join(links)
    html = html + '''
        </ul></body></html>
    '''
    os.chdir(sc.output_path('2019'))
    index_file = open("index.html", "w")
    index_file.write(html)
    index_file.close()
    return html
