CREATE TABLE phases
(
    id	  	serial primary key,
    name  	text unique not null
);

CREATE TABLE formats
(
    id	  	serial primary key,
    name  	text unique not null,
    
    type 	text
);

CREATE TABLE events
(
    id	  	serial primary key,
    name  	text unique not null,
    
    location text
);

CREATE TABLE teams
(
    id	  	serial primary key,
    name  	text unique not null,
    
    title 	text
);

CREATE TABLE alliances
(
    id	  	serial primary key,
    name  	text unique not null
);

CREATE TABLE tasks
(
    id	  	serial primary key,
    name  	text unique not null,
    
    success text not null,
    failure text
);

CREATE TABLE actors
(
    id	  	serial primary key,
    name  	text unique not null
);

CREATE TABLE stations
(
    id	  	serial primary key,
    name  	text unique not null
);

CREATE TABLE matches
(
    id	  	serial primary key,
    name  	text unique not null
);

CREATE TABLE levels
(
    id	  	serial primary key,
    name  	text unique not null
);

CREATE TABLE dates
(
    id	  	serial primary key,
    name  	text unique not null
);
