from flask import Flask, jsonify, request
import pickle
import numpy as np
import requests
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Path Fix
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'model', 'model.pkl')
LE_PATH = os.path.join(BASE_DIR, '..', 'model', 'label_encoder.pkl')

# Models Load Karo
with open(MODEL_PATH, 'rb') as f:
    models = pickle.load(f)

with open(LE_PATH, 'rb') as f:
    le = pickle.load(f)

print("Models loaded! ✅")

@app.route('/')
def home():
    return jsonify({"message": "Weather API chal rahi hai! ✅"})

@app.route('/predict', methods=['GET'])
def predict():
    city = request.args.get('city', 'Delhi')

    # GeoCoding
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    geo_data = requests.get(geo_url).json()

    if not geo_data.get("results"):
        return jsonify({"error": f"{city} nahi mila!"})

    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]
    city_name = geo_data["results"][0]["name"]

    # Live Data Fetch
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": ["relative_humidity_2m", "pressure_msl",
                   "precipitation", "cloudcover"],
        "timezone": "Asia/Kolkata",
        "forecast_days": 1
    }
    data = requests.get(url, params=params).json()

    current = data["current_weather"]
    hourly = data["hourly"]

    humidity = hourly["relative_humidity_2m"][0]
    wind = current["windspeed"]
    pressure = hourly["pressure_msl"][0]
    rain = hourly["precipitation"][0]
    cloud = hourly["cloudcover"][0]
    temp = current["temperature"]
    now = pd.Timestamp.now()

    # City Encode
    try:
        city_encoded = le.transform([city_name])[0]
    except:
        city_encoded = 0

    # Features — naye order ke saath
    features = np.array([[
        city_encoded,
        temp,
        humidity,
        wind,
        cloud,
        rain,
        now.month,
        now.day,
        pressure,
        now.hour,
        now.dayofweek,
        lat,
        lon
    ]])

    # 4 Din Ka Forecast
    forecast = []
    for i in range(4):
        day_pred = {
            "day": i + 1,
            "temp": round(float(models['temp'][i].predict(features)[0]), 1),
            "humidity": round(float(models['humidity'][i].predict(features)[0]), 1),
            "wind": round(float(models['wind'][i].predict(features)[0]), 1),
            "rain": max(0, round(float(models['rain'][i].predict(features)[0]), 2)),        }
        forecast.append(day_pred)

    return jsonify({
        "city": city_name,
        "current": {
            "temp": temp,
            "humidity": humidity,
            "wind": wind,
            "pressure": pressure,
            "cloud": cloud,
            "rain": rain
        },
        "forecast": forecast
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)