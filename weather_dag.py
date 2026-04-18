from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
from sqlalchemy import create_engine

DB_CONN = "postgresql://postgres:030426Bc@172.26.160.1:5432/weatherdb"

def extract(**context):
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": -1.2921,
		"longitude": 36.8219,
		"current_weather": True
	}
	response = requests.get(url, params=params)
	data = response.json()
	context["ti"].xcom_push(key="weather", value=data["current_weather"])

def transform(**context):
	current = context["ti"].xcom_pull(key="weather", task_ids="extract_weather")
	record = {
		"city": "Nairobi",
		"recorded_at": current["time"],
		"temperature_c": current["temperature"],
		"windspeed_kmh": current["windspeed"],
		"weathercode": current["weathercode"]
	}
	context["ti"].xcom_push(key="record", value=record)

def load(**context):
	record = context["ti"].xcom_pull(key="record", task_ids="transform_weather")
	df = pd.DataFrame([record])
	df["recorded_at"] = pd.to_datetime(df["recorded_at"])
	engine = create_engine(DB_CONN)
	df.to_sql("weather_data", con=engine, if_exists="append", index=False)

default_args = {
	"owner": "brian",
	"retries": 1,
	"retry_delay": timedelta(minutes=5)
}

dag = DAG(
	dag_id="weather_pipeline",
	default_args=default_args,
	description="Hourly Nairobi weather ETL pipeline",
	schedule_interval="@hourly",
	start_date=datetime(2026, 4, 12),
	catchup=False
)

extract_task = PythonOperator(
	task_id="extract_weather",
	python_callable=extract,
	provide_context=True,
	dag=dag
)

transform_task = PythonOperator(
	task_id="transform_weather",
	python_callable=transform,
	provide_context=True,
	dag=dag
)

load_task = PythonOperator(
	task_id="load_weather",
	python_callable=load,
	provide_context=True,
	dag=dag
)

extract_task >> transform_task >> load_task
