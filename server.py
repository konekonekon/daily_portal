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
    cities = ['Paris', 'Tokyo', 'Montreal']

    # CURRENT TIME
    time_info = {}
    for city in cities:
        time_info[city] = time.get_times(city)

    # WEATHER FORECAST
    weather_info = {}
    for city in cities:
        weather_info[city] = weather.get_weatherdata(city)

    # RATP
    train_info = train.get_traininfo()

    return render_template(
        'portal.html',
        times = time_info,
        forecasts = weather_info,
        trains = train_info
    )

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
