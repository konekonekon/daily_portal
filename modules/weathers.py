import requests
from api_keys import api_keys


class Weather:

    def __init__(self, w):
        self.datehours = w['dt_txt'].split(":")[0] + "h"
        self.temp = w['main']['temp']
        self.humidity = w['main']['humidity']
        self.main = w['weather'][0]['main']
        self.description = w['weather'][0]['description']
        self.icon = w['weather'][0]['icon']
        self.wind = w['wind']['speed']
        self.clouds = w['clouds']['all']

    # for test, don't used.
    def __str__(self):
        return '{} -> {}°C'.format(self.datehours, self.temp)


city_id = {
    'Paris': 6455259,
    'Tokyo': 1850147,
    'Montreal': 6077243,
}

def get_weatherdata(city):
    # get weather forecast data
    weather_key = api_keys['weather']
    res = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast',
        params = {'id': city_id[city], 'units': 'metric', 'appid': weather_key},
    ).json()
    # suppose a case where the city name is coherent
    assert city == res['city']['name']
    weatherforecast_list = res['list'][:5]
    # weatherforecast_list takes 5 elements by time
    # for each element,
    # Weather(w) creates sevevral objects
    # => return a list of objects, containing 5 elements by time
    # [objects1, objects2,..]
    return [Weather(w) for w in weatherforecast_list]
