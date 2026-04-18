import pandas as pd
from datetime import datetime

def transform(data: dict, city: str) -> pd.DataFrame:
    print("[Transform] Extracting fields from API response...")
    
    current = data["current_weather"]
    
    record = {
        "city": city,
        "recorded_at": current["time"],
        "temperature_c": current["temperature"],
        "windspeed_kmh": current["windspeed"],
        "weathercode": current["weathercode"]
    }
    
    df = pd.DataFrame([record])
    
    df["recorded_at"] = pd.to_datetime(df["recorded_at"])
    
    print(f"[Transform] Weather record ready: {current['temperature']}°C in {city}")
    return df