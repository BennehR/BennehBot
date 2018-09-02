import json
import time
from requests import get

with open('config.json') as json_data:
    JSONConfig = json.load(json_data)

current_ip = get('https://api.ipify.org').text
existing_ip = JSONConfig["Variables"]["IP"]

def get_ip():
    if current_ip is not existing_ip:
        counter = 0
        while counter < 3:
            counter += 1
            try:
                JSONConfig["Variables"]["IP"] = current_ip
                with open('config.json', 'w') as outputfile:
                    json.dump(JSONConfig, outputfile, indent=4)
            except:
                time.sleep(10)
                pass

    return current_ip