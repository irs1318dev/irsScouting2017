import pandas as pd
import os
import os.path

import bokeh.models as bmodels
import bokeh.models.widgets as bmw
import bokeh.layouts as blt
import bokeh.io

import server.model.connection as smc
import server.model.event as sme
import server.config as sc
import server.view.bokeh


def ranking_df():
    conn = smc.pool.getconn()
    sql = '''
        SELECT team, task, SUM(successes) AS successes FROM vw_measures 
        GROUP BY team, task;
    '''
    df_temp = pd.read_sql(sql, conn)
    df_temp = df_temp.set_index(['task', 'team'])
    df_temp = df_temp.unstack()
    df_temp.columns = df_temp.columns.droplevel()
    df_temp = df_temp.fillna(0)
    df_temp = df_temp.T
    taskList = ['pickSide', 'startItem', 'crossHabLine', 'crossCenterLine',
                'collision', 'getHatch', 'frontBay', 'closeHatch', 'centerHatch',
                'farHatch', 'rocketHatch', 'dropHatchs', 'getCargo', 'closeCargo',
                'centerCargo', 'farCargo', 'rocketCargo', 'dropCargos',
                'pickupLoadingHatch', 'groundHatchPickup', 'pickupLoadingCargo',
                'groundCargoPickup', 'csHatch', 'csCargo', 'dropHatch', 'dropCargo',
                'rocketHatch1', 'rocketHatch2', 'rocketHatch3', 'rocketCargo1',
                'rocketCargo2', 'rocketCargo3', 'pickupLoadingHatch', 'groundHatchPickup',
                'pickupLoadingCargo', 'groundCargoPickup', 'climb', 'supportClimb',
                'disabled', 'temp', 'fellOver', 'stuckOnPlat', 'duration']
    addcol(df_temp, taskList)
    sql = '''
        SELECT team, matches FROM vw_num_matches 
        GROUP BY team, matches;
    '''
    df_num_matches = pd.read_sql(sql, conn)
    df_all_cols = pd.merge(df_temp, df_num_matches, how='inner', on='team')
    df_all = df_all_cols.set_index('team')
    sql = '''
        SELECT team, COUNT(CASE WHEN capability='1' THEN 1 END) AS Climb1,
        COUNT(CASE WHEN capability='2' THEN 1 END) AS Climb2,
        COUNT(CASE WHEN capability='3' THEN 1 END) AS Climb3
        FROM vw_measures WHERE task='climb'
        GROUP BY team;
    '''
    df_climb = pd.read_sql(sql, conn)
    df_climb = df_climb.set_index('team')
    df_all = pd.concat([df_all, df_climb], axis=1, sort=False)
    df_all = df_all.fillna(0)
    sql = '''
        SELECT team, match FROM vw_measures WHERE task='crossHabLine';
    '''
    df_habMatch = pd.read_sql(sql, conn)
    sql = '''
        SELECT team, match, COUNT(CASE WHEN capability='Side' THEN 1 END) AS sideHab,
        COUNT(CASE WHEN capability='Center' THEN 1 END) AS centerHab,
        COUNT(CASE WHEN capability='LV.2' THEN 1 END) AS level2Hab
        FROM vw_measures WHERE task='pickSide'
        GROUP BY team, match;
    '''
    df_teamSide = pd.read_sql(sql, conn)
    df_fun = pd.merge(df_habMatch, df_teamSide, how='inner', on='team')
    df_fun2 = df_fun.loc[df_fun['match_x'] == df_fun['match_y']]
    df_fun2 = df_fun2.drop(['match_x', 'match_y'], axis=1)
    df_fun2 = df_fun2.groupby('team').sum()
    df_all = pd.concat([df_all, df_fun2], axis=1, sort=False)
    df_all = df_all.fillna(0)
    df_all['team'] = df_all.index
    df_all['totalCargo'] = (df_all['getCargo'] + df_all['rocketCargo1'] + df_all['rocketCargo'] +
                            df_all['rocketCargo2'] + df_all['rocketCargo3'] + df_all['csCargo'])
    df_all['totalHatch'] = (df_all['getHatch'] + df_all['rocketHatch1'] + df_all['rocketHatch1'] +
                            df_all['rocketHatch2'] + df_all['rocketHatch3'] + df_all['csHatch'])
    df_all['avgCargo'] = df_all['totalCargo'] / df_all['matches']
    df_all['avgHatch'] = df_all['totalHatch'] / df_all['matches']
    df_all['avgCargoPoints'] = df_all['avgCargo'] * 3
    df_all['avgHatchPoints'] = df_all['avgHatch'] * 2
    df_all['climb1Points'] = df_all['climb1'] * 3
    df_all['climb2Points'] = df_all['climb2'] * 6
    df_all['climb3Points'] = df_all['climb3'] * 12
    df_all['avgClimbPoints'] = (df_all['climb3Points'] + df_all['climb2Points'] +
                                df_all['climb1Points']) / df_all['matches']
    df_all['habPoints'] = ((df_all['centerhab'] + df_all['sidehab']) * 3) + (df_all['level2hab'] * 6)
    df_all['avgHabPoints'] = df_all['habPoints'] / df_all['matches']
    df_all['avgPoints'] = (df_all['avgCargoPoints'] + df_all['avgHatchPoints'] +
                           df_all['avgClimbPoints'] + df_all['avgHabPoints'])
    df_all['level1hab'] = (df_all['sidehab'] + df_all['centerhab'])
    df_all['dontMove'] = (df_all['matches'] - (df_all['level1hab'] + df_all['level2hab']))
    df_all['Defense'] = df_all['duration'] / df_all['matches']

    smc.pool.putconn(conn)
    return df_all


