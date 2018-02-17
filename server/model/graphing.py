import sys
import os
import re

import pandas as pd 
# This section is necessary for viewing plots in the notebook.
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import holoviews as hv
hv.extension('bokeh','matplotlib')
import seaborn as snsb
from sqlalchemy import text

import server.model.connection
import server.model.event as event
import server.model.dal as sm_dal

matplotlib.style.use("ggplot")
engine = server.model.connection.engine


def get_data(tasks, phase='teleop', teams=None):
	teams_tasks_data = list()
	conn = engine.connect()
	evt = event.EventDal.get_current_event()
	event_id = sm_dal.event_ids[evt]
	phase_id = sm_dal.phase_ids[phase]

	if(teams is None):
		teams = Graphing.get_teams()

	for team in teams:
		team_id = sm_dal.team_ids[team]
		team_data = list()

		for task in tasks:
			task_id = sm_dal.task_ids[task]

			sql = text("SELECT * FROM measures WHERE "
					   "event_id = :event_id "
					   "AND task_id = :task_id "
					   "AND team_id = :team_id "
					   "AND phase_id = :phase_id;")

			results = conn.execute(sql, event_id=event_id, task_id=task_id,
								   team_id=team_id, phase_id=phase_id).fetchall()

			for row in results:
				match = sm_dal.match_names[row['match_id']]
				attempts = row['attempts']
				successes = row['successes']
				capability = row['capability']

				team_data.append([team, task, match, attempts, successes, capability])

		teams_tasks_data.append(team_data)

	conn.close()
	return teams_tasks_data


def get_teams():
	all_teams = list()
	sql = text("SELECT DISTINCT team FROM schedules WHERE "
			   "event = :event ORDER BY team;")

	conn = engine.connect()
	results = conn.execute(sql, event=event.EventDal.get_current_event())
	conn.close()

	for row in results:
		all_teams.append(str(row).split('\'')[1])

	return all_teams


def average_tasks(team_data):
	task = None
	fixed_data = list()
	current_data = list()
	sum = 1

	for row in team_data:
		if row[1] == task:
			current_data[2] += row[3]
			current_data[3] += row[4]
			sum += 1
		else:
			if task is not None:
				fixed_data.append([current_data[0], current_data[1], 'na', current_data[2] / sum, current_data[3] / sum])

			current_data = [row[0], row[1], row[3], row[4]]
			task = row[1]
			sum = 1

	fixed_data.append([current_data[0], current_data[1], 'na', current_data[2] / sum, current_data[3] / sum])
	return fixed_data


def save_view(view, name):
	renderer = hv.renderer('bokeh')
	# Convert to bokeh figure then save using bokeh
	plot = renderer.get_plot(view).state

	from bokeh.io import output_file, save, show
	save(plot, name + '.html')
