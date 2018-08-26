import logging
import json
import subprocess
import datetime
import shutil
from telegram.ext import Updater, CommandHandler

#Variables
sub_bots_enabled = []
screen_name_list = []

#Import JSON data
with open('config.json') as json_data:
    json_config = json.load(json_data)

#Functions
def get_time_difference(sub_bot):
    bots_last_response = datetime.datetime.strptime(sub_bot["Last Response"], '%d/%m/%Y %H:%M:%S')
    current_time = datetime.datetime.now()
    time_apart = current_time - bots_last_response
    return round(time_apart.total_seconds()/60)

#############
#Main script#
#############

#Find all running screens
result = subprocess.check_output(['ls', '/run/screen/S-benneh'])
screen_split = result.decode().split('\n')
for screen_name in screen_split:
    deep_split = screen_name.split('.')
    if len(deep_split) > 1:
        screen_name_list.append(deep_split[1])
del screen_split[(len(screen_split) - 1)]
screen_count = len(screen_split)

response = "There are {} screens active:".format(screen_count)
for screen_name in screen_name_list:
    response = response + "\n{}".format(screen_name)
print(response)
print("")

#Check bot status against screens
print("Bot Name \t Status \t Screen \t Response")
print("-"* shutil.get_terminal_size()[0])
for sub_bot in json_config["Independant SubBots"]:
    if sub_bot["Enabled"] == "True":
        if sub_bot["Name"] in screen_name_list:
            print("{} \t Enabled \t Active \t Last response:{}m ago".format(sub_bot["Name"], get_time_difference(sub_bot)))
        else:
            print("{} \t Enabled \t Missing \t Last response:{}m ago".format(sub_bot["Name"], get_time_difference(sub_bot)))
    else:
        print("{} \t Disabled".format(sub_bot["Name"]))

def bot_status(bot, update):
    print("Status check called")
    response_text = "Independant bots:"
    for sub_bot in json_config["Independant SubBots"]:
        response_text = response_text + "\n{} - Last response:{}m ago".format(sub_bot["Name"], get_time_difference(sub_bot))
    response_text = response_text + "\n\nDiscord bots:"
    for sub_bot in json_config["Discord SubBots"]:
        response_text = response_text + "\n{} - Last response:{}m ago".format(sub_bot["Name"], get_time_difference(sub_bot))
    
    update.message.reply_text(response_text)
    print("Status reply sent")
    
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
updater = Updater(token=json_config["Tokens"]["Telegram"]["Bot Token"])

updater.dispatcher.add_handler(CommandHandler('Status', bot_status))

updater.start_polling()
updater.idle()

