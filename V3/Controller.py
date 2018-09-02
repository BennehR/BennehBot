import logging
import json
import subprocess
import datetime
import shutil
import ip_grabber
import uf_launch_schedule
from telegram.ext import Updater, CommandHandler
from functools import wraps


#Variables
sub_bots_enabled = []
screen_name_list = []
LIST_OF_ADMINS = []

#Import JSON data
with open('config.json') as json_data:
    json_config = json.load(json_data)

for users in json_config["Bot Users"]:
    if users["Admin"] == "True":
        LIST_OF_ADMINS.append(int(users["ID"]))
        print("Adding {}".format(users["ID"]))
    else:
        print("Ignoring {}".format(users["ID"]))

#Decorators
def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            update.message.reply_text("You are unauthorised to perform that command. \nIf you think this is in error speak to the host.")
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

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

@restricted
def get_ip(bot, update):
    print("IP request received")
    update.message.reply_text(ip_grabber.get_ip())
    print("IP Sent")

def get_launches(bot, update):
    print("Received launch schedule request")
    update.message.reply_text(uf_launch_schedule.get_updates())
    print("Launch schedule sent")

def help(bot, update):
    update.message.reply_text("/Status\n/IP\n/Launch")

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
updater = Updater(token=json_config["Tokens"]["Telegram"])

updater.dispatcher.add_handler(CommandHandler('Status', bot_status))
updater.dispatcher.add_handler(CommandHandler('IP', get_ip))
updater.dispatcher.add_handler(CommandHandler('Launch', get_launches))
updater.dispatcher.add_handler(CommandHandler('?', help))

updater.start_polling()
updater.idle()

