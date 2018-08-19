import discord
import asyncio
import time
import datetime
import sqlite3 as lite
import sys
import os
import concurrent.futures

from discord.ext import commands
from threading import Thread

import UF_Factorio
import UF_NoMansSky

FactorioVerListSetup = UF_Factorio.FactorioVerListSetup
FactorioVersionCheck = UF_Factorio.FactorioVersionCheck
NMSVerListSetup = UF_NoMansSky.NMSVerListSetup
NMSVersionCheck = UF_NoMansSky.NMSVersionCheck

keepLooping = True

con = None
bot = commands.Bot(command_prefix='!')

def printMsg(msg):
    print("BOT: " + str(msg))

try:
    printMsg('Opening connection to BennehBotDB database')

    con = lite.connect('BennehBotDB.db')

    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')

    data = cur.fetchone()

    printMsg('SQLite version: %s' % data)
    printMsg('Connection successful')

finally:
    if con:
        con.close()
        printMsg('Closing connection')

def getToken():
    con = lite.connect('BennehBotDB.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM clientToken")

    for row in cur:
        clientToken = row[0]
        con.close()
        return(clientToken)

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete()

async def loopTasks():
    tasks = [
        FactorioVersionCheck(bot),
        NMSVersionCheck()
    ]

    while keepLooping is True:
        for t in tasks:
            start_loop(t)
        await asyncio.sleep(5)

@bot.event
async def on_ready():
    printMsg('Logged in as')
    printMsg(bot.user.name)
    printMsg(bot.user.id)
    printMsg('------') 
    #await FactorioVerListSetup()
    bot.loop.create_task(FactorioVersionCheck(bot))
    bot.loop.create_task(NMSVersionCheck())
    #await bot.loop.create_task(loopTasks)

    """ loop = asyncio.get_event_loop()
    loop.run_forever(asyncio.gather(
        FactorioVersionCheck(bot),
        NMSVersionCheck(),
    )) """

    """ loop = asyncio.get_event_loop()

    try:
        asyncio.ensure_future(FactorioVersionCheck(bot))
        asyncio.ensure_future(NMSVersionCheck())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        printMsg('Loop completed')
        loop.close() """

    """ new_loop = asyncio.new_event_loop()
    asyncio.run_coroutine_threadsafe(FactorioVersionCheck(bot), new_loop)
    asyncio.run_coroutine_threadsafe(NMSVersionCheck(), new_loop) """


@bot.command(pass_context=True)
async def hello(ctx):
    printMsg('Yo ' + ctx.author.name)

bot.run(getToken())