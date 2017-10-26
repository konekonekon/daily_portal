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

# def get_citiesweatherdata():
#     weather_key = api_keys['weather']
#     r = requests.get(
#         'http://api.openweathermap.org/data/2.5/group?id=6455259,1850147,6077243&units=metric&appid=' + weather_key
#     )
#     paris_weather = json.loads(r.text)['list'][0]
#     tokyo_weather = json.loads(r.text)['list'][1]
#     montreal_weather = json.loads(r.text)['list'][-1]
# 
#     return paris_weather, tokyo_weather, montreal_weather
#
# def parse_weatherdata(wdata):
#     main = wdata['weather'][0]['main']
#     description = wdata['weather'][0]['description']
#     icon = wdata['weather'][0]['icon']
#     temp = wdata['main']['temp']
#     humidity = wdata['main']['humidity']
#     wind = wdata['wind']['speed']
#     clouds = wdata['clouds']['all']
#     name = wdata['name']
#     return { 'Cityname':name,
#         'Weather':main, 'Description':description, 'Icon':icon,
#         'Temperature':temp, 'Humidity':humidity, 'Wind':wind, 'Clouds':clouds }


def get_weatherdatalist(c):
    # get cityID
    if c == 'Paris':
        cid = '6455259'
    elif c == 'Tokyo':
        cid = '1850147'
    elif c == 'Montreal':
        cid = '6077243'

    # get weather forecast data
    weather_key = api_keys['weather']
    res = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast?id=' + cid + '&units=metric&appid=' + weather_key
    )
    if c == json.loads(res.text)['city']['name']:
        weatherforecast_list = json.loads(res.text)['list'][:5]
    return weatherforecast_list

def parse_weatherdata2(city):
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
    return passingtime, heurewrap, directions


@app.route('/', methods=['GET'])
def index():
    # CURRENT TIME
    frtime = get_francetime()
    jptime = get_jptime()
    qctime = get_quebectime()

    # WEATHER
    # CURRENT
    # dict_weatherdata = list()
    # for databycity in get_citiesweatherdata():
    #     dict_weatherdata.append(parse_weatherdata(databycity))

    # FORECAST
    forecasts = {}
    for city in ['Paris', 'Tokyo', 'Montreal']:
        forecasts[city] = parse_weatherdata2(city)

    # RATP
    passtimes, heures, direcs = get_traininfo()


    return render_template('portal.html',
            ftime=frtime, jtime=jptime, qtime=qctime,

            # content=get_citiesweatherdata(),
            # weatherdata=dict_weatherdata,
            wforecasts=forecasts,

            #horaire=heures,
            dirs=direcs, ptimes=passtimes
            )



if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
