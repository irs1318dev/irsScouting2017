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
	return  [ x[0] for x in col if x[2] > 0 ]


#Holoviews generation
def hv_table(data, label='Successes'):
	return hv.Table(data, "Team", ['Task', label])


def hv_stack(data, label='', style=dict(), side='Successes', width=400, height=400):
	return hv.Bars(data, ["Team", "Task"], side, label=label).opts(plot=dict(tools=['hover'], stack_index=1, legend_position="top", xrotation=45, width=width, height=height), style=style)


def hv_bar(data, label='', style=dict(), side='Successes', width=400, height=400):
	return hv.Bars(data, ["Team", "Task"], side, label=label).opts(plot=dict(tools=['hover'], legend_position="top", xrotation=45, width=width, height=height), style=style)

def hv_box(data, label='', style=dict(), side='Successes', width=400, height=400):
	return hv.BoxWhisker(data, ["Team", "Task"], side, label=label).opts(plot=dict(tools=['hover'], legend_position="top", xrotation=45, width=width, height=height), style=style)


def save_view(view, name):
	renderer = hv.renderer('bokeh')
	# Convert to bokeh figure then save using bokeh
	plot = renderer.get_plot(view).state

	from bokeh.io import output_file, save, show
	output_file(config.web_data(name + '.html'), mode='inline')
	save(plot, title=name)


def graph_match(match_list):
	df_rnk = get_dataframe()

	tasks = ['placeSwitch', 'placeExchange', 'placeScale']
	data = get_list(df_rnk, tasks)
	red_place_plot = hv_bar(filter_teams(data, match_list[:3]), 'Red Cubes Placed')
	blue_place_plot = hv_bar(filter_teams(data, match_list[3:]), 'Blue Cubes Placed')

	tasks = ['pickupPlatform', 'pickupCubeZone', 'pickupPortal', 'pickupExchange']
	team_sums = get_column(df_rnk, 'pickupFloor', 'teleop', 'sum_successes', task_rename='pickupTotal')
	pickup_max = get_column(df_rnk, 'pickupFloor', 'teleop', 'sum_successes')
	for location in tasks:
		data = get_column(df_rnk, location, 'teleop', 'sum_successes')
		for i in range(len(pickup_max)):
			if data[i][2] > pickup_max[i][2]:
				pickup_max[i] = data[i]
			team_sums[i][2] += data[i][2]

	for i in range(len(pickup_max)):
		if team_sums[i][2] != 0:
			pickup_max[i][2] = str(pickup_max[i][2] / team_sums[i][2] * 100) + '%'
		else:
			pickup_max[i][2] = '0%'

	red_get_plot = hv_table(filter_teams(pickup_max, match_list[:3]), 'Red Pickup')
	blue_get_plot = hv_table(filter_teams(pickup_max, match_list[3:]), 'Blue Pickup')

	tasks = ['makeClimb', 'getFoul', 'disabled']
	data = get_list(df_rnk, tasks, 'finish', 'sum_successes')
	red_extra = hv_table(filter_teams(data, match_list[:3]), 'Red Other')
	blue_extra = hv_table(filter_teams(data, match_list[3:]), 'Blue Other')

	plot = hv.Layout(red_place_plot + blue_place_plot + red_get_plot + blue_get_plot + red_extra + blue_extra).cols(2)
	save_view(plot, 'matchData')


def graph_event():
	df_rnk = get_dataframe()

	tasks = ['placeSwitch', 'placeExchange', 'placeScale']
	data = get_list(df_rnk, tasks)
	place_plot = hv_stack(filter_teams(data), 'Cubes Placed', width=1000)

	success = get_column(df_rnk, 'makeClimb', 'finish', 'sum_successes')
	attempt = get_column(df_rnk, 'makeClimb', 'finish', 'sum_attempts', task_rename='attemptClimb')
	climbs = hv_bar(filter_teams(combine_tasks([success, attempt]), sorted_teams(success)), 'Climbs', width=1000)

	success = get_column(df_rnk, 'disabled', 'finish', 'sum_successes')
	attempt = get_column(df_rnk, 'disabled', 'finish', 'sum_attempts', task_rename='temporary')
	fouls = hv_bar(filter_teams(combine_tasks([success, attempt]), sorted_teams(success)), 'Problems', width=1000)

	plot = hv.Layout(place_plot + climbs + fouls).cols(1)
	save_view(plot, 'eventData')
