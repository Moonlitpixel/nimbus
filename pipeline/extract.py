import requests
import pandas as pd
import duckdb
from datetime import datetime

def run_pipeline():
    # 1. SETTINGS
    DB_PATH = "database/nimbus_data.db"
    LAT, LON = 14.5995, 120.9842 # Manila
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LAT,
        "longitude": LON,
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
        "timezone": "Asia/Singapore"
    }

    # 2. EXTRACT
    print(f"--- Fetching Weather for Manila ({datetime.now().strftime('%H:%M:%S')}) ---")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()['current']
        df = pd.DataFrame([data])
        df['timestamp'] = datetime.now()
        
        # 3. LOAD (DuckDB)
        # This connects to the file and creates a table if it doesn't exist
        con = duckdb.connect(DB_PATH)
        con.execute("CREATE TABLE IF NOT EXISTS weather_history AS SELECT * FROM df WHERE 1=0")
        con.execute("INSERT INTO weather_history SELECT * FROM df")
        
        # Check if it worked
        row_count = con.execute("SELECT COUNT(*) FROM weather_history").fetchone()[0]
        con.close()
        
        print(f"✅ Success! Database now has {row_count} total records.")
        return df
    else:
        print(f"❌ API Error: {response.status_code}")
        return None

if __name__ == "__main__":
    run_pipeline()