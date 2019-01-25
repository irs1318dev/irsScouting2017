# import server.view.graphing as graphing
#
#
# def pickup_locations():
# 	tasks = ['pickupPlatform', 'pickupCubeZone', 'pickupPortal']
# 	team_sums = graphing.get_column('pickupFloor', 'teleop', 'sum_successes', task_rename='pickupTotal')
# 	pickup_max = graphing.get_column('pickupFloor', 'teleop', 'sum_successes')
#
# 	for location in tasks:
# 		data = graphing.get_column(location, 'teleop', 'sum_successes')
# 		for i in range(len(data)):
# 			if data[i][2] > pickup_max[i][2]:
# 				pickup_max[i] = data[i]
# 			team_sums[i][2] += data[i][2]
#
# 	for i in range(len(pickup_max)):
# 		if team_sums[i][2] != 0:
# 			pickup_max[i][2] = str(round(pickup_max[i][2] / team_sums[i][2] * 100)) + '%'
# 		else:
# 			pickup_max[i][2] = '0%'
# 	return pickup_max
#
#
# def graph_match(match_list):
# 	graphing.update_dataframe()
#
# 	tasks = ['placeSwitch', 'placeExchange', 'placeScale']
# 	data = graphing.get_list(tasks)
# 	place_plot = graphing.hv_bar(graphing.split_alliances(data, match_list), 'Cubes Placed')
#
# 	data = pickup_locations()
# 	get_plot = graphing.hv_table(graphing.split_alliances(data, match_list), 'Pickup')
#
# 	tasks = ['autoLine', 'placeSwitch', 'placeScale']
# 	data = graphing.get_list(tasks, 'auto')
# 	auto_plot = graphing.hv_stack(graphing.split_alliances(data, match_list), 'Auto')
#
# 	tasks = ['placeIncorrect', 'crossNull']
# 	data = graphing.get_list(tasks, 'auto', 'sum_successes')
# 	drop_plot = graphing.hv_table(graphing.split_alliances(data, match_list), 'Auto Fails')
#
# 	tasks = ['makeClimb', 'supportClimb', 'parkPlatform']
# 	data = graphing.get_list(tasks, 'finish')
# 	climb_plot = graphing.hv_stack(graphing.split_alliances(data, match_list), 'Climbing')
#
# 	tasks = ['disabled', 'getFoul']
# 	data = graphing.get_list(tasks, 'finish', 'sum_successes')
# 	fail_plot = graphing.hv_table(graphing.split_alliances(data, match_list), 'Total Problems')
#
# 	plot = (place_plot + get_plot + auto_plot + drop_plot + climb_plot + fail_plot).cols(2)
# 	return graphing.get_html(plot, 'matchData')
#
#
# #Print outs
# def graph_printout():
# 	graphing.update_dataframe()
#
# 	switch_sum = graphing.math_tasks(graphing.get_column('placeSwitch'), graphing.get_column('placeOpponent'), '+', 'placeSwitches')
#
# 	tasks = ['placeOpponent', 'placeSwitch', 'placeExchange']
# 	data = graphing.combine_tasks([graphing.get_list(tasks)])
# 	place_plot = graphing.hv_stack(graphing.filter_teams(data, graphing.sorted_teams(data)), 'Average Cubes Placed' + graphing.updated, width=1500, height=1160)
#
# 	data = graphing.get_column('placeScale')
# 	exchange_plot = graphing.hv_stack(graphing.filter_teams(data, graphing.sorted_teams(data)), 'Average scale Cubes Placed' + graphing.updated, width=1500, height=1160)
#
# 	return graphing.get_html(place_plot, 'eventData') + graphing.get_html(exchange_plot, 'eventData')
#
#
# #Alliance selection
# def graph_short_event():
# 	graphing.update_dataframe()
#
# 	switch_sum = graphing.math_tasks(graphing.get_column('placeSwitch'), graphing.get_column('placeOpponent'), '+', 'placeSwitches')
#
# 	tasks = ['placeScale', 'placeExchange']
# 	data = graphing.combine_tasks([switch_sum, graphing.get_list(tasks)])
# 	place_plot = graphing.hv_stack(graphing.filter_teams(data), 'Average Cubes Placed', width=1500)
#
# 	tasks = ['placeSwitch', 'placeOpponent'] + tasks
# 	data = graphing.get_list(tasks, 'teleop', 'max_successes')
# 	exchange_plot = graphing.hv_stack(graphing.filter_teams(data), 'Max Cubes Placed', width=1500)
#
# 	plot = (place_plot + exchange_plot).cols(1)
# 	return graphing.get_html(plot, 'eventData')
#
#
# def graph_long_event():
# 	graphing.update_dataframe()
#
# 	switch_sum = graphing.math_tasks(graphing.get_column('placeSwitch'), graphing.get_column('placeOpponent'), '+', 'placeSwitches')
# 	data = graphing.combine_tasks([switch_sum, graphing.get_column('placeExchange'), graphing.get_column('placeScale')])
# 	place_plot = graphing.hv_stack(graphing.filter_teams(data), 'Cubes Placed', width=1500)
#
# 	success = graphing.get_column('makeClimb', 'finish')
# 	attempt = graphing.get_column('makeClimb', 'finish')
# 	climb_plot = graphing.hv_stack(graphing.filter_teams(graphing.combine_tasks([success, attempt]), graphing.sorted_teams(success)), 'Climbs', width=1500)
#
# 	success = graphing.get_column('disabled', 'finish', 'sum_successes')
# 	attempt = graphing.math_tasks(graphing.get_column('disabled', 'finish', 'sum_attempts'), success, '-', 'temporary')
# 	foul_plot = graphing.hv_bar(graphing.filter_teams(graphing.combine_tasks([success, attempt]), graphing.scoring_teams(attempt)), 'Problems', width=1500)
#
# 	tasks = ['autoLine', 'placeSwitch', 'placeScale']
# 	data = graphing.get_list(tasks, 'auto')
# 	auto_plot = graphing.hv_stack(graphing.filter_teams(data), 'Auto', width=1500)
#
# 	data = graphing.get_list(tasks, 'auto', 'avg_attempts')
# 	auto_att = graphing.hv_stack(graphing.filter_teams(data), 'Auto Attempts', width=1500)
#
# 	plot = (auto_plot + auto_att + climb_plot + foul_plot).cols(1)
# 	graphing.save_view(plot, 'longEventData')
# 	return graphing.get_html(plot, 'longEventData')
#
#
# def examine_match(match_list):
# 	#Collect relevant data
# 	graphing.update_dataframe()
# 	match_count = graphing.get_column('autoLine', 'auto', 'matches')
#
# 	tasks = ['autoLine', 'placeSwitch', 'placeScale']
# 	auto_avg = graphing.get_list(tasks, 'auto')
#
# 	tasks = ['placeSwitch', 'placeScale', 'placeOpponent', 'placeExchange']
# 	place_avg = graphing.get_list(tasks, 'teleop')
# 	place_max = graphing.get_list(tasks, 'teleop', 'max_successes')
#
# 	tasks = ['parkPlatform', 'makeClimb', 'supportClimb']
# 	end_sum = graphing.get_list(tasks, 'finish', 'sum_successes')
#
# 	pickup_max = pickup_locations()
# 	disabled_sum = graphing.get_column('disabled', 'finish', 'sum_attempts')
#
# 	#Display teams in match
# 	team_widgets = list()
# 	for team in match_list:
# 		widget = '<td style="padding: 5px;"><h3>Team ' + team + ' &nbsp;Played: ' + str(graphing.filter_teams(match_count, [team])[0][2]) + '</h3>'
# 		widget += '<div> <div style="float: left;">'
#
# 		#Auto
# 		widget += " --Auto Averages-- <br>"
# 		widget += "Cross Auto Line: &nbsp;" + graphing.value(auto_avg, team, 'autoLine') + "&nbsp;&nbsp;&nbsp;<br>"
# 		widget += "Place Switch: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + graphing.value(auto_avg, team, 'placeSwitch') + "&nbsp;&nbsp;<br>"
# 		widget += "Place Scale: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + graphing.value(auto_avg, team, 'placeScale') + "&nbsp;&nbsp;<br>"
#
# 		#Ending
# 		widget += "<br> --Final Sums-- <br>"
# 		widget += "Parked: &nbsp;&nbsp;" + graphing.value(end_sum, team, 'parkPlatform') + "<br>"
# 		widget += "Climbs: &nbsp;&nbsp;" + graphing.value(end_sum, team, 'makeClimb') + "<br>"
# 		widget += "Support: &nbsp;" + graphing.value(end_sum, team, 'supportClimb') + "<br>"
#
# 		widget += '</div> <div style="float: left;">'
#
# 		#Placement
# 		widget += "<br> --Placement-- <br>"
# 		widget += "Switch Max: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + graphing.value(place_max, team, 'placeSwitch')
# 		widget += " &nbsp;Avg: &nbsp;" + graphing.value(place_avg, team, 'placeSwitch') + "&nbsp;&nbsp;<br>"
# 		widget += "Scale Max: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + graphing.value(place_max, team, 'placeScale')
# 		widget += " &nbsp;Avg: &nbsp;" + graphing.value(place_avg, team, 'placeScale') + "&nbsp;&nbsp;<br>"
# 		widget += "Opponent Max: &nbsp;" + graphing.value(place_max, team, 'placeOpponent')
# 		widget += " &nbsp;Avg: &nbsp;" + graphing.value(place_avg, team, 'placeOpponent') + "&nbsp;&nbsp;<br>"
# 		widget += "Exchange Max: &nbsp;" + graphing.value(place_max, team, 'placeExchange')
# 		widget += " &nbsp;Avg: &nbsp;" + graphing.value(place_avg, team, 'placeExchange') + "&nbsp;&nbsp;<br>"
#
# 		#Other
# 		pickup_team = graphing.filter_teams(pickup_max, [team])[0]
# 		widget += "<br>" + pickup_team[1] + " for " + pickup_team[2] + "<br>"
# 		widget += "<br>Disabled: " + graphing.value(disabled_sum, team, 'disabled')
#
# 		widget += "</div> </div>"
# 		widget += "</td>"
# 		team_widgets.append(widget)
#
# 	#Place display into table
# 	out = '<table> <tr class="Red">'
# 	out += team_widgets[0] + team_widgets[1] + team_widgets[2]
# 	out += '</tr><tr class="Blue">'
# 	out += team_widgets[3] + team_widgets[4] + team_widgets[5]
# 	out += '</tr></table>'
# 	return out
#
