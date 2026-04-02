# ☁️ Nimbus: AI-Powered Weather Intelligence

Nimbus is a full-stack data project that turns raw weather data into clear, useful insights.

Instead of just showing forecasts, it analyzes real conditions and gives practical recommendations people can actually use—like when to bring an umbrella or avoid going out due to heat and humidity.

I built this to practice real-world data engineering: collecting data, storing it efficiently, and turning it into something meaningful with a clean UI.

---

## 🚀 Tech Stack

| Layer       | Technology              | Why I Used It |
|------------|------------------------|--------------|
| Frontend   | Next.js (App Router)   | Fast, modern React framework |
| Styling    | Tailwind CSS           | Easy custom UI styling |
| Language   | TypeScript             | Safer data handling |
| Backend    | Python (Pandas)        | Data processing and cleaning |
| Database   | DuckDB                 | Lightweight and fast for analytics |
| AI         | Claude API             | Generate simple weather advice |

---

## 🛠️ What It Does

### 🔄 Data Pipeline
- Fetches weather data from the Open-Meteo API  
- Cleans and organizes it using Python (Pandas)  
- Stores it locally using DuckDB  

### 🗄️ Data Storage
- Uses DuckDB to store historical weather data  
- Lets me query data quickly using SQL  

### 🤖 AI Insights
- Analyzes current weather conditions  
- Generates simple recommendations like:  
  > "High humidity today — drink more water and avoid midday heat."  

### 🎨 Dashboard
- Clean and responsive UI  
- Displays weather data in charts and summaries  
- Built with Next.js and Tailwind  

---

## 📂 Project Structure
nimbus/
├── dashboard/
├── data/
├── database/
├── notebooks/
├── pipeline/
├── venv/
├── .gitignore
├── README.md
├── requirements.txt
