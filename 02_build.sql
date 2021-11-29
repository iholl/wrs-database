DROP TABLE IF EXISTS surveys, sightings;

CREATE TABLE surveys (
  id serial,
  ndow_id text PRIMARY KEY,
  survey_date bigint,
  route_id text,
  leader text,
  affiliation text,
  phone text,
  email text,
  total_observers integer,
  observer_names text,
  start_sky text,
  start_temperature text,
  start_wind text,
  end_sky text,
  end_temperature text,
  end_wind text,
  precipitation text,
  ice text, 
  fog text,
  snow_cover text
);

\copy surveys(ndow_id, survey_date, route_id, leader, affiliation, phone, email, total_observers, observer_names, start_sky, start_temperature, start_wind, end_sky, end_temperature, end_wind, precipitation, ice, fog, snow_cover) FROM 'surveys.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE sightings (
  id serial PRIMARY KEY,
  ndow_id text REFERENCES surveys (ndow_id), 
  sight_time text,
  species integer,
  number_species integer,
  activity text,
  obs_mph integer,
  distance text,
  road_side text,
  doubleback text,
  comments text,
  x bigint,
  y bigint
);

\copy sightings(ndow_id, sight_time, species, activity, obs_mph, distance, road_side, doubleback, number_species, comments, x, y) FROM 'sightings.csv' DELIMITER ',' CSV HEADER;
