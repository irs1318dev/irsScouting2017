import os
import os.path

import bokeh.models as bmodels
import bokeh.plotting as plt
import bokeh.palettes as bpalettes
import bokeh.models.widgets as bmw
import bokeh.layouts as blt
import bokeh.io

import server.season.s2019.view.rankingtable as rt
import server.model.event as sme
import server.config as sc
import server.view.bokeh


def point_chart():
    try:
        df_temp = rt.ranking_df()
        df_new = df_temp.filter(['avgHatchPoints', 'avgCargoPoints', 'avgClimbPoints', 'avgHabPoints'], axis=1)
        points_cds = bmodels.ColumnDataSource(df_new)
        task = points_cds.column_names[1:]
        tooltips = [
            ("", "team: @index"),
            ("", "$name: @$name")
        ]
        p = plt.figure(title='Points Chart', x_range=points_cds.data['index'],
                       plot_width=1100, plot_height=350, tooltips=tooltips, toolbar_location="above")
        hr = p.vbar_stack(task, x='index', width=0.4,
                          source=points_cds, color=bpalettes.RdBu4)
        legend = bokeh.models.Legend(items=[(x, [hr[task.index(x)]]) for x in task], location=(0, 0))
        p.add_layout(legend, 'right')
        p.xaxis.major_label_orientation = 3.14 / 4
        return p
    except Exception as err:
        raise err
        return(bmw.Div(text=str(err)))
        # print(err)
        # print("The points chart has fallen and cannot get up!")


def pages_pointschart():
    match = sme.EventDal.get_current_match()
    os.chdir(sc.output_path())
    chart = point_chart()
    div1 = blt.WidgetBox(bmw.Div(text='<a href="index.html">Home Page</a>'))
    div2 = blt.WidgetBox(bmw.Div(text='<h1>Points Chart</h1>' +
                                     'updated at match:' + match))
    bokeh.io.output_file('pointschart.html')
    col = blt.column([div1, div2, chart])
    title = 'Ranking Table: Match ' + match
    # LocalResource needed to load JS and CSS files from local folder
    res = server.view.bokeh.LocalResource(
        os.path.join(sc.output_path(), 'static'))
    bokeh.io.save(col, title=title, resources=res)
