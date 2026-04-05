from extract import get_coordinates, get_weather
from transform import transform_weather
from load import get_connection, upsert_city, upsert_weather
from datetime import datetime

def run_pipeline(city_name: str):
    print(f"\n🌤  Nimbus Pipeline --- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   City: {city_name}")

    city = get_coordinates(city_name)
    print(f"📍 Geocoded: {city['name']}, {city['country']}")

    raw = get_weather(city)
    print(f"📡 Fetched {len(raw['daily']['time'])} days of weather data")

    rows = transform_weather(city, raw)
    print(f"🔄 Transformed {len(rows)} rows")

    con = get_connection()
    city_id = upsert_city(con, rows[0])
    inserted = upsert_weather(con, city_id, rows)
    con.close()

    print(f"💾 Loaded {inserted} new rows (city_id: {city_id})")
    print(f"✅ Pipeline complete!\n")

if __name__ == "__main__":
    cities = ["Manila", "Tokyo", "London"]
    for city in cities:
        run_pipeline(city)