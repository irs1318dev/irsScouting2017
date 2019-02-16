#finding the total number of successes in auto
sql = """SELECT teams.name, measures.successes
FROM teams,measures,tasks,phases
WHERE teams.id = measures.team_id
AND tasks.id = measures.task_id
AND phases.id = measures.phase_id
AND phases.name = 'auto'
"""
#finding the total for each team in teleop for a certain indicator
sql = """SELECT teams.name, SUM(measures.successes)
FROM teams,measures,tasks,phases
WHERE teams.id = measures.team_id
AND tasks.id = measures.task_id
AND phases.id = measures.phase_id
AND tasks.name = 'placeGear'
AND phases.name = 'teleop'
GROUP BY teams.name"""

#FINDING THE NUMBER OF POINTS PER MATCH PER ALLIANCE

sql = """SELECT matches.name, alliances.name, sum(measures.successes)
FROM matches,alliances,measures,events
WHERE matches.id = measures.match_id
AND alliances.id = measures.alliance_id
AND events.id = measures.event_id
AND alliances.name in ('red', 'blue')
AND events.name = 'pncmp'
GROUP BY matches.name,alliances.name
ORDER BY matches.name,alliances.name"""
#the numbers are big, ask stacy


#for all alliances, including na (what is that?)
sql = """SELECT matches.name, alliances.name, sum(measures.successes)
FROM matches,alliances,measures
WHERE matches.id = measures.match_id
AND alliances.id = measures.alliance_id
GROUP BY matches.name,alliances.name
ORDER BY matches.name, alliances.name;"""

#same thing, but ID to the event itself
sql  = """SELECT matches.name, alliances.name, sum(measures.successes)
FROM matches,alliances,measures,events
WHERE matches.id = measures.match_id
AND alliances.id = measures.alliance_id
AND events.id = measures.event_id
AND events.name = 'pncmp'
GROUP BY matches.name,alliances.name
ORDER BY matches.name, alliances.name;"""

#for blue:
sql = """SELECT matches.name, alliances.name, sum(measures.successes)
FROM matches,alliances,measures
WHERE matches.id = measures.match_id
AND alliances.id = measures.alliance_id
AND alliances.name = 'blue' 
GROUP BY matches.name,alliances.name
ORDER BY matches.name, alliances.name;"""


#for red:
sql = """SELECT matches.name, alliances.name, sum(measures.successes)
FROM matches,alliances,measures
WHERE matches.id = measures.match_id
AND alliances.id = measures.alliance_id
AND alliances.name = 'red' 
GROUP BY matches.name,alliances.name
ORDER BY matches.name, alliances.name;"""

#total number of points for a certain indicator at a certain event at a certain match
sql = """SELECT matches.name, alliances.name, sum(measures.successes)
FROM matches,alliances,measures,events,tasks
WHERE matches.id = measures.match_id
AND alliances.id = measures.alliance_id
AND events.id = measures.event_id
AND tasks.id = measures.task_id
AND events.name = 'pncmp'
AND tasks.name = 'climbRope'
GROUP BY matches.name,alliances.name
ORDER BY matches.name, alliances.name;"""