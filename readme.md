# ☁️ Nimbus: AI-Powered Weather Intelligence

Nimbus is a full-stack data project that turns raw weather data into clear, useful insights.

Instead of just showing forecasts, it analyzes real conditions and gives practical recommendations people can actually use—like when to bring an umbrella or avoid going out due to heat and humidity.

I built this to practice real-world data engineering: collecting data, storing it efficiently, and turning it into something meaningful with a clean UI.

---
## 🚀 Tech Stack

| Layer       | Technology                  | Why I Used It                                      |
|------------|-----------------------------|----------------------------------------------------|
| Frontend   | Next.js 14 + TypeScript     | App Router, SSR, secure API routes                 |
| Styling    | Tailwind CSS                | Utility-first responsive design with dark mode     |
| Charts     | Recharts                    | Temperature trends and analytics visualizations    |
| Pipeline   | Python + Pandas             | ETL — extract, transform, load weather data        |
| Database   | MotherDuck (cloud DuckDB)   | Cloud-hosted, queryable from pipeline and frontend |
| AI         | Google Gemini (RAG pattern) | Fact-grounded insights and natural language chat   |
| Data Source| Open-Meteo API              | Free weather + geocoding API, no key required      |

---

## 🛠️ What It Does

### 🔄 Data Pipeline
- Geocodes any city name worldwide to coordinates via Open-Meteo's geocoding API
- Fetches 7-day daily forecasts including temperature, precipitation, UV index, wind, and weather codes
- Cleans and normalizes raw JSON using Python and Pandas
- Loads data into MotherDuck using a relational 2-table schema with upsert logic — no duplicates

### 🗄️ Data Storage
- **MotherDuck** (cloud DuckDB) — data persists and is accessible from both the pipeline and the frontend
- **Relational schema** — `cities` dimension table + `daily_weather` fact table linked by foreign key
- Pipeline is idempotent — running it twice on the same day produces zero duplicate rows

### 🤖 AI Insights
- Uses the **RAG pattern** — Gemini reads a live weather snapshot before every response
- Generates smart daily briefings grounded in real data
- Supports natural language chat with full conversation memory
- Streaming responses rendered word-by-word in real time

### 🎨 Dashboard
- Search any city — geocodes, fetches, and re-renders everything dynamically
- Live weather card, condition stats, hourly chart, 5-day forecast
- Analytics strip: 7-day averages, rainy day count, peak UV
- Dark mode, responsive layout, live clock
- Secure API routes keep MotherDuck and Gemini keys off the client

---

## 📂 Project Structure

```
nimbus/
├── dashboard/          # Next.js 14 + TypeScript frontend
├── data/               # Raw and processed data
├── database/           # Local DuckDB files (dev only)
├── notebooks/          # Data science analysis scripts
├── pipeline/
│   ├── extract.py      # Geocode city + fetch weather from Open-Meteo
│   ├── transform.py    # Clean, normalize, map weather codes
│   ├── load.py         # Upsert into MotherDuck (cities + daily_weather)
│   └── orchestrate.py  # Run full ETL pipeline end-to-end
├── venv/               # Python environment (ignored in Git)
├── .env                # Secret tokens (ignored in Git)
├── .gitignore
├── README.md
└── requirements.txt
```

