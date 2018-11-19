import datetime
import time
import json
import subprocess
import os.path
#import ip_grabber
#import urllib.request
#from config_update_retry import update_response as update_response

file_name = os.path.basename(__file__)[:-3]
print(file_name)

"""subprocess.run(["screen", "-S", "IP_Grabber_Loop", "-c", "python3", "ip_grabber.py"]) 

#while True:
#    update_response("Independant SubBots", "No Mans_Sky", "medium")
#    time.sleep(5)

LIST_OF_ADMINS = []

with open('config.json') as json_data:
    json_config = json.load(json_data)

for users in json_config["Bot Users"]:
    if users["Admin"] == 'True':
        LIST_OF_ADMINS.append(int(users["ID"]))
        print("Adding {}".format(users["ID"]))
    else:
        print("Ignoring {}".format(users["ID"]))


ip = ip_grabber.get_ip()
print(ip)

list1 = ["1918.pts-0.raspberrypi", "2609.pts-0.raspberrypi", "2621.pts-0.raspberrypi", ""]
for screen_name in list1:
    deep_split = screen_name.split('.')
    screen_name = deep_split[1]
del list1[(len(list1) - 1)]
screen_count = len(list1)

response = "There are {} screens active:".format(screen_count)
for screen_name in list1:
    response = response + "\n{}".format(screen_name)
print(response)


with open('config.json') as json_data:
            JSONConfig = json.load(json_data)
            print(json_data.read())

time1 = '23/08/2018 12:10:00'
time1Obj = datetime.datetime.strptime(time1, '%d/%m/%Y %H:%M:%S')
print(time1Obj)

time2 = '23/08/2018 12:26:00'
timeObj2 = datetime.datetime.strptime(time2, '%d/%m/%Y %H:%M:%S')
print(timeObj2)

time3 = '23/08/2018 12:26:00'
timeObj3 = datetime.datetime.strptime(time2, '%d/%m/%Y %H:%M:%S')
print(timeObj3)

timeApart = timeObj2 - time1Obj
print("The time between var's is: {}".format(timeApart))
print("The time between var's is: {}".format(timeApart.total_seconds()))
print("The time between var's is: {}".format((timeApart.total_seconds()/60)))


screenString = "2018-08-25 07:48:12.230053 - b'There are screens on:\r\n\t325.BotController\t(24/08/18 17:18:08)\t(Attached)\n\t27220.UF_NoMansSky\t(22/08/18 21:34:18)\t(Detached)\n\t27099.BennehBot\t(22/08/18 21:32:41)\t(Detached)\n3 Sockets in /run/screen/S-benneh.\r\n'"

screenSplit = screenString.split('\n\t')

i = 0
for line in screenSplit:
        print("{} - {}".format(i, line))
        i += 1

print(list(JSONConfig.keys()))

for SubBot in JSONConfig["Independant SubBots"]:
    if (SubBot["Name"]) == "No Mans Sky":
        SubBot["Last Response"] = time1Obj

with open('config.json', 'w') as outputfile:
    json.dump(JSONConfig, outputfile, indent=4) """