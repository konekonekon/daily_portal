from flask import Flask, render_template
import requests
import modules.times as time
import modules.weathers as weather
import modules.trains as train

import matplotlib.pyplot as plt
import numpy as np
# import seaborn as sns
import pandas as pd
import io
from flask import send_file


app = Flask(__name__)


def generate_png_graph(output):
    df=pd.DataFrame({'xvalues': range(1,101), 'yvalues': np.random.randn(100) })
    # plot
    plt.plot('xvalues', 'yvalues', data=df)
    plt.savefig(output, format='png')

@app.route('/weather.png', methods=['GET'])
def weather_graph():
    buff = io.BytesIO()
    generate_png_graph(buff)
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
