import time
import json
import random
from datetime import datetime

def dt_converter(o):
    if isinstance(o, datetime):
        return o.__str__()


def update_response(bot_type, bot, priority):
    with open('config.json') as json_data:
        json_config = json.load(json_data)
    
    counter = 0
    while counter < 3:
        try:
            updated = False
            for subbot in json_config[bot_type]:
                if subbot["Name"] == bot:
                    subbot["Last Response"] = time.strftime('%Y-%m-%d %H:%M:%S')
                    with open('config.json', 'w') as outputfile:
                        json.dump(json_config, outputfile, indent=4)
                    print("File Updated")
                    updated = True
                    counter = 4
                    break

            if updated is False:
                print("No bot name of [{}] was found in the json.config file")
                counter = 4
                break
        except:
            if priority == "high":
               interval = random.randrange(1, 10, 1)
            elif priority == "medium":
                interval = random.randrange(10, 30, 1)
            elif priority == "low":
                interval = random.randrange(30, 60, 1)
            print("Error occured while updating config.json, waiting {} seconds to try again".format(interval))
            time.sleep(interval)
            counter += 1
    
    if counter == 3:
        print("Failed to write to config.json")
        return