import logging
import json
import subprocess
import datetime
import shutil
import config_update_retry as config_update_retry
import ip_grabber as ip_grabber
#from subbots.ip_grabber import get_ip
import uf_launch_schedule as uf_launch_schedule
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
    bots_last_response = datetime.datetime.strptime(sub_bot["Last Response"], '%Y-%m-%d %H:%M:%S')
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
    with open('config.json') as json_data:
        json_config = json.load(json_data)
    response_text = "Independant bots:"
    for sub_bot in json_config["Independant SubBots"]:
        response_text = response_text + "\n{} - Last response:{}m ago".format(sub_bot["Name"], get_time_difference(sub_bot))
    response_text = response_text + "\n\nDiscord bots:"
    for sub_bot in json_config["Discord SubBots"]:
        response_text = response_text + "\n{} - Last response:{}m ago".format(sub_bot["Name"], get_time_difference(sub_bot))
    
    update.message.reply_text(response_text)
    print("Status reply sent")

################################
#IP_Grabber commands
@restricted
def get_ip(bot, update):
    print("IP request received")
    update.message.reply_text(ip_grabber.get_ip())
    print("IP Sent")

def begin_ip_loop(bot, update):
    print("Beginning IP Grabber loop in a window")
    update.message.reply_text("Beginning IP Grabber loop in a window")
    ip_grabber.set_enabled()

def stop_ip_loop(bot, update):
    print("Disabling IP Grabber, process will make one final check and end in the next 15 minutes.")
    update.message.reply_text("Disabling IP Grabber, process will make one final check and end in the next 15 minutes.")
    ip_grabber.set_disabled()

################################
#uf_launch_schdule commands
def get_launches(bot, update):
    print("Received launch schedule request")
    update.message.reply_text(uf_launch_schedule.get_updates())
    print("Launch schedule sent")

################################
#Telegram bot commands
def help(bot, update):
    #bot_commands = ['Status', 'IP', 'IP_Loop_Begin', 'IP_Loop_Stop', 'Launch', '?']
    response_text = ""
    for command in bot_commands:
        response_text = "/{}\n{}".format(command, response_text)
    update.message.reply_text(response_text)

################################
logging.basicConfig(filename='logs/Controller.log', level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
updater = Updater(token=json_config["Tokens"]["Telegram"])

################################
#Command handlers

bot_commands = {
    "Status" : bot_status,
    "IP" : get_ip,
    "IP_Loop_Begin" : begin_ip_loop,
    "IP_Loop_Stop" : stop_ip_loop,
    "Launch" : get_launches,
    "Help" : help
}

for command in bot_commands:
    updater.dispatcher.add_handler(CommandHandler(command, bot_commands[command]))
    print("Added command {} with def {}".format(command, bot_commands[command]))

""" updater.dispatcher.add_handler(CommandHandler('Status', bot_status))

updater.dispatcher.add_handler(CommandHandler('IP', get_ip))
updater.dispatcher.add_handler(CommandHandler('IP_Loop_Begin', begin_ip_loop))
updater.dispatcher.add_handler(CommandHandler('IP_Loop_Stop', stop_ip_loop))

updater.dispatcher.add_handler(CommandHandler('Launch', get_launches))
updater.dispatcher.add_handler(CommandHandler('?', help)) """

updater.start_polling()
updater.idle()

