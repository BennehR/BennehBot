import discord
import asyncio
import time
import datetime
import sqlite3 as lite
import sys
import os

from discord.ext import commands
import UF_Factorio
import UF_NoMansSky

FactorioVerListSetup = UF_Factorio.FactorioVerListSetup
FactorioVersionCheck = UF_Factorio.FactorioVersionCheck

con = None
bot = commands.Bot(command_prefix='!')

try:
    print('Opening connection to BennehBotDB database')

    con = lite.connect('BennehBotDB.db')

    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')

    data = cur.fetchone()

    print('SQLite version: %s' % data)
    print('Connection successful')

finally:
    if con:
        con.close()
        print('Closing connection')

def getToken():
    con = lite.connect('BennehBotDB.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM clientToken")

    for row in cur:
        clientToken = row[0]
        con.close()
        return(clientToken)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------') 
    await FactorioVerListSetup()
    bot.loop.create_task(FactorioVersionCheck(bot))

@bot.command(pass_context=True)
async def hello(ctx):
    print('Yo ' + ctx.author.name)

bot.run(getToken())