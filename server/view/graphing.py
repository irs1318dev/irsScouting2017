# This section is necessary for viewing plots.
import pandas as pd
import holoviews as hv
hv.extension('bokeh','matplotlib')
from sqlalchemy import text

import server.model.connection
import server.model.event as event
import server.model.dal as sm_dal
import server.config as config
import server.view.dataframes as sv_dataframes

engine = server.model.connection.engine
count_df = 	None

#Data collection
def get_dataframe():
	return sv_dataframes.ranking_df(12)


def get_teams():
	all_teams = list()
	sql = text("SELECT DISTINCT team FROM schedules WHERE "
			   "event_id = :event ORDER BY team;")

	conn = engine.connect()
	results = conn.execute(sql, event=event.EventDal.get_current_event()[0])
	conn.close()

	for row in results:
		all_teams.append(str(row).split('\'')[1])

	return all_teams


def _nan_to_zero(elmt):
    return 0 if pd.isnull(elmt) else elmt


#Data organizing
def get_column(df_rnk, task, phase='teleop', stat='avg_successes', actor='robot', task_rename=None):
	try:
		data = [_nan_to_zero(x) for x in df_rnk[phase][actor][task][stat]]
	except KeyError:
		print("ERROR: ", phase, actor, task, stat)
		return list()

	if task_rename is None:
		task_rename = task
	all_data = list()
	i = 0
	for team_num in df_rnk.index.values:
		all_data.append([team_num, task_rename, data[i]])
		i += 1

	return all_data


def combine_tasks(all_data_cols):
	combined_data = list()
	max_count = 0
	for col in all_data_cols:
		max_count = max(max_count, len(col))

	if len(all_data_cols) > 0:
		for i in range(max_count):
			for col in all_data_cols:
				if i < len(col):
					combined_data.append(col[i])
	return combined_data


def get_list(df_rnk, tasks, phase='teleop', stat='avg_successes', actor='robot'):
	all_data_cols = list()
	for task in tasks:
		all_data_cols.append(get_column(df_rnk, task, phase, stat, actor))
	return combine_tasks(all_data_cols)


def filter_teams(data, teams=None):
	filtered_data = list()

	if(teams is None):
		teams = get_teams()

	for team in teams:
		for row in data:
			if row[0] == team:
				filtered_data.append(row)

	return filtered_data


def sorted_teams(col, hide_zeros=True):
	if hide_zeros:
		col = filter_teams(col, scoring_teams(col))
	sorted_list = sorted(col, key=lambda x: x[2], reverse=True)
	return [ x[0] for x in sorted_list ]


def scoring_teams(col):
	teams = [ x[0] for x in col if x[2] > 0 ]
	return list(set(teams))


def math_tasks(col1, col2, operator='+', name=None):
	col1 = filter_teams(col1)
	col2 = filter_teams(col2)

	for i in range(len(col1)):
		if operator == '+':
			col1[i][2] += col2[i][2]
		if operator == '-':
			col1[i][2] -= col2[i][2]
		if operator == '/':
			col1[i][2] /= col2[i][2]
		if operator == '>':
			col1[i][2] = max(col1[i][2], col2[i][2])

		if name is not None:
			col1[i][1] = name
	return col1


def split_alliances(data, match_list):
	split_data = list()
	data = filter_teams(data, match_list)

	for row in data:
		if row[0] in match_list[:3]:
			row[0] = 'Red: ' + row[0]
			split_data.append(row)
		if row[0] in match_list[3:]:
			row[0] = 'Blue: ' + row[0]
			split_data.append(row)
	return split_data


#Holoviews generation
def hv_table(data, label='Successes'):
	return hv.Table(data, "Team", ['Task', label])


def hv_stack(data, label='', style=dict(), side='Successes', width=800, height=400):
	return hv.Bars(data, ["Team", "Task"], side, label=label).opts(plot=dict(tools=['hover'], stack_index=1, legend_position="top", xrotation=45, width=width, height=height), style=style)


def hv_bar(data, label='', style=dict(), side='Successes', width=800, height=400):
	return hv.Bars(data, ["Team", "Task"], side, label=label).opts(plot=dict(tools=['hover'], legend_position="top", xrotation=45, width=width, height=height), style=style)

def hv_box(data, label='', style=dict(), side='Successes', width=800, height=400):
	return hv.BoxWhisker(data, ["Team", "Task"], side, label=label).opts(plot=dict(tools=['hover'], legend_position="top", xrotation=45, width=width, height=height), style=style)


#Export plots through bokeh
def save_view(view, name):
	renderer = hv.renderer('bokeh')
	# Convert to bokeh figure then save using bokeh
	plot = renderer.get_plot(view).state

	from bokeh.io import output_file, save

	output_file(config.web_data(name + '.html'), mode='inline')
	save(plot, title=name)

def get_html(view, name):
	renderer = hv.renderer('bokeh')
	# Convert to bokeh figure then save using bokeh
	plot = renderer.get_plot(view).state

	from bokeh.embed import file_html
	from bokeh.resources import INLINE
	
	return file_html(plot, INLINE, name)
