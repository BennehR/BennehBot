import asyncio
import time
import urllib.request
import requests
import sqlite3 as lite
from bs4 import BeautifulSoup
from config_update_retry import update_response
import logging

FacVers = []
logging.basicConfig(filename='logs/UF_Factorio.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def printMsg(msg):
    print("UF_Fac: " + str(msg))

async def FactorioVerListSetup():
    FacVers.clear()
    printMsg('Refreshing version list')
    try:
        con = lite.connect('BennehBotDB.db')
        cur = con.cursor()
        cur.execute("SELECT Ver FROM Factorio_Versions")

        for versions in cur:
            FacVers.append(versions[0])

    except lite.Error as e:
        return('Unhandled connection error \n' + e.message)
    finally:
        con.close()

async def VersionCheck(botVar):

    while True:
        await FactorioVerListSetup()
        printMsg('List updated')
        Channel = botVar.get_channel(396716668967059468)
        UrlHeader = 'https://forums.factorio.com/'
        page = requests.get('https://forums.factorio.com/viewforum.php?f=3&sid=9e666eb4cc7efaa762351041e014425f')
        data = page.text
        soup = BeautifulSoup(data, 'html.parser')
        links = soup.find_all('a', {"class" : "topictitle"})

        #Loop through the links found by BS
        for thread in links:
            ThreadName = thread.text

            #If the ThreadName is not blank
            if ThreadName != "":

                #If the ThreadName contains 'Version' trim it out and begin
                if "Version" in ThreadName:
                    ThreadName = ThreadName[8:]

                    #If the number does not exist in the array of known versions
                    #Grab its URL and date submitted then add all this to the DB
                    if ThreadName not in FacVers:
                        printMsg(ThreadName + " appears to be a new release")
                        ThreadURL = thread.attrs['href']
                        ThreadURL = UrlHeader + ThreadURL[2:]
                        ThreadSubmitted = thread.parent.text
                        SplitLoc = ThreadSubmitted.find('»')
                        ThreadSubmitted = ThreadSubmitted[SplitLoc + 2:]
                        ThreadSubmitted = ThreadSubmitted.strip()

                        try:
                            con = lite.connect('BennehBotDB.db')
                            cur = con.cursor()
                            cur.execute("INSERT INTO Factorio_Versions VALUES(?,?,?,?)", (ThreadName, ThreadSubmitted, ThreadURL, "N/A"))
                            con.commit()
                        except lite.Error as e:
                            return('Unhandled connection error \n' + e.message)
                        finally:
                            con.close()
                        
                        await Channel.send('A new version has been posted to the forum.')
                        await Channel.send(ThreadName + " - " + ThreadSubmitted + " - " + ThreadURL)
                        printMsg('A new version has been posted to the forum.')
                        printMsg(ThreadName + " - " + ThreadSubmitted + " - " + ThreadURL)
        printMsg("UF_Fac done.")
        update_response("Discord SubBots", "Factorio", "medium")
        await asyncio.sleep(900)