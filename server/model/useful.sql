SELECT phases.name AS phase, actors.name AS actor, tasks.name AS task,
measures.capability, measures.attempts, measures.successes, measures.cycle_times
FROM measures INNER JOIN tasks ON measures.task_id=tasks.id
INNER JOIN phases ON measures.phase_id = phases.id
INNER JOIN actors ON measures.actor_id = actors.id
WHERE event_id=25137
ORDER BY task;

SELECT * FROM schedules WHERE event_id=25137
ORDER BY "date" DESC;
