import arrow

class TimeInfo:

    def __init__(self, city_time):
        self.city_time = city_time


city_code = {
    'Paris': 'Europe/Paris',
    'Tokyo': 'Asia/Tokyo',
    'Montreal': 'Canada/Eastern',
}

def get_times(c):
    return TimeInfo(arrow.now(city_code[c]).format('dddd, MMMM Do YYYY, HH:mm'))
