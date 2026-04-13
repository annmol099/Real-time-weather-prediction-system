from flask import Flask, jsonify, request
import joblib
import numpy as np
import requests
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Models Load Karo
models = joblib.load("../model/model.pkl")
print("Models loaded! ✅")

@app.route('/')
def home():
    return jsonify({"message": "Weather API chal rahi hai! ✅"})

@app.route('/predict', methods=['GET'])
def predict():
    city = request.args.get('city', 'Delhi')

    # GeoCoding — koi bhi city
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

    features = np.array([[
        humidity, wind, pressure, rain, cloud,
        now.hour, now.day, now.month, now.dayofweek,
        lat, lon
    ]])

    # Forecast Predict Karo 4 din ka
    forecast = []
    for i in range(4):
        day_pred = {
            "day": i + 1,
            "temp": round(float(models['temp'][i].predict(features)[0]), 1),
            "humidity": round(float(models['humidity'][i].predict(features)[0]), 1),
            "wind": round(float(models['wind'][i].predict(features)[0]), 1),
            "rain": round(float(models['rain'][i].predict(features)[0]), 2),
        }
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
    app.run(debug=True, port=5000)