import requests

def extract(lat: float, lon: float) -> dict:
    print(f"[Extract] Calling weather API for coordinates: {lat}, {lon}")
    
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API call failed with status code: {response.status_code}")
    
    data = response.json()
    print(f"[Extract] API call successful")
    return data