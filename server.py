from flask import Flask, render_template
import arrow
import requests
import json
from api_keys import api_keys
from lxml import html

app = Flask(__name__)


def get_francetime():
    return arrow.now('Europe/Paris').format('dddd, MMMM Do YYYY, HH:mm')

def get_jptime():
    return arrow.now('Asia/Tokyo').format('dddd, MMMM Do YYYY, HH:mm')

def get_quebectime():
    return arrow.now('Canada/Eastern').format('dddd, MMMM Do YYYY, HH:mm')


city_id = {
    'Paris': 6455259,
    'Tokyo': 1850147,
    'Montreal': 6077243,
}


def get_weatherdatalist(city):
    # get weather forecast data
    weather_key = api_keys['weather']
    res = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast',
        params={'id': city_id[city], 'units': 'metric', 'appid': weather_key},
    ).json()
    assert city == res['city']['name']
    weatherforecast_list = res['list'][:5]
    return weatherforecast_list

def get_weatherdata(city):
    forecastbytime = {}
    for w in get_weatherdatalist(city):
        temp = w['main']['temp']
        humidity = w['main']['humidity']
        main = w['weather'][0]['main']
        description = w['weather'][0]['description']
        icon = w['weather'][0]['icon']
        wind = w['wind']['speed']
        clouds = w['clouds']['all']
        datehours = w['dt_txt']
        forecastbytime[datehours] = {
            'temp' : temp,
            'humidity' : humidity,
            'weather' : main,
            'description' : description,
            'icon' : icon,
            'wind' : wind,
            'clouds' : clouds
        }
    return forecastbytime


class TrainInfo:
    def __init__(self, directions, heures_passage, heures_wrap):
        self.directions = directions
        self.heures_passage = heures_passage
        self.heures_wrap = heures_wrap


def get_traininfo():
    #https://www.ratp.fr/horaires?networks=rer&line_rer=B&stop_point_rer=Sceaux&type=now&departure_date=25%2F10%2F2017&departure_hour=12&departure_minute=45&op=Rechercher&form_build_id=form-3s9chyTmgWZFUA58gygtM3MiRfgCx1WMrqvDQqAKHfE&form_id=scheduledform
    #page = requests.get('https://www.ratp.fr/horaires?networks=rer&line_rer=B&stop_point_rer=Sceaux&type=now&op=Rechercher')
    #page = requests.get('https://www.ratp.fr/horaires?networks=rer&line_rer=B&stop_point_rer=Sceaux&type=now&departure_date=25%2F10%2F2017&departure_hour=13&departure_minute=15&op=Rechercher&form_build_id=form-3s9chyTmgWZFUA58gygtM3MiRfgCx1WMrqvDQqAKHfE&form_id=scheduledform')
    page = requests.get('https://www.ratp.fr/horaires?networks=rer&line_rer=B&stop_point_rer=Sceaux&type=now&op=Rechercher&form_build_id=form-3s9chyTmgWZFUA58gygtM3MiRfgCx1WMrqvDQqAKHfE&form_id=scheduledform')
    tree = html.fromstring(page.content)
    directions = tree.xpath('//strong[@class="directions"]/text()')
    heurewrap = tree.xpath('//span[@class="heure-wrap"]/text()')
    # remove the current search time
    passingtime = [h for h in heurewrap if h != heurewrap[0]]
    # remove the first item
    if passingtime[0] == "Heure de passage":
        passingtime.remove(passingtime[0])
    #return passingtime, heurewrap, directions
    return TrainInfo(directions, passingtime, heurewrap)


# @app.route('/weather.png', methods=['GET'])
# def weather_graph():
#     response = flask.response(content_type='image/png')
#     response.body = generate_png_graph()
#     return response


@app.route('/', methods=['GET'])
def index():
    # CURRENT TIME
    frtime = get_francetime()
    jptime = get_jptime()
    qctime = get_quebectime()

    # WEATHER FORECAST
    forecasts = {}
    for city in ['Paris', 'Tokyo', 'Montreal']:
        forecasts[city] = get_weatherdata(city)

    # RATP
    trains = get_traininfo()


    return render_template('portal.html',
    #         time=time_info,
    #         weather=weather_info,
    #         trains=trains_info,
    # )

            ftime=frtime, jtime=jptime, qtime=qctime,

            wforecasts=forecasts,

            #horaire=heures,
            trains=trains
            )



if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
