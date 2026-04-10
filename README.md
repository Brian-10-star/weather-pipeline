# Nairobi Weather Pipeline

A live ETL pipeline that pulls current weather data from the Open-Meteo API for Nairobi, Kenya and stores it incrementally in a PostgreSQL database using Python.

## Pipeline Architecture

```
Open-Meteo API → Extract → Transform → Load → PostgreSQL
```

## Tools Used

- Python 3.13
- Requests
- Pandas
- SQLAlchemy
- PostgreSQL 18
- Open-Meteo API (free, no API key required)

## How to Run

1. Clone the repository
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Create a `.env` file with your database connection:
```
   DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/weatherdb
```
4. Create the database table:
```bash
   psql -U postgres -d weatherdb -f sql/create_table.sql
```
5. Run the pipeline:
```bash
   python main.py
```

## How It Works

Each time `main.py` is run it:
1. Calls the Open-Meteo API with Nairobi's coordinates (-1.2921, 36.8219)
2. Extracts the current temperature, wind speed and weather code
3. Loads the record into PostgreSQL with two timestamps:
   - `recorded_at` — when the weather was recorded by the sensor
   - `ingested_at` — when the pipeline ingested it into the database

Running the pipeline repeatedly builds up a historical weather dataset over time.

## Sample Output

```
[Extract] Calling weather API for coordinates: -1.2921, 36.8219
[Extract] API call successful
[Transform] Extracting fields from API response...
[Transform] Weather record ready: 24.0°C in Nairobi
[Load] Connecting to database...
[Load] Weather record written to 'weather_data'
Pipeline complete!
```

## Sample Data

| id | city | recorded_at | temperature_c | windspeed_kmh | weathercode | ingested_at |
|----|------|-------------|---------------|---------------|-------------|-------------|
| 1 | Nairobi | 2026-04-10 14:00:00 | 24.0 | 16.6 | 3 | 2026-04-10 17:05:45 |
| 2 | Nairobi | 2026-04-10 14:00:00 | 24.0 | 16.6 | 3 | 2026-04-10 17:08:30 |

## Weather Code Reference

| Code | Meaning |
|------|---------|
| 0 | Clear sky |
| 1-3 | Partly cloudy |
| 45-48 | Foggy |
| 51-67 | Rainy |
| 80-82 | Rain showers |
| 95 | Thunderstorm |

## What I'd Add Next

- Schedule pipeline with Apache Airflow to run every hour automatically
- Track multiple cities at once
- Add weather code descriptions to the database
- Build a dashboard to visualize temperature trends over time