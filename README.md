# Nairobi Weather Pipeline

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-316192?logo=postgresql)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.x-017CEE?logo=apacheairflow)
![API](https://img.shields.io/badge/API-Open--Meteo-orange)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

A live ETL pipeline that pulls real-time weather data for Nairobi, Kenya from the Open-Meteo API and loads it incrementally into PostgreSQL — building a growing historical dataset with every run. Extended with an **Apache Airflow DAG** for fully automated hourly execution.

This repository covers two projects:
- **Project 2** — Core ETL pipeline (Python script)
- **Project 3** — Airflow automation (DAG with scheduled runs)

---

## Project 2 — Core Weather Pipeline

### Pipeline Architecture

```
Open-Meteo REST API
(Nairobi: lat -1.2921, lon 36.8219)
        │
        ▼
┌───────────────┐
│    Extract    │  HTTP GET request → parse JSON response
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   Transform   │  Extract temperature, wind speed, weather code
│               │  Add recorded_at and ingested_at timestamps
└───────┬───────┘
        │
        ▼
┌───────────────┐
│     Load      │  Append new record to PostgreSQL (incremental)
└───────┬───────┘
        │
        ▼
  PostgreSQL DB
  weatherdb → weather_data
  (grows with every run)
```

### Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.13 | Pipeline logic |
| Requests | HTTP calls to Open-Meteo API |
| Pandas | Data transformation |
| SQLAlchemy | Database connection and loading |
| psycopg2 | PostgreSQL driver |
| python-dotenv | Secure credential management |
| PostgreSQL 18 | Incremental data storage |
| Open-Meteo API | Free weather data — no API key required |

### How It Works

Each run of `main.py`:
1. Calls the Open-Meteo API with Nairobi's coordinates (`-1.2921, 36.8219`)
2. Extracts temperature (°C), wind speed (km/h), and weather code
3. Adds two timestamps:
   - `recorded_at` — when the weather was recorded by the sensor
   - `ingested_at` — when the pipeline ran and wrote to the database
4. Appends the record to PostgreSQL — never overwrites, always increments

Running the pipeline repeatedly builds a historical weather dataset over time, enabling trend analysis across hours, days, and weeks.

### Sample Output

```
[Extract] Calling weather API for coordinates: -1.2921, 36.8219
[Extract] API call successful
[Transform] Extracting fields from API response...
[Transform] Weather record ready: 24.0°C in Nairobi
[Load] Connecting to database...
[Load] Weather record written to 'weather_data'
Pipeline complete!
```

### Sample Data

| id | city | recorded_at | temperature_c | windspeed_kmh | weathercode | ingested_at |
|---|---|---|---|---|---|---|
| 1 | Nairobi | 2026-04-10 14:00:00 | 24.0 | 16.6 | 3 | 2026-04-10 17:05:45 |
| 2 | Nairobi | 2026-04-10 15:00:00 | 23.5 | 14.2 | 1 | 2026-04-10 18:05:30 |

### Weather Code Reference

| Code | Meaning |
|---|---|
| 0 | Clear sky |
| 1–3 | Partly cloudy |
| 45–48 | Foggy |
| 51–67 | Rainy |
| 80–82 | Rain showers |
| 95 | Thunderstorm |

### How to Run

```bash
# 1. Clone the repository
git clone https://github.com/Brian-10-star/weather-pipeline.git
cd weather-pipeline

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your .env file
echo "DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/weatherdb" > .env

# 4. Create the database table
psql -U postgres -d weatherdb -f sql/create_table.sql

# 5. Run the pipeline
python main.py
```

---

## Project 3 — Airflow Automation (weather_dag.py)

The pipeline was converted into an **Apache Airflow DAG** that runs automatically every hour — eliminating manual execution entirely.

### DAG Architecture

```
Airflow Scheduler (cron: @hourly)
        │
        ▼
┌─────────────────┐
│ extract_weather │  Calls Open-Meteo API, returns raw JSON via XCom
└────────┬────────┘
         │  XCom
         ▼
┌──────────────────┐
│transform_weather │  Parses JSON, structures into a clean record via XCom
└────────┬─────────┘
         │  XCom
         ▼
┌───────────────┐
│ load_weather  │  Writes record to PostgreSQL weatherdb.weather_data
└───────────────┘
```

### Key Features

| Feature | Detail |
|---|---|
| Schedule | `@hourly` cron — runs every hour automatically |
| Task communication | XCom — passes data between tasks without temp files |
| Fault tolerance | Automatic retries with 5-minute delay on task failure |
| Monitoring | Live Airflow web dashboard at `http://localhost:8080` |
| Environment | Ubuntu via WSL2 on Windows 11 |

### DAG File Location

```
~/airflow/dags/weather_dag.py
```

### Running Airflow

Airflow requires two terminals running simultaneously:

```bash
# Terminal 1 — start the web server
airflow webserver --port 8080

# Terminal 2 — start the scheduler
airflow scheduler
```

Then open `http://localhost:8080` in your browser to monitor DAG runs and task logs.

---

## Project Portfolio

This is Projects 2 & 3 of 5 in my Data Engineering portfolio:

| # | Project | Tools |
|---|---|---|
| 1 | [NYC Taxi Pipeline](https://github.com/Brian-10-star/nyc-taxi-pipeline) | Python, Pandas, PostgreSQL |
| 2 | **Nairobi Weather Pipeline** ← you are here | Python, REST API, PostgreSQL |
| 3 | **Airflow Weather DAG** ← you are here | Apache Airflow, Cron, XCom |
| 4 | [dbt Data Warehouse](https://github.com/Brian-10-star/taxi-dbt) | dbt, SQL, Data Modeling |
| 5 | Cloud Pipeline | GCP, Cloud Storage, Cloud Functions |

---

## Author

**Brian Mbugua Chira**
BSc Computer Science — Egerton University, Kenya (Expected 2028)

- GitHub: [github.com/Brian-10-star](https://github.com/Brian-10-star)
- LinkedIn: [linkedin.com/in/mbuguabrian](https://linkedin.com/in/mbuguabrian)
- Email: chirabrian1@gmail.com
