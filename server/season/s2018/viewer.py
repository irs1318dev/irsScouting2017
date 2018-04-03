import server.view.graphing as graphing


def pickup_locations(df_rnk):
	tasks = ['pickupPlatform', 'pickupCubeZone', 'pickupPortal']
	team_sums = graphing.get_column(df_rnk, 'pickupFloor', 'teleop', 'sum_successes', task_rename='pickupTotal')
	pickup_max = graphing.get_column(df_rnk, 'pickupFloor', 'teleop', 'sum_successes')

	for location in tasks:
		data = graphing.get_column(df_rnk, location, 'teleop', 'sum_successes')
		for i in range(len(data)):
			if data[i][2] > pickup_max[i][2]:
				pickup_max[i] = data[i]
			team_sums[i][2] += data[i][2]

	for i in range(len(pickup_max)):
		if team_sums[i][2] != 0:
			pickup_max[i][2] = str(round(pickup_max[i][2] / team_sums[i][2] * 100)) + '%'
		else:
			pickup_max[i][2] = '0%'
	return pickup_max


def graph_match(match_list):
	df_rnk = graphing.get_dataframe()

	tasks = ['placeSwitch', 'placeExchange', 'placeScale']
	data = graphing.get_list(df_rnk, tasks)
	place_plot = graphing.hv_bar(graphing.split_alliances(data, match_list), 'Cubes Placed')

	data = pickup_locations(df_rnk)
	get_plot = graphing.hv_table(graphing.split_alliances(data, match_list), 'Pickup')

	tasks = ['autoLine', 'placeSwitch', 'placeScale']
	data = graphing.get_list(df_rnk, tasks, 'auto')
	auto_plot = graphing.hv_stack(graphing.split_alliances(data, match_list), 'Auto')

	tasks = ['placeIncorrect', 'crossNull']
	data = graphing.get_list(df_rnk, tasks, 'auto', 'sum_successes')
	drop_plot = graphing.hv_table(graphing.split_alliances(data, match_list), 'Auto Fails')

	tasks = ['makeClimb', 'supportClimb', 'parkPlatform']
	data = graphing.get_list(df_rnk, tasks, 'finish')
	climb_plot = graphing.hv_stack(graphing.split_alliances(data, match_list), 'Climbing')

	tasks = ['disabled', 'getFoul']
	data = graphing.get_list(df_rnk, tasks, 'finish', 'sum_successes')
	fail_plot = graphing.hv_table(graphing.split_alliances(data, match_list), 'Total Problems')

	plot = (place_plot + get_plot + auto_plot + drop_plot + climb_plot + fail_plot).cols(2)
	return graphing.get_html(plot, 'matchData')


def graph_event():
	df_rnk = graphing.get_dataframe()

	tasks = ['placeSwitch', 'placeScale', 'placeExchange']
	data = graphing.get_list(df_rnk, tasks)
	place_plot = graphing.hv_stack(graphing.filter_teams(data), 'Average Cubes Placed', width=1500)

	data = graphing.get_list(df_rnk, tasks, 'teleop', 'max_successes')
	exchange_plot = graphing.hv_stack(graphing.filter_teams(data), 'Max Cubes Placed', width=1500)

	plot = (place_plot + exchange_plot).cols(1)
	graphing.save_view(plot, 'eventData')
	return graphing.get_html(plot, 'eventData')


def graph_long_event():
	df_rnk = graphing.get_dataframe()

	tasks = ['placeSwitch', 'placeExchange', 'placeScale']
	data = graphing.get_list(df_rnk, tasks)
	place_plot = graphing.hv_stack(graphing.filter_teams(data), 'Cubes Placed', width=1500)

	success = graphing.get_column(df_rnk, 'makeClimb', 'finish', 'sum_successes')
	attempt = graphing.get_column(df_rnk, 'makeClimb', 'finish', 'sum_attempts', task_rename='attemptClimb')
	climb_plot = graphing.hv_bar(graphing.filter_teams(graphing.combine_tasks([success, attempt]), graphing.sorted_teams(success)), 'Climbs', width=1500)

	success = graphing.get_column(df_rnk, 'disabled', 'finish', 'sum_successes')
	attempt = graphing.get_column(df_rnk, 'disabled', 'finish', 'sum_attempts', task_rename='temporary')
	foul_plot = graphing.hv_bar(graphing.filter_teams(graphing.combine_tasks([success, attempt]), graphing.scoring_teams(attempt)), 'Problems', width=1500)

	tasks = ['autoLine', 'placeSwitch', 'placeScale']
	data = graphing.get_list(df_rnk, tasks, 'auto')
	auto_plot = graphing.hv_stack(graphing.filter_teams(data), 'Auto', width=1500)

	plot = (place_plot + auto_plot + climb_plot + foul_plot).cols(1)
	graphing.save_view(plot, 'longEventData')
	return graphing.get_html(plot, 'longEventData')


def single_point(data, team, task):
	data = graphing.filter_teams(data, [team])
	for row in data:
		if row[1] == task:
			return str(round(float(row[2]), 2))
	return "0.0"

def examine_match(match_list):
	df_rnk = graphing.get_dataframe()

	tasks = ['autoLine', 'placeSwitch', 'placeScale']
	auto_avg = graphing.get_list(df_rnk, tasks, 'auto')

	tasks = ['placeSwitch', 'placeScale', 'placeOpponent', 'placeExchange']
	place_avg = graphing.get_list(df_rnk, tasks, 'teleop')
	place_max = graphing.get_list(df_rnk, tasks, 'teleop', 'max_successes')

	tasks = ['parkPlatform', 'makeClimb', 'supportClimb']
	end_sum = graphing.get_list(df_rnk, tasks, 'finish', 'sum_successes')

	pickup_max = pickup_locations(df_rnk)
	disabled_sum = graphing.get_column(df_rnk, 'disabled', 'finish', 'sum_attempts')

	team_widgets = list()
	for team in match_list:
		widget = '<td style="padding: 5px;"><h3>Team ' + team + '</h3>'

		widget += '<div> <div style="float: left;">'

		widget += " --Auto Averages-- <br>"
		widget += "Cross Auto Line: &nbsp;" + single_point(auto_avg, team, 'autoLine') + "&nbsp;&nbsp;&nbsp;<br>"
		widget += "Place Switch: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + single_point(auto_avg, team, 'placeSwitch') + "&nbsp;&nbsp;<br>"
		widget += "Place Scale: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + single_point(auto_avg, team, 'placeScale') + "&nbsp;&nbsp;<br>"

		widget += "<br> --Final Sums-- <br>"
		widget += "Parked: &nbsp;&nbsp;" + single_point(end_sum, team, 'parkPlatform') + "<br>"
		widget += "Climbs: &nbsp;&nbsp;" + single_point(end_sum, team, 'makeClimb') + "<br>"
		widget += "Support: &nbsp;" + single_point(end_sum, team, 'supportClimb') + "<br>"

		widget += '</div> <div style="float: left;">'

		widget += " --Placement-- <br>"
		widget += "Switch Max: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + single_point(place_max, team, 'placeSwitch')
		widget += " &nbsp;Avg: &nbsp;" + single_point(place_avg, team, 'placeSwitch') + "&nbsp;&nbsp;<br>"
		widget += "Scale Max: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + single_point(place_max, team, 'placeScale')
		widget += " &nbsp;Avg: &nbsp;" + single_point(place_avg, team, 'placeScale') + "&nbsp;&nbsp;<br>"
		widget += "Opponent Max: &nbsp;" + single_point(place_max, team, 'placeOpponent')
		widget += " &nbsp;Avg: &nbsp;" + single_point(place_avg, team, 'placeOpponent') + "&nbsp;&nbsp;<br>"
		widget += "Exchange Max: &nbsp;" + single_point(place_max, team, 'placeExchange')
		widget += " &nbsp;Avg: &nbsp;" + single_point(place_avg, team, 'placeExchange') + "&nbsp;&nbsp;<br>"
		
		pickup_team = graphing.filter_teams(pickup_max, [team])[0]
		widget += "<br>" + pickup_team[1] + " for " + pickup_team[2] + "<br>"

		widget += "<br>Disabled: " + single_point(disabled_sum, team, 'disabled')

		widget += "</div> </div>"
		
		widget += "</td>"
		team_widgets.append(widget)

	out = '<table> <tr class="Red">'
	out += team_widgets[0] + team_widgets[1] + team_widgets[2]
	out += '</tr><tr class="Blue">'
	out += team_widgets[3] + team_widgets[4] + team_widgets[5]
	out += '</tr></table>'
	return out

