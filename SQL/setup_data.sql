CREATE TABLE measures (
    event_id 	int not null REFERENCES events(id),
    match_id 	int not null REFERENCES matches(id),
    team_id 	int not null REFERENCES teams(id),
    level_id    int not null REFERENCES levels(id),
    date_id     int not null REFERENCES dates(id),
    alliance_id int not null REFERENCES alliances(id),
    station_id  int not null REFERENCES stations(id),
    actor_id    int not null REFERENCES actors(id),
    task_id     int not null REFERENCES tasks(id),
    format_id   int not null REFERENCES formats(id),
    phase_id    int not null REFERENCES phases(id),
    
    
    success int not null default 0,
    failure int not null default 0
);

CREATE TABLE schedule (

	event_id 	int not null REFERENCES events(id),
    match_id 	int not null REFERENCES matches(id),
    team_id 	int not null REFERENCES teams(id),
    level_id    int not null REFERENCES levels(id),
    date_id     int not null REFERENCES dates(id),
    alliance_id int not null REFERENCES alliances(id),
    station_id  int not null REFERENCES stations(id)
);

CREATE TABLE game (
    actor_id    int not null REFERENCES actors(id),
    task_id   int not null REFERENCES tasks(id)
);

	

CREATE UNIQUE INDEX measures_idx 
	ON measures (event_id, match_id, team_id, level_id, date_id, alliance_id, station_id, actor_id, task_id, format_id, phase_id)
   
   CREATE UNIQUE INDEX game_idx 
	ON measures (event_id, match_id, team_id, level_id, date_id, alliance_id, station_id, actor_id, task_id, format_id, phase_id)
    
    CREATE UNIQUE INDEX schedule_idx 
	ON measures (event_id, match_id, team_id, level_id, date_id, alliance_id, station_id, actor_id, task_id, format_id, phase_id)