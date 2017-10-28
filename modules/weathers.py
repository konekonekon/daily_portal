import requests
from api_keys import api_keys

class WeatherInfo:

    def __init__(self, forecasts):
        weather_info = {}
        for city in ['Paris', 'Tokyo', 'Montreal']:
            weather_info[city] = weather.get_weatherdata(city)
        self.forecasts = forecasts



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
        params = {'id': city_id[city], 'units': 'metric', 'appid': weather_key},
    ).json()
    # suppose a case where the city name is coherent
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
    # return forecastbytime
    return WeatherInfo(forecastbytime)
