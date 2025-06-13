import os
from datetime import datetime
from flask import Flask, jsonify, render_template
import requests
from dotenv import load_dotenv

load_dotenv()  # reads .env

OWM_KEY = os.getenv("OWM_API_KEY")
LAT     = os.getenv("LAT")
LONG    = os.getenv("LONG")
UNIT    = os.getenv("UNIT", "imperial")

app = Flask(__name__)

def get_time_date():
    now = datetime.now()
    return {
        # “12 June 2025”
        "date": now.strftime("%-d %B %Y"),
        # “Thursday”
        "day": now.strftime("%A"),
        # “4:18 PM”
        "time": now.strftime("%-I:%M %p")
    }

def get_weather():
    url = (
        "https://api.openweathermap.org/data/2.5/weather?"
        f"lat={LAT}&lon={LONG}&units={UNIT}&appid={OWM_KEY}"
    )
    print(f"[DEBUG] Requesting URL: {url}")
    resp = requests.get(url)
    print(f"[DEBUG] Status: {resp.status_code}, Body: {resp.text[:100]}")
    resp.raise_for_status()
    j = resp.json()
    print(f"[DEBUG] JSON keys: {list(j.keys())}")
    return {
        "temp": round(j["main"]["temp"]),            # integer degrees
        "desc": j["weather"][0]["description"].title()
    }

@app.route("/")
def index():
    # initial render – the JS will pull fresh JSON from /api/data
    return render_template("index.html")

@app.route("/api/data")
def api_data():
    return jsonify({
        **get_time_date(),
        **get_weather()
    })

if __name__ == "__main__":
    # debug=True only for local tinkering
    app.run(host="0.0.0.0", port=5001, debug=True)
