DROP TABLE IF EXISTS surveys, sightings, speciesLookup;

CREATE TABLE speciesLookup (
  species_id integer NOT NULL,
  species_name text NOT NULL
);

\copy speciesLookup(species_id, species_name) FROM 'species_lookup_table.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE surveys (
  id serial,
  ndow_id text PRIMARY KEY,
  unix_date bigint,
  route_id text,
  leader text,
  affiliation text,
  phone text,
  email text,
  observers integer,
  observer_names text,
  precipitation text,
  ice text, 
  fog text,
  snow_cover text,
  complete text
);

\copy surveys(ndow_id, unix_date, route_id, leader, affiliation, phone, email, observers, observer_names, precipitation, ice, fog, snow_cover, complete) FROM 'surveys.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE sightings (
  id serial PRIMARY KEY,
  ndow_id text REFERENCES surveys (ndow_id), 
  sight_time text,
  species integer,
  species_name text,
  species_count integer,
  activity text,
  speed integer,
  distance text,
  direction text,
  doubleback text,
  comments text,
  x bigint,
  y bigint
);

\copy sightings(ndow_id, sight_time, species, species_count, activity, speed, distance, direction, doubleback, comments, x, y) FROM 'sightings.csv' DELIMITER ',' CSV HEADER;

ALTER TABLE sightings ADD COLUMN geom geometry(Point, 26911);
UPDATE sightings SET geom = ST_SetSRID(ST_MakePoint(x, y), 26911);

UPDATE sightings AS v SET species_name = s.species_name FROM speciesLookup AS s WHERE v.species = s.species_id;

ALTER TABLE surveys ADD COLUMN surveyed_date date;
UPDATE surveys SET surveyed_date = to_timestamp(surveys.unix_date/1000);
