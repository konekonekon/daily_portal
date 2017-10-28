import arrow

city_code = {
    'Paris': 'Europe/Paris',
    'Tokyo': 'Asia/Tokyo',
    'Montreal': 'Canada/Eastern',
}

def get_times(c):
    return arrow.now(city_code[c]).format('dddd, MMMM Do YYYY, HH:mm')
