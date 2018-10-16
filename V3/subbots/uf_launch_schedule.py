import datetime
import time
import json
import requests

jsonurl = requests.get('https://launchlibrary.net/1.4/launch/next/5')
parsed = json.loads(jsonurl.content.decode('utf8'))


def status_convert(status):
    if status == 1:
        return "Green"
    elif status == 2:
        return "Red"
    elif status == 3:
        return "Success"
    elif status == 4:
        return "Failed"

def get_updates():
    response = ""
    for launch in parsed["launches"]:
        launch_id = launch["id"]
        name = launch["name"]
        window_open = launch["windowstart"]
        window_close = launch["windowend"]
        mission_stauts = status_convert(launch["status"])
        launch_location = launch["location"]["name"]

        response = response + "-=Launch=-\n({}) {}\n-=Window=-\n{} - {}\n-=Location=-\n{}\n-=Status=-\n{}\n\n".format(launch_id, name, window_open, window_close, launch_location, mission_stauts)
    
    return response