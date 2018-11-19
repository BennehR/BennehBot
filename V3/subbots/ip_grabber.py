import json
import time
#from config_update_retry import update_response
from config_update_retry import update_response
from requests import get
import subprocess
import logging

with open('config.json') as json_data:
    JSONConfig = json.load(json_data)

logging.basicConfig(filename='logs/IPGrabber.log', level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
current_ip = get('https://api.ipify.org').text
existing_ip = JSONConfig["Variables"]["IP"]

def get_ip():
    if current_ip is not existing_ip:
        counter = 0
        while counter < 3:
            counter += 1
            try:
                JSONConfig["Variables"]["IP"] = current_ip
                with open('subbots.config.json', 'w') as outputfile:
                    json.dump(JSONConfig, outputfile, indent=4)
            except:
                time.sleep(10)
                pass

    return current_ip

def get_state():
    with open('config.json') as json_data:
        JSONConfig = json.load(json_data)

    for subbot in JSONConfig["Independant SubBots"]:
        if subbot["Name"] == "IP_Grabber":
            state = subbot["Enabled"]
            print(state)
            return state

def set_enabled():
    counter = 0
    while counter < 3:
        counter += 1
        try:
            JSONConfig["Independant SubBots"]["IP_Grabber"]["Enabled"] = "True"
            with open('config.json', 'w') as outputfile:
                json.dump(JSONConfig, outputfile, indent=4)
                counter = 3
                subprocess.call("screen -S IP_Grabber_Loop bash -c 'python3 ip_grabber.py'") 
        except:
            time.sleep(10)
            counter += 1
            pass

def set_disabled():
    counter = 0
    while counter < 3:
        counter += 1
        try:
            JSONConfig["Independant SubBots"]["IP_Grabber"]["Enabled"] = "False"
            with open('config.json', 'w') as outputfile:
                json.dump(JSONConfig, outputfile, indent=4)
                counter = 3
        except:
            time.sleep(10)
            counter += 1
            pass

def begin_loop():
    while get_state() == "True":
        get_ip()
        update_response("Independant SubBots", "IP_Grabber", "high")
        time.sleep(3600)
        print("IP Looped")

    print("IP Grabber has been identified as Disabled, loop exiting.")

if __name__ == "__main__":
    begin_loop()