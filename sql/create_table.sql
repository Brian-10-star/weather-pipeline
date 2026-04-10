CREATE TABLE IF NOT EXISTS weather_data (
    id              SERIAL PRIMARY KEY,
    city            VARCHAR(100),
    recorded_at     TIMESTAMP,
    temperature_c   FLOAT,
    windspeed_kmh   FLOAT,
    weathercode     INT,
    ingested_at     TIMESTAMP DEFAULT NOW()
);