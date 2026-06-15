/*
Agency
*/

CREATE TABLE agency AS
  SELECT 
    * EXCLUDE(agency_phone, agency_id),
    CAST(agency_phone AS VARCHAR) AS agency_phone,
    CAST(agency_id AS VARCHAR) AS agency_id
  FROM read_csv('./files/agency.txt');

/*
Calendar dates
*/

CREATE TABLE calendar_dates AS
SELECT
  * EXCLUDE(date),
  CAST(strptime(CAST(date AS VARCHAR), '%Y%m%d') AS DATE) AS date,
FROM read_csv('./files/calendar_dates.txt');

/*
Calendar 
*/

CREATE TABLE calendar AS
SELECT
  * EXCLUDE(start_date, end_date),
  CAST(strptime(CAST(start_date AS VARCHAR), '%Y%m%d') AS DATE) AS start_date,
  CAST(strptime(CAST(end_date AS VARCHAR), '%Y%m%d') AS DATE) AS end_date,
FROM read_csv('./files/calendar.txt');

/*
Feed info
*/

CREATE TABLE feed_info AS
  SELECT
    * EXCLUDE(feed_start_date, feed_end_date),
    CAST(strptime(CAST(feed_start_date AS VARCHAR), '%Y%m%d') AS DATE) AS feed_start_date,
    CAST(strptime(CAST(feed_end_date AS VARCHAR), '%Y%m%d') AS DATE) AS feed_end_date
  FROM read_csv('./files/feed_info.txt');

/*
Routes
*/

CREATE TABLE routes AS
  SELECT
    * EXCLUDE(route_color, route_text_color),
    CAST(route_color AS VARCHAR) AS route_color,
    CAST(route_text_color AS VARCHAR) AS route_text_color
  FROM read_csv('./files/routes.txt');

INSTALL spatial;
LOAD spatial;

/*
Shapes
*/

CREATE TABLE shapes AS
SELECT
  *,
  ST_Point(shape_pt_lon, shape_pt_lat) AS shape_pt_point
FROM read_csv('./files/shapes.txt');

/*
Geoshapes
*/

CREATE TABLE geoshapes AS
SELECT
  shape_id,
  ST_MakeLine(LIST(shape_pt_point ORDER BY shape_pt_sequence)) AS 'geometry'
FROM shapes
WHERE shape_pt_point IS NOT NULL
GROUP BY shape_id;

/*
Stop times
*/

CREATE TABLE stop_times AS
SELECT
  * EXCLUDE(arrival_time, departure_time),
  INTERVAL (
    CAST(split_part(arrival_time::VARCHAR, ':', 1) AS INTEGER) * 3600 +
    CAST(split_part(arrival_time::VARCHAR, ':', 2) AS INTEGER) * 60 +
    CAST(split_part(arrival_time::VARCHAR, ':', 3) AS INTEGER)
  ) SECOND AS arrival_time,
  INTERVAL (
    CAST(split_part(departure_time::VARCHAR, ':', 1) AS INTEGER) * 3600 +
    CAST(split_part(departure_time::VARCHAR, ':', 2) AS INTEGER) * 60 +
    CAST(split_part(departure_time::VARCHAR, ':', 3) AS INTEGER)
  ) SECOND AS departure_time
FROM read_csv('./files/stop_times.txt', types={'arrival_time': 'VARCHAR', 'departure_time': 'VARCHAR', 'stop_id': 'VARCHAR'});

/*
Stops
*/

CREATE TABLE stops AS
  SELECT
    *,
    ST_Point(stop_lon, stop_lat) AS stop_point
  FROM read_csv('./files/stops.txt');

/*
Trips
*/

CREATE TABLE trips AS
SELECT * FROM read_csv('./files/trips.txt');

/*
Shapes of the trips going through a specific stop

Populate the table stop_shapes with the shape_id of the trips that go through each stop_id. 
*/

CREATE OR REPLACE TABLE stop_shapes AS
SELECT DISTINCT
  st.stop_id,
  t.shape_id
FROM stop_times st
JOIN trips t ON st.trip_id = t.trip_id
WHERE st.stop_id IS NOT NULL AND t.shape_id IS NOT NULL;

/*
Create a table that contains the distance between each stop and the shapes that go through it. 
*/

CREATE OR REPLACE TABLE stop_shape_distances AS
SELECT
  ss.stop_id,
  ss.shape_id,
  ST_Distance(s.stop_point, g.geometry) AS distance
FROM stop_shapes ss
JOIN stops s ON ss.stop_id = s.stop_id
JOIN geoshapes g ON ss.shape_id = g.shape_id
WHERE s.stop_point IS NOT NULL AND g.geometry IS NOT NULL;

/*
Add a column to the stop_shape_distances table with the closest point on the shape to the stop. 
*/

ALTER TABLE stop_shape_distances
ADD COLUMN closest_point GEOMETRY;

UPDATE stop_shape_distances
SET closest_point = ST_ClosestPoint(
  (SELECT geometry FROM geoshapes WHERE shape_id = stop_shape_distances.shape_id),
  (SELECT stop_point FROM stops WHERE stop_id = stop_shape_distances.stop_id)
)
WHERE closest_point IS NULL;

/*
Update agency_fare_url in the agency table to https://www.incofer.go.cr/transporte-de-personas/
*/

UPDATE agency
SET agency_fare_url = 'https://www.incofer.go.cr/transporte-de-personas/'
WHERE agency_id = 'INCOFER';

/*
Substitute all locations stop_point in the stops table with the closest point on the first shape that goes through each stop.
*/

UPDATE stops s
SET stop_point = (
  SELECT closest_point
  FROM stop_shape_distances ssd
  WHERE ssd.stop_id = s.stop_id
  ORDER BY distance
  LIMIT 1
)
WHERE s.stop_point IS NOT NULL;

/*
Update stop_lon and stop_lat in the stops table to match the new stop_point. 
*/

UPDATE stops
SET stop_lon = ST_X(stop_point),
    stop_lat = ST_Y(stop_point)
WHERE stop_point IS NOT NULL;

/*
Export the updated stops table to a new CSV file in ./files/stops.txt, but without the stop_point column, and with the header.
*/

COPY (
  SELECT * EXCLUDE (stop_point)
  FROM stops
)
TO './files/stops.txt' WITH CSV HEADER;

