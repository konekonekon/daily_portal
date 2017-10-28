import requests
from lxml import html


class TrainInfo:

    def __init__(self, directions, passingtimes_dir1, passingtimes_dir2):
        self.directions = directions
        self.passingtimes_dir1 = passingtimes_dir1
        self.passingtimes_dir2 = passingtimes_dir2


def get_traininfo():
    #https://www.ratp.fr/horaires?networks=rer&line_rer=B&stop_point_rer=Sceaux&type=now&departure_date=25%2F10%2F2017&departure_hour=12&departure_minute=45&op=Rechercher&form_build_id=form-3s9chyTmgWZFUA58gygtM3MiRfgCx1WMrqvDQqAKHfE&form_id=scheduledform
    page = requests.get('https://www.ratp.fr/horaires?networks=rer&line_rer=B&stop_point_rer=Sceaux&type=now&op=Rechercher')
    #page = requests.get('https://www.ratp.fr/horaires?networks=rer&line_rer=B&stop_point_rer=Sceaux&type=now&departure_date=25%2F10%2F2017&departure_hour=13&departure_minute=15&op=Rechercher&form_build_id=form-3s9chyTmgWZFUA58gygtM3MiRfgCx1WMrqvDQqAKHfE&form_id=scheduledform')
    # page = requests.get('https://www.ratp.fr/horaires?networks=rer&line_rer=B&stop_point_rer=Sceaux&type=now&op=Rechercher&form_build_id=form-3s9chyTmgWZFUA58gygtM3MiRfgCx1WMrqvDQqAKHfE&form_id=scheduledform')
    tree = html.fromstring(page.content)
    directions = tree.xpath('//strong[@class="directions"]/text()')
    heurewrap = tree.xpath('//span[@class="heure-wrap"]/text()')
    # remove the current search time
    passingtimes = [h for h in heurewrap if h != heurewrap[0]]
    # remove the first item
    if passingtimes[0] == "Heure de passage":
        passingtimes.remove(passingtimes[0])
    # find intersection of 2 train-directions
    for pt in passingtimes:
        if pt == "Heure de passage":
            index = passingtimes.index(pt)

    passingtimes_dir1 = passingtimes[:index]
    passingtimes_dir2 = passingtimes[index+1:]

    return TrainInfo(directions, passingtimes_dir1, passingtimes_dir2)
