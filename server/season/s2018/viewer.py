import server.view.graphing as graphing


def graph_match(match_list):
	df_rnk = graphing.get_dataframe()

	tasks = ['placeSwitch', 'placeExchange', 'placeScale']
	data = graphing.get_list(df_rnk, tasks)
	place_plot = graphing.hv_bar(graphing.split_alliances(data, match_list), 'Cubes Placed')

	tasks = ['pickupPlatform', 'pickupCubeZone', 'pickupPortal', 'pickupExchange']
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

	get_plot = graphing.hv_table(graphing.split_alliances(pickup_max, match_list), 'Pickup')

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


def examine_match(match_list):
	df_rnk = graphing.get_dataframe()