def ranking_general(df_all):
    try:
        Rank_cds = bmodels.ColumnDataSource(df_all)
        fixed2 = bmw.NumberFormatter(format='0.00')
        cols = [
            bmw.TableColumn(field='team', title='Team'),
            bmw.TableColumn(field='avgCargo', title='Average Cargo', formatter=fixed2),
            bmw.TableColumn(field='avgHatch', title='Average Hatches', formatter=fixed2),
            bmw.TableColumn(field='avgHatchPoints', title='Hatch Points', formatter=fixed2),
            bmw.TableColumn(field='avgCargoPoints', title='Cargo Points', formatter=fixed2),
            bmw.TableColumn(field='avgPoints', title='Average Points', formatter=fixed2),
            bmw.TableColumn(field='climb1', title='Total Lvl1 Climbs', formatter=fixed2),
            bmw.TableColumn(field='climb2', title='Total Lvl2 Climbs', formatter=fixed2),
            bmw.TableColumn(field='climb3', title='Total Lvl3 Climbs', formatter=fixed2),
            bmw.TableColumn(field='Defense', title='Avg Defense', formatter=fixed2),
        ]
        data_table = bmw.DataTable(source=Rank_cds, columns=cols, width=900, height=380)
    except:
        return bmw.Div(text="Error with general ranking table")
    return data_table


def ranking_auto(df_all):
    try:
        Rank_cds = bmodels.ColumnDataSource(df_all)
        fixed2 = bmw.NumberFormatter(format='0.00')
        cols = [
            bmw.TableColumn(field='team', title='Team'),
            bmw.TableColumn(field='level2hab', title='Move lvl2', formatter=fixed2),
            bmw.TableColumn(field='level1hab', title='Move lvl1', formatter=fixed2),
            bmw.TableColumn(field='dontMove', title='Don\'t Move', formatter=fixed2),
            bmw.TableColumn(field='rocketHatch', title='Rocket Hatch', formatter=fixed2),
            bmw.TableColumn(field='frontBay', title='CS Front Hatch', formatter=fixed2),
            bmw.TableColumn(field='closeHatch', title='CS Close Hatch', formatter=fixed2),
            bmw.TableColumn(field='centerHatch', title='CS Center Hatch', formatter=fixed2),
            bmw.TableColumn(field='farHatch', title='CS Far Hatch', formatter=fixed2),
        ]
        data_table = bmw.DataTable(source=Rank_cds, columns=cols, width=900, height=380)
    except:
        return bmw.Div(text="Error with auto ranking table")
    return data_table


def pages_rankingtable():
    df_all = ranking_df()
    autoTable = ranking_auto(df_all)
    generalTable = ranking_general(df_all)
    match = sme.EventDal.get_current_match()
    tab1 = bmw.Panel(child=generalTable, title='General Table')
    tab2 = bmw.Panel(child=autoTable, title='Auto Table')
    tabs = bmw.Tabs(tabs=[tab1, tab2])
    div1 = blt.WidgetBox(bmw.Div(text='<a href="index.html">Home Page</a>'))
    div2 = blt.WidgetBox(bmw.Div(text='<h1>Ranking Table</h1>' +
                                      'updated at match:' + match))
    os.chdir(sc.output_path('2019'))
    bokeh.io.output_file('rankingtable.html')
    col = blt.column([div1, div2, tabs])
    title = 'Ranking Table: Match ' + match
    # LocalResource needed to load JS and CSS files from local folder
    res = server.view.bokeh.LocalResource(
        os.path.join(sc.output_path('2019'), 'static'))
    bokeh.io.save(col, title=title, resources=res)


def addcol(df, colnames):
    for colname in colnames:
        if colname not in df:
            df[colname] = 0