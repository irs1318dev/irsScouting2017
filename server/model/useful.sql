SELECT phases.name AS phase, actors.name AS actor, tasks.name AS task,
measures.capability, measures.attempts, measures.successes, measures.cycle_times
FROM measures INNER JOIN tasks ON measures.task_id=tasks.id
INNER JOIN phases ON measures.phase_id = phases.id
INNER JOIN actors ON measures.actor_id = actors.id
WHERE event_id=25137
ORDER BY task;

SELECT * FROM schedules WHERE event_id=25137
ORDER BY "date" DESC;


SELECT
    events.name AS "event", levels.name AS "level", matches.name AS "match",
    teams.name AS team, tasks.name AS task, task_options.option_name,
    measures.attempts AS attempts, measures.successes AS successes
FROM measures
    INNER JOIN events ON measures.event_id = events.id
    INNER JOIN levels ON measures.level_id = levels.id
    INNER JOIN matches ON measures.match_id = matches.id
    INNER JOIN teams ON measures.team_id = teams.id
    INNER JOIN tasks ON measures.task_id = tasks.id
    LEFT JOIN task_options ON measures.capability = task_options.id
WHERE
    events.name = 'waiss'
ORDER BY
    matches.name, teams.name;


SELECT * FROM schedules INNER JOIN events ON schedules.event_id = events."id"
WHERE events.name = 'wayak' AND events.season = '2018' ORDER BY "match" DESC;

-- Getting match count
SELECT team, COUNT(schedules.id)
	FROM schedules
	INNER JOIN status ON schedules.event_id = status.event_id
	WHERE schedules.match < status.match
	GROUP BY team
