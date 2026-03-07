
-- RELATIONAL DATABASE SCHEMA (MySQL)
-- Database: assignment_db

-- TABLE 1: Dimension table for physical weather stations
CREATE TABLE Station (
    station_id INT PRIMARY KEY AUTO_INCREMENT,
    station_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL
);

-- TABLE 2: Main fact table for daily time-series climate data
CREATE TABLE Daily_Climate (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    record_date DATE NOT NULL,
    mean_temp FLOAT,
    humidity FLOAT,
    wind_speed FLOAT,
    station_id INT,
    FOREIGN KEY (station_id) REFERENCES Station(station_id),
    UNIQUE (station_id, record_date)
);

-- TABLE 3: Log table for machine learning predictions
CREATE TABLE Model_Prediction (
    prediction_id INT PRIMARY KEY AUTO_INCREMENT,
    target_date DATE NOT NULL,
    predicted_temp FLOAT NOT NULL,
    station_id INT,
    FOREIGN KEY (station_id) REFERENCES Station(station_id)
);

-- Insert our base station so foreign keys work correctly
INSERT INTO Station (station_name, city) VALUES ('Central Agricultural Hub', 'Delhi');

-- 3 REQUIRED SQL QUERIES (Task 2)

-- Query 1: Latest climate reading (Time-Series Ordering)
SELECT record_date, mean_temp, humidity 
FROM Daily_Climate 
ORDER BY record_date DESC 
LIMIT 1;

-- Query 2: Date range query (Time-Series Filtering)
SELECT record_date, wind_speed 
FROM Daily_Climate 
WHERE record_date BETWEEN '2013-01-02' AND '2013-01-04';

-- Query 3: Relational JOIN for ML predictions
SELECT Station.station_name, Model_Prediction.target_date, Model_Prediction.predicted_temp
FROM Model_Prediction
JOIN Station ON Model_Prediction.station_id = Station.station_id;
