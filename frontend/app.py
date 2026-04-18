from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

API_URL = "http://127.0.0.1:5000/predict"

def get_day_name(date):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
            'Friday', 'Saturday', 'Sunday']
    return days[date.weekday()]

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    error = None
    city = ''

    if request.method == 'POST':
        city = request.form.get('city', '').strip()
    else:
        city = request.args.get('city', '').strip()

    if city:
        try:
            response = requests.get(f"{API_URL}?city={city}", timeout=10)
            result = response.json()
            
            if 'error' in result:
                error = result['error']
            else:
                data = result
                today = datetime.now()
                for i, day in enumerate(data['forecast']):
                    future = today + timedelta(days=i+1)
                    day['day_name'] = get_day_name(future)
                    day['date'] = future.strftime("%d %b")
                    
        except Exception as e:
            error = str(e)

    return render_template('index.html', data=data, error=error, city=city)

if __name__ == '__main__':
    app.run(debug=True, port=8080)