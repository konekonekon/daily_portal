from flask import Flask, render_template, send_file
import requests
import modules.times as time
import modules.weathers as weather
import modules.trains as train

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io



app = Flask(__name__)
weather_info = {}


@app.route('/', methods=['GET'])
def index():
    cities = ['Paris', 'Tokyo', 'Montreal']

    # CURRENT TIME
    time_info = {}
    for city in cities:
        time_info[city] = time.get_times(city)

    # WEATHER FORECAST
    # create the same result as above structure
    # {city1 : [objects1, objects2,..]}, {city2 : [objects1, objects2,..]}, ..
    global weather_info
    weather_info = {
        city: weather.get_weatherdata(city)
        for city in cities
    }

    # RATP
    train_info = train.get_traininfo()

    # send to html file
    return render_template(
        'portal.html',
        times = time_info,
        forecasts = weather_info,
        trains = train_info
    )


def generate_png_graph(output):
    global weather_info
    hourlist = []
    templist = []
    humiditylist = []
    windlist = []
    cloudslist = []

    #for city in weather_info:
    #    print(city + ":")
    for f in weather_info["Tokyo"]:
        hourlist.append(f.datehours.split("2017-")[1].split(":")[0] + "h")
        templist.append(f.temp)
        humiditylist.append(f.humidity)
        windlist.append(f.wind)
        cloudslist.append(f.clouds)
        # print(datelist)

    df = pd.DataFrame({'xvalues': hourlist, 'yvalues': templist })
    plt.plot('xvalues', 'yvalues', data=df)
    plt.savefig(output, format='png')


@app.route('/weather.png', methods=['GET'])
def weather_graph():
    global weather_info
    buff = io.BytesIO()
    generate_png_graph(buff)
    buff.seek(0)
    return send_file(buff, mimetype='image/png')


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
