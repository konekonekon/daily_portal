from flask import Flask, render_template
import modules.times as time
import modules.weathers as weather
import modules.trains as train

app = Flask(__name__)


# @app.route('/weather.png', methods=['GET'])
# def weather_graph():
#     response = flask.response(content_type='image/png')
#     response.body = generate_png_graph()
#     return response


@app.route('/', methods=['GET'])
def index():
    # CURRENT TIME
    frtime = time.get_francetime()
    jptime = time.get_jptime()
    qctime = time.get_quebectime()

    # WEATHER FORECAST
    forecasts = {}
    for city in ['Paris', 'Tokyo', 'Montreal']:
        forecasts[city] = weather.get_weatherdata(city)

    # RATP
    trains = train.get_traininfo()


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
