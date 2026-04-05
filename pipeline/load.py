import duckdb
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    token = os.getenv("MOTHERDUCK_TOKEN")
    con = duckdb.connect(f"md:nimbus?motherduck_token={token}")
    return con

def upsert_city(con, row: dict) -> int:
    """Insert city if it doesn't exist, return its id."""
    con.execute("""
        INSERT INTO cities (id, name, country, latitude, longitude, timezone)
        SELECT
            COALESCE((SELECT MAX(id) FROM cities), 0) + 1,
            ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM cities WHERE name = ? AND country = ?
        )
    """, [
        row["city_name"], row["country"], row["latitude"], row["longitude"], row["timezone"],
        row["city_name"], row["country"]
    ])

    result = con.execute(
        "SELECT id FROM cities WHERE name = ? AND country = ?",
        [row["city_name"], row["country"]]
    ).fetchone()

    return result[0]

def upsert_weather(con, city_id: int, rows: list[dict]):
    """Insert weather rows, skipping duplicates on city_id + date."""
    inserted = 0
    for row in rows:
        existing = con.execute(
            "SELECT 1 FROM daily_weather WHERE city_id = ? AND date = ?",
            [city_id, row["date"]]
        ).fetchone()

        if not existing:
            next_id = con.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM daily_weather").fetchone()[0]
            con.execute("""
                INSERT INTO daily_weather
                    (id, city_id, date, temp_max_c, temp_min_c, precipitation_mm,
                     uv_index_max, wind_max_kmh, weather_code, condition, sunrise, sunset)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                next_id, city_id, row["date"], row["temp_max_c"], row["temp_min_c"],
                row["precipitation_mm"], row["uv_index_max"], row["wind_max_kmh"],
                row["weather_code"], row["condition"], row["sunrise"], row["sunset"]
            ])
            inserted += 1

    return inserted

if __name__ == "__main__":
    from extract import get_coordinates, get_weather
    from transform import transform_weather

    city = get_coordinates("Manila")
    raw = get_weather(city)
    rows = transform_weather(city, raw)

    con = get_connection()
    city_id = upsert_city(con, rows[0])
    inserted = upsert_weather(con, city_id, rows)
    con.close()

    print(f"✅ City id: {city_id}")
    print(f"✅ Inserted {inserted} new rows into MotherDuck")