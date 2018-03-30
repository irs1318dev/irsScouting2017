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


def save_view(view, name):
	renderer = hv.renderer('bokeh')
	# Convert to bokeh figure then save using bokeh
	plot = renderer.get_plot(view).state

	from bokeh.io import output_file, save
	output_file(config.web_data(name + '.html'), mode='inline')
	save(plot, title=name)

def save_image(view, name):
	renderer = hv.renderer('bokeh')
	# Convert to bokeh figure then save using bokeh
	plot = renderer.get_plot(view).state

	from bokeh.io import export_png
	export_png(plot, filename=config.web_data(name + '.png'))


def graph_match(match_list):
	df_rnk = get_dataframe()

	tasks = ['placeSwitch', 'placeExchange', 'placeScale']
	data = get_list(df_rnk, tasks)
	place_plot = hv_bar(split_alliances(data, match_list), 'Cubes Placed')

	tasks = ['pickupPlatform', 'pickupCubeZone', 'pickupPortal', 'pickupExchange']
	team_sums = get_column(df_rnk, 'pickupFloor', 'teleop', 'sum_successes', task_rename='pickupTotal')
	pickup_max = get_column(df_rnk, 'pickupFloor', 'teleop', 'sum_successes')

	for location in tasks:
		data = get_column(df_rnk, location, 'teleop', 'sum_successes')
		for i in range(len(data)):
			if data[i][2] > pickup_max[i][2]:
				pickup_max[i] = data[i]
			team_sums[i][2] += data[i][2]

	for i in range(len(pickup_max)):
		if team_sums[i][2] != 0:
			pickup_max[i][2] = str(round(pickup_max[i][2] / team_sums[i][2] * 100)) + '%'
		else:
			pickup_max[i][2] = '0%'

	get_plot = hv_table(split_alliances(pickup_max, match_list), 'Pickup')

	tasks = ['autoLine', 'placeSwitch', 'placeScale']
	data = get_list(df_rnk, tasks, 'auto')
	auto_plot = hv_stack(split_alliances(data, match_list), 'Auto')

	tasks = ['placeIncorrect', 'crossNull']
	data = get_list(df_rnk, tasks, 'auto', 'sum_successes')
	drop_plot = hv_table(split_alliances(data, match_list), 'Auto Fails')

	tasks = ['makeClimb', 'supportClimb', 'parkPlatform']
	data = get_list(df_rnk, tasks, 'finish')
	climb_plot = hv_stack(split_alliances(data, match_list), 'Climbing')

	tasks = ['disabled', 'getFoul']
	data = get_list(df_rnk, tasks, 'finish', 'sum_successes')
	fail_plot = hv_table(split_alliances(data, match_list), 'Total Problems')

	plot = hv.Layout(place_plot + get_plot + auto_plot + drop_plot + climb_plot + fail_plot).cols(2)
	save_view(plot, 'matchData')


def graph_event():
	df_rnk = get_dataframe()

	tasks = ['placeSwitch', 'placeScale', 'placeExchange']
	data = get_list(df_rnk, tasks)
	place_plot = hv_stack(filter_teams(data), 'Average Cubes Placed', width=1500)

	data = get_list(df_rnk, tasks, 'teleop', 'max_successes')
	exchange_plot = hv_stack(filter_teams(data), 'Max Cubes Placed', width=1500)

	plot = hv.Layout(place_plot + exchange_plot).cols(1)
	save_view(plot, 'eventData')

def graph_long_event():
	df_rnk = get_dataframe()

	tasks = ['placeSwitch', 'placeExchange', 'placeScale']
	data = get_list(df_rnk, tasks)
	place_plot = hv_stack(filter_teams(data), 'Cubes Placed', width=1500)

	success = get_column(df_rnk, 'makeClimb', 'finish', 'sum_successes')
	attempt = get_column(df_rnk, 'makeClimb', 'finish', 'sum_attempts', task_rename='attemptClimb')
	climb_plot = hv_bar(filter_teams(combine_tasks([success, attempt]), sorted_teams(success)), 'Climbs', width=1500)

	success = get_column(df_rnk, 'disabled', 'finish', 'sum_successes')
	attempt = get_column(df_rnk, 'disabled', 'finish', 'sum_attempts', task_rename='temporary')
	foul_plot = hv_bar(filter_teams(combine_tasks([success, attempt]), scoring_teams(attempt)), 'Problems', width=1500)

	tasks = ['autoLine', 'placeSwitch', 'placeScale']
	data = get_list(df_rnk, tasks, 'auto')
	auto_plot = hv_stack(filter_teams(data), 'Auto', width=1500)

	plot = hv.Layout(place_plot + auto_plot + climb_plot + foul_plot).cols(1)
	save_view(plot, 'longEventData')
