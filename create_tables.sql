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