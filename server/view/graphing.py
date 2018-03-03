# This section is necessary for viewing plots.
import holoviews as hv
hv.extension('bokeh','matplotlib')
from sqlalchemy import text

import server.model.connection
import server.model.event as event
import server.model.dal as sm_dal
import server.config as config
import server.view.dataframes as dataframes

engine = server.model.connection.engine
count_df = 	None

#Data collection
def get_data(tasks, phase='teleop', teams=None):
	teams_tasks_data = list()
	conn = engine.connect()
	event_id = event.EventDal.get_current_event()[0]
	phase_id = sm_dal.phase_ids[phase]

	count_df = dataframes.match_num_df()

	if(teams is None):
		teams = get_teams()

	for team in teams:
		if team != '':
			team_id = sm_dal.team_ids[team]
			team_data = list()

			for task in tasks:
				task_id = sm_dal.task_ids[task]

				sql = text("SELECT * FROM measures WHERE "
						   "event_id = :event_id "
						   "AND task_id = :task_id "
						   "AND team_id = :team_id "
						   "AND phase_id = :phase_id LIMIT 1000;")

				results = conn.execute(sql, event_id=event_id, task_id=task_id,
									   team_id=team_id, phase_id=phase_id).fetchall()

				for row in results:
					match = sm_dal.match_names[row['match_id']]
					attempts = row['attempts']
					successes = row['successes']
					capability = row['capability']

					team_data.append([team, task, match, successes, attempts, capability])

			teams_tasks_data.append(team_data)

	conn.close()
	return teams_tasks_data


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


def get_match_count(team):
	return count_df.query("team=='" + team + "'")["matches"]


#Process values
def average_tasks(data):
	fixed_data = list()
	for team_data in data:
		task = None
		current_data = ['na','na',0,0]
		team_fixed = list()
		count = get_match_count(team_data[0][0])

		for row in team_data:
			if row[1] == task:
				current_data[2] += row[3]
				current_data[3] += row[4]
			else:
				if task is not None:
					team_fixed.append([row[0], current_data[1], 'na', current_data[2] / count, current_data[3] / count, 'na'])

				current_data = [row[0], row[1], row[3], row[4]]
				task = row[1]

		team_fixed.append([current_data[0], current_data[1], 'na', current_data[2] / count, current_data[3] / count, 'na'])
		fixed_data.append(team_fixed)
	return fixed_data


def sum_tasks(data):
	fixed_data = list()
	for team_data in data:
		task = None
		current_data = list('na','na',0,0)
		team_fixed = list()

		for row in team_data:
			if row[1] == task:
				current_data[2] += row[3]
				current_data[3] += row[4]
			else:
				if task is not None:
					team_fixed.append([row[0], current_data[1], 'na', current_data[2], current_data[3], 'na'])

				current_data = [row[0], row[1], row[3], row[4]]
				task = row[1]

		team_fixed.append([current_data[0], current_data[1], 'na', current_data[2], current_data[3], 'na'])
		fixed_data.append(team_fixed)
	return fixed_data

def totals_team(data):
	total_data = list()
	for team_data in data:
		for row in team_data:
			found = False
			for task in total_data:
				if row[1] == task[1]:
					found = True
					task[3] += row[3]
					task[4] += row[4]
			if not found:
				total_data.append(['Total', row[1], 'na', row[3], row[4], 'na'])
	return data.append(total_data)



#Configure data for visual
def flatten_success(data):
	flat_list = list()
	for sublist in data:
		for item in sublist:
			flat_list.append([item[0], item[1], item[3]])
	return flat_list


def flatten_attempt(data):
	flat_list = list()
	for sublist in data:
		for item in sublist:
			flat_list.append([item[0], item[1], item[4]])
	return flat_list

def flatten_capability(data):
	flat_list = list()
	for sublist in data:
		for item in sublist:
			if(item[5] != 'na'):
				flat_list.append([item[0], item[5], 1])
	return flat_list


#Holoviews generation
def hv_table(data, label='Successes'):
	return hv.Table(data, "Team", ['Task', label])


def hv_stack(data, label='', style=dict(), side='Successes', width=400, height=400):
	return hv.Bars(data, ["Team", "Task"], side, label=label).opts(plot=dict(tools=['hover'], stack_index=1, legend_position="top", width=width, height=height), style=style)


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


def test_output(match_list, match):
	tasks = ['placeSwitch', 'placeScale']
	data = get_data(tasks, 'teleop', match_list)

	total = flatten_success(data)
	avg = flatten_success(average_tasks(data))
	avg_att = flatten_attempt(average_tasks(data))

	plot = hv_table(total) + hv_stack(avg) + hv_bar(avg) + hv_box(total)
	save_view(plot, 'test')


def graph_match(match_list, match):
    tasks = ['placeSwitch', 'placeExchange', 'placeScale']
    data = flatten_success(average_tasks(get_data(tasks, 'teleop', match_list)))
    red_place_plot = hv_bar(data[:3], 'Red Cubes Placed')
    blue_place_plot = hv_bar(data[3:], 'Blue Cubes Placed')

    tasks = ['pickupPlatform', 'pickupCubeZone', 'pickupPortal', 'pickupExchange', 'pickupFloor']
    data = flatten_success(average_tasks(get_data(tasks, 'teleop', match_list)))
    red_get_plot = hv_stack(data[:3], 'Red Pickup')
    blue_get_plot = hv_stack(data[3:], 'Blue Pickup')

    tasks = ['makeClimb']
    climbs = hv_bar(flatten_success(get_data(tasks, 'finish', match_list)), 'Climbs')

    tasks = ['getFoul', 'disabled']
    fouls = hv_bar(flatten_success(get_data(tasks, 'finish', match_list)), "Fouls")

    plot = hv.Layout(red_place_plot + red_get_plot + blue_place_plot + blue_get_plot + climbs + fouls).cols(2)
    save_view(plot, 'matchData')


def graph_event():
    tasks = ['placeSwitch', 'placeExchange', 'placeScale']
    place_plot = hv_stack(flatten_success(average_tasks(get_data(tasks, 'teleop'))), 'Cubes Placed', width=1000)

    tasks = ['climberLocation']
    climbs = hv_stack(flatten_capability(get_data(tasks, 'finish')), 'Climbs', width=1000)

    tasks = ['getFoul', 'disabled']
    fouls = hv_box(flatten_success(get_data(tasks, 'finish')), 'Problems', width=1000)

    plot = hv.Layout(place_plot + climbs + fouls).cols(1)
    save_view(plot, 'eventData')
