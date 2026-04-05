WMO_CONDITIONS = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Icy fog", 51: "Light drizzle", 53: "Drizzle",
    55: "Heavy drizzle", 61: "Light rain", 63: "Rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow", 77: "Snow grains",
    80: "Light showers", 81: "Showers", 82: "Heavy showers",
    85: "Snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm w/ hail", 99: "Thunderstorm w/ heavy hail"
}

def transform_weather(city: dict, raw: dict) -> list[dict]:
    """Transform raw Open-Meteo response into clean rows for the database."""
    daily = raw["daily"]
    rows = []

    for i, date in enumerate(daily["time"]):
        code = daily["weather_code"][i]
        rows.append({
            "city_name":        city["name"],
            "country":          city["country"],
            "latitude":         city["latitude"],
            "longitude":        city["longitude"],
            "timezone":         city["timezone"],
            "date":             date,
            "temp_max_c":       daily["temperature_2m_max"][i],
            "temp_min_c":       daily["temperature_2m_min"][i],
            "precipitation_mm": daily["precipitation_sum"][i],
            "uv_index_max":     daily["uv_index_max"][i],
            "wind_max_kmh":     daily["wind_speed_10m_max"][i],
            "weather_code":     code,
            "condition":        WMO_CONDITIONS.get(code, "Unknown"),
            "sunrise":          daily["sunrise"][i],
            "sunset":           daily["sunset"][i],
        })

    return rows

if __name__ == "__main__":
    from extract import get_coordinates, get_weather

    city = get_coordinates("Manila")
    raw = get_weather(city)
    rows = transform_weather(city, raw)

    print(f"✅ Transformed {len(rows)} rows")
    for row in rows:
        print(f"   {row['date']} | {row['temp_max_c']}°C max | {row['condition']}")