from flask import Flask, json
import requests
from datetime import datetime

app = Flask(__name__)


URL = 'http://api.openweathermap.org/data/2.5/forecast?q=London,uk&APPID=c00adc1c9fdee3f71ac15c8fd947ea30'


@app.route('/weather/london/<date>/<time>/', methods=['GET'])
@app.route('/weather/london/<date>/<time>/<category>/', methods=['GET'])
def get_weather(date, time, category=None):
    """ Both endpoints map over the same function for simplicity.
    It formats the date & time then gets the data from openweather api.
    Parses json for the forcast and then builds the appropriate response."""
    format_date = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
    format_time = datetime.strptime(time, '%H%M%S').strftime('%H:%M:%S')
    target_date = format_date + " " + format_time

    response = requests.get(URL)

    if response.status_code == 200:
        json_data = response.json()

        forecast = [f for f in json_data['list'] if f['dt_txt'] == target_date]

        if forecast:
            forecast = forecast[0]
            description = forecast['weather'][0]['description']
            temperature = int(round(forecast['main']['temp'] - 273.15))
            temperature = str(temperature) + 'C'
            humidity = str(forecast['main']['humidity'])+'%'
            pressure = str(forecast['main']['pressure'])

            response_data = {'description': description, 'temperature': temperature,
                        'humidity': humidity, 'pressure': pressure}
        else:
            message = 'No data for ' + target_date
            response_data = {'status': 'error', 'message': message}

        if category:
            category_data = {k: v for k, v in response_data.iteritems() if k == category}
            response_data = category_data

    else:
        response_data = {'status': 'error', 'message': 'Could not obtain data from api'}

    return json.dumps(response_data)


if __name__ == '__main__':
    app.run(debug=True)
