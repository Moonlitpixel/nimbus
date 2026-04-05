import requests

def get_coordinates(city_name: str) -> dict:
    """Geocode a city name to lat/lon using Open-Meteo's free geocoding API."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    
    response = requests.get(url, params=params)
    results = response.json().get("results")
    
    if not results:
        raise ValueError(f"City not found: {city_name}")
    
    result = results[0]
    return {
        "name": result["name"],
        "country": result["country"],
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "timezone": result["timezone"]
    }

def get_weather(city: dict) -> dict:
    """Fetch 7-day daily forecast from Open-Meteo for a given city."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "daily": [
            "temperature_2m_max", "temperature_2m_min",
            "precipitation_sum", "uv_index_max",
            "wind_speed_10m_max", "weather_code",
            "sunrise", "sunset"
        ],
        "timezone": city["timezone"],
        "forecast_days": 7
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise ConnectionError(f"Weather API error: {response.status_code}")
    
    return response.json()

if __name__ == "__main__":
    city = get_coordinates("Manila")
    print(f"📍 Found: {city['name']}, {city['country']}")
    
    weather = get_weather(city)
    print(f"✅ Got {len(weather['daily']['time'])} days of weather data")
    print(f"   Dates: {weather['daily']['time'][0]} → {weather['daily']['time'][-1]}")