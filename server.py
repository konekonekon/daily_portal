# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_file, request
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


def generate_png_graph(output, cn):
    global weather_info
    hourlist = []
    templist = []
    humiditylist = []
    cloudslist = []

    for f in weather_info[cn]:
        hourlist.append(f.datehours.split("2017-")[1].split(":")[0] + "h")
        templist.append(f.temp)
        humiditylist.append(f.humidity)
        cloudslist.append(f.clouds)

    plt.figure(1)
    #temperature
    plt.subplot(311)
    df = pd.DataFrame({'xvalues': hourlist, 'yvalues': templist })
    plt.plot('xvalues', 'yvalues', data=df, color='red', alpha=0.3, linestyle='-', linewidth=3)
    plt.ylabel('°C')
    plt.title("Temperature")
    #clouds
    plt.subplot(312)
    df3 = pd.DataFrame({'xvalues3': hourlist, 'yvalues3': cloudslist })
    plt.plot('xvalues3', 'yvalues3', data=df3, color='green', alpha=0.5, linestyle='-', linewidth=3)
    plt.ylabel('%')
    plt.title("Clouds")
    #humidity
    plt.subplot(313)
    df2 = pd.DataFrame({'xvalues2': hourlist, 'yvalues2': humiditylist })
    plt.plot('xvalues2', 'yvalues2', data=df2, color='skyblue', linestyle='-', linewidth=3)
    plt.ylabel('%')
    plt.text(hourlist[1], max(humiditylist)-5, 'Humidity',
        verticalalignment='center', horizontalalignment='left',
        color='green', fontsize=15)
    plt.title("Humidity")

    plt.tight_layout()
    plt.savefig(output, format='png')
    plt.close()


@app.route('/weather.png', methods=['GET'])
def weather_graph():
    global weather_info
    buff = io.BytesIO()
    cityname = request.args["city"]
    generate_png_graph(buff, cityname)
    buff.seek(0)
    return send_file(buff, mimetype='image/png')


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


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
