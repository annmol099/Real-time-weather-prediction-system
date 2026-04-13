# Weather Forecast API (Flask + Open-Meteo + ML)

A production-style starter Weather API built with **Flask**.  
It accepts a city name, fetches live weather from **Open-Meteo**, and returns a **4-day machine-learning forecast**.

---

## 1) What this project does

This API solves 2 tasks in one response:

1. **Current weather** for a city  
2. **Next 4 days forecast** (predicted by trained ML models)

So frontend apps can call one endpoint (`/predict`) and directly render:
- current conditions
- short-range forecast cards/charts

---

## 2) Core Features

- ✅ City-based query (`/predict?city=Delhi`)
- ✅ Geocoding support (city → latitude/longitude)
- ✅ Live weather fetch from Open-Meteo
- ✅ 4-day predictions using saved model bundle (`model.pkl`)
- ✅ JSON response structure, frontend-friendly
- ✅ CORS enabled (`flask-cors`) for browser apps

---

## 3) Project Structure

```text
weather/
├── api/
│   └── app.py
├── model/
│   └── model.pkl
└── README.md
```

> `app.py` loads model using `../model/model.pkl`.  
> Keep this folder structure unchanged unless you also update the model path in code.

---

## 4) Tech Stack

- **Backend Framework:** Flask
- **CORS:** flask-cors
- **ML loading/inference:** joblib + NumPy
- **Time handling:** pandas
- **HTTP requests:** requests
- **Data provider:** Open-Meteo (Geocoding + Forecast APIs)

---

## 5) How the API works (step-by-step)

When client calls:

```http
GET /predict?city=Mumbai
```

The server executes:

1. **Read query param**
   - `city = request.args.get('city', 'Delhi')`
   - If city missing, default is **Delhi**

2. **Geocoding request**
   - Calls Open-Meteo Geocoding API using city name
   - Gets first result (`count=1`)
   - Extracts:
     - `latitude`
     - `longitude`
     - normalized `name`

3. **Live weather request**
   - Calls Open-Meteo Forecast API with lat/lon
   - Reads:
     - `current_weather` (temperature, windspeed)
     - `hourly` arrays (humidity, pressure, precipitation, cloud cover)

4. **Feature preparation**
   - Builds model input vector with:
     1. humidity  
     2. wind  
     3. pressure  
     4. rain  
     5. cloud  
     6. hour  
     7. day  
     8. month  
     9. dayofweek  
     10. latitude  
     11. longitude  

5. **Prediction loop (4 days)**
   - For `i in range(4)`:
     - predict temperature using `models['temp'][i]`
     - predict humidity using `models['humidity'][i]`
     - predict wind using `models['wind'][i]`
     - predict rain using `models['rain'][i]`

6. **Return JSON**
   - final response includes city, current weather, and forecast list

---

## 6) Requirements

- Python **3.9+**
- pip
- Internet connection (external weather API calls)

Install dependencies:

```bash
pip install flask flask-cors joblib numpy pandas requests
```

---

## 7) Setup on Windows

From project root:

```powershell
cd C:\Users\Avi\Desktop\weather
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install flask flask-cors joblib numpy pandas requests
```

If PowerShell blocks scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

---

## 8) Run the API

```powershell
cd .\api
python .\app.py
```

Default URL:

- `http://127.0.0.1:5000`

---

## 9) API Endpoints

### A) Health Check

**GET** `/`

Used to verify server is running.

**Response**
```json
{
  "message": "Weather API chal rahi hai! ✅"
}
```

---

### B) Predict Weather

**GET** `/predict?city=<CityName>`

**Query parameter**
- `city` (optional)
  - example: `Delhi`, `Mumbai`, `London`
  - default: `Delhi`

**Example**
```http
GET /predict?city=Mumbai
```

---

## 10) Response Schema

### Success Response

```json
{
  "city": "Mumbai",
  "current": {
    "temp": 31.2,
    "humidity": 74,
    "wind": 12.6,
    "pressure": 1004.3,
    "cloud": 65,
    "rain": 0.1
  },
  "forecast": [
    { "day": 1, "temp": 30.4, "humidity": 72.8, "wind": 10.9, "rain": 0.12 },
    { "day": 2, "temp": 29.9, "humidity": 74.1, "wind": 11.2, "rain": 0.08 },
    { "day": 3, "temp": 30.1, "humidity": 73.5, "wind": 10.7, "rain": 0.15 },
    { "day": 4, "temp": 30.0, "humidity": 72.2, "wind": 10.3, "rain": 0.09 }
  ]
}
```

### Error Response (city not found)

```json
{
  "error": "InvalidCity nahi mila!"
}
```

---

## 11) Model Contract (`model.pkl`)

`model.pkl` must be a dictionary-like object with keys:

- `temp`
- `humidity`
- `wind`
- `rain`

Each key should contain **4 models** (index `0..3`) and each model must implement:

```python
predict(features)
```

Expected feature shape in this app:

- `features.shape == (1, 11)`

---

## 12) Quick Testing

### Browser
- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/predict?city=Delhi`

### PowerShell
```powershell
curl "http://127.0.0.1:5000/"
curl "http://127.0.0.1:5000/predict?city=Bengaluru"
```

---

## 13) Known Limitations (current code)

- No timeout in HTTP requests
- No try/except around network errors
- City value is directly interpolated in geocoding URL
- API response keys assumed present (`current_weather`, `hourly`)
- Error responses do not always return proper HTTP status codes

---

## 14) Recommended Improvements

1. Use safer request pattern:
   - `requests.get(url, params=params, timeout=10)`

2. Add robust exception handling:
   - `requests.exceptions.RequestException`
   - key validation before indexing response JSON

3. Return proper HTTP status codes:
   - `400` invalid input
   - `404` city not found
   - `502` provider failure
   - `500` internal error

4. Add project files:
   - `requirements.txt`
   - `.env` for configuration
   - unit tests (Flask test client)

5. Improve logging:
   - replace `print()` with structured logging

---

## 15) Troubleshooting

### `README.md` not found
Create manually:
```powershell
New-Item -Path "C:\Users\Avi\Desktop\weather\README.md" -ItemType File -Force
```

### `model.pkl` not found
Check path:
- `C:\Users\Avi\Desktop\weather\model\model.pkl`

### API not starting on port 5000
Port conflict: change in `app.run(debug=True, port=5000)` to another port.

---

## 16) License

Add a license based on your use case (MIT / Apache-2.0 / proprietary).