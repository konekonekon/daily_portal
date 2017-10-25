from flask import Flask, render_template
import arrow
import requests
import json
from api_keys import api_keys

app = Flask(__name__)


def get_francetime():
    return arrow.now('Europe/Paris').format('dddd, MMMM Do YYYY, H:m')

def get_jptime():
    return arrow.now('Asia/Tokyo').format('dddd, MMMM Do YYYY, H:m')

def get_quebectime():
    return arrow.now('Canada/Eastern').format('dddd, MMMM Do YYYY, H:m')

def get_citiesweatherdata():
    weather_key = api_keys['weather']
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/group?id=6455259,1850147,6077243&units=metric&appid=' + weather_key
    )
    paris_weather = json.loads(r.text)['list'][0]
    tokyo_weather = json.loads(r.text)['list'][1]
    montreal_weather = json.loads(r.text)['list'][-1]

    return paris_weather, tokyo_weather, montreal_weather

def parse_weatherdata(wdata):
    main = wdata['weather'][0]['main']
    description = wdata['weather'][0]['description']
    icon = wdata['weather'][0]['icon']
    temp = wdata['main']['temp']
    humidity = wdata['main']['humidity']
    wind = wdata['wind']['speed']
    clouds = wdata['clouds']['all']
    name = wdata['name']
    return { 'Cityname':name,
        'Weather':main, 'Description':description, 'Icon':icon,
        'Temperature':temp, 'Humidity':humidity, 'Wind':wind, 'Clouds':clouds }


@app.route('/', methods=['GET'])
def index():
    #time
    frtime = get_francetime()
    jptime = get_jptime()
    qctime = get_quebectime()

    #weather
    dict_weatherdata = list()
    for databycity in get_citiesweatherdata():
        dict_weatherdata.append(parse_weatherdata(databycity))

    #ratp
    # response = requests.get(
    #     'https://www.ratp.fr/horaires?networks=rer&line_rer=B&line_busratp=&name_line_busratp=&id_line_busratp=&line_noctilien=&name_line_noctilien=&id_line_noctilien=&stop_point_rer=Sceaux&type=now&departure_date=24%2F10%2F2017&departure_hour=22&departure_minute=50&op=Rechercher&form_build_id=form-nkSV0Xj6ef_xE5T7QuSX4yf6OqJaExtJxRMrbKQspqc&form_id=scheduledform'
    # )
    # ratp_response = json.loads(response.text)


    return render_template('portal.html',
            ftime=frtime, jtime=jptime, qtime=qctime,
            # content=get_citiesweatherdata(),
            weatherdata=dict_weatherdata,
            # ratp=ratp_response
            )



if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
