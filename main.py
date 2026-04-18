import os
from dotenv import load_dotenv
from src.extract import extract
from src.transform import transform
from src.load import load

load_dotenv()

CITY    = "Nairobi"
LAT     = -1.2921
LON     = 36.8219
DB_CONN = os.getenv("DATABASE_URL")

if __name__ == "__main__":
    data = extract(LAT, LON)
    df   = transform(data, CITY)
    load(df, DB_CONN)
    print("Pipeline complete!")