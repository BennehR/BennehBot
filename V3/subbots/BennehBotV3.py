import discord
import asyncio
import time
import datetime
import sqlite3 as lite
import sys
import os
import importlib
import json
import logging

from discord.ext import commands
from threading import Thread

logging.basicConfig(filename='logs/BennehBot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

bot = commands.Bot(command_prefix='!')

def printMsg(msg):
    print("BOT: " + str(msg))

with open('config.json') as json_data:
    d = json.load(json_data)

@bot.event
async def on_ready():
    printMsg('Logged in as')
    printMsg(bot.user.name)
    printMsg(bot.user.id)
    printMsg('------') 

    for SubBot in d["Discord SubBots"]:
        if SubBot["Enabled"] == "True":
            SubBotFile = importlib.import_module(SubBot["File"])
            printMsg("Starting {} update finder".format(SubBot["Name"]))
            try:
                bot.loop.create_task(SubBotFile.VersionCheck(bot))
            except:
                try:
                    bot.loop.create_task(SubBotFile.VersionCheck())
                except:
                    pass
        else:
            printMsg("SubBot {} disabled".format(SubBot["Name"]))

@bot.command(pass_context=True)
async def hello(ctx):
    printMsg('Yo ' + ctx.author.name)
    Channel = ctx.channel
    await Channel.send("Hey {}".format(ctx.author.name))

bot.run(d["Tokens"]["Discord"], reconnect=True)