from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

user_api = '830b0e8b4f82f745aedd716a190e46ae'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        location = request.form['city']
        complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={user_api}"
        api_link = requests.get(complete_api_link)
        api_data = api_link.json()

        if api_data['cod'] == 404:
            error = f"Invalid city: {location}, please try again."
        else:
            temp_city = api_data['main']['temp'] - 273.15
            weather_desc = api_data['weather'][0]['description']
            hmdt = api_data['main']['humidity']
            wind_spd = api_data['wind']['speed'] * 3.6
            date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

            weather_data = {
                "city": location.upper(),
                "temp": f"{temp_city:.2f} °C",
                "desc": weather_desc.title(),
                "humidity": f"{hmdt}%",
                "wind": f"{wind_spd:.2f} km/h",
                "date_time": date_time
            }

    return render_template("index.html", weather=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
