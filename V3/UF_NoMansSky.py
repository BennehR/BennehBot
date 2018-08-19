import asyncio
import datetime
import urllib.request
import requests
import sqlite3 as lite
from bs4 import BeautifulSoup
import json

NMSVers = []

def printMsg(msg):
    print("UF_NMS: " + str(msg))

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def TelegramUpdate(updateInfo, JSONData):
    for token in JSONData["Tokens"]["Telegram"]["ChatID"]:
        url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(JSONData["Tokens"]["Telegram"]["BotToken"], next(iter(token.keys())), updateInfo)
        printMsg(url)
        get_url(url)

async def NMSVerListSetup():
    NMSVers.clear()
    printMsg('Refreshing version list')
    try:
        con = lite.connect('BennehBotDB.db')
        cur = con.cursor()
        cur.execute("SELECT PatchName FROM NMS_Versions")
        i = 0

        for versions in cur:
            NMSVers.append(versions[0])

    except lite.Error as e:
        return('Unhandled connection error \n' + e.message)
    finally:
        con.close()

async def NMSVersionCheck():
    while True:
        with open('config.json') as json_data:
            JSONConfig = json.load(json_data)

        await NMSVerListSetup()
        printMsg('List updated')
        UrlHeader = 'https://www.nomanssky.com/'
        page = requests.get('https://www.nomanssky.com/release-log/')
        data = page.text
        soup = BeautifulSoup(data, 'html.parser')
        updateEntries = soup.find_all('a', {"class" : "link link--inherit"})
        i = 0

        for entry in updateEntries:
            updateText = entry.find("h2", recursive=True)
            updateText = updateText.text
            updateURL = entry.attrs['href']

            #This section checks if the URL starts with https, corrects if not
            if "http" not in updateURL:
                updateURL = UrlHeader + updateURL[1:]

            dateStamp = str(datetime.datetime.now())

            if updateText not in NMSVers:
                printMsg('New entry')
                updateInfo = updateText + " - " + updateURL + " - " + dateStamp
                printMsg(updateInfo)
                TelegramUpdate(updateInfo, JSONConfig)

                try:
                    printMsg('Connecting...')
                    con = lite.connect('BennehBotDB.db')
                    printMsg('Connected!')
                    cur = con.cursor()
                    printMsg('Adding to DB...')
                    cur.execute("INSERT INTO NMS_Versions VALUES(?,?,?)", (updateText, updateURL, dateStamp))
                    printMsg('Committing...')
                    con.commit()
                    printMsg('Entry added to DB')
                except Exception as e:
                    return("Unhandled connection error \n" + str(e))
                except lite.Error as e:
                    return('Unhandled connection error \n' + e.message)
                finally:
                    con.close()

        printMsg('UF_NMS done.')
        await asyncio.sleep(900)