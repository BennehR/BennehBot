import discord
import asyncio
import time
import datetime
import sqlite3 as lite
import sys
import urllib.request
import requests

from bs4 import BeautifulSoup
from discord.ext import commands


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

async def FactorioVersionCheck():
    page = requests.get('https://forums.factorio.com/viewforum.php?f=3&sid=9e666eb4cc7efaa762351041e014425f')
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    links = soup.find_all('a', {"class" : "topictitle"})
    i = 0

    for thread in links:
        charUrl = thread.text

        if charUrl != "":
            if "Version" in charUrl:
                ThreadName = charUrl[8:]
                print(ThreadName)
                await asyncio.sleep(2)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------') 
    bot.loop.create_task(FactorioVersionCheck())

@bot.command(pass_context=True)
async def hello(ctx):
    print('Yo ' + ctx.author.name)

bot.run(getToken())