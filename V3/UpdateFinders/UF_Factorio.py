import asyncio
import time
import urllib.request
import requests
from bs4 import BeautifulSoup

FacVers = []

async def FactorioVerListSetup():
    FacVers.clear()
    try:
        con = lite.connect('BennehBotDB.db')
        cur = con.cursor()
        cur.execute("SELECT Ver FROM Factorio_Versions")
        i = 0

        for versions in cur:
            FacVers.append(versions[0])

    except lite.Error as e:
        return('Unhandled connection error \n' + e.message)
    finally:
        con.close()
    
    #print(FacVers)
    #print('----------')

async def FactorioVersionCheck():
    while True:
        await FactorioVerListSetup()
        Channel = bot.get_channel(396716668967059468)
        UrlHeader = 'https://forums.factorio.com/'
        page = requests.get('https://forums.factorio.com/viewforum.php?f=3&sid=9e666eb4cc7efaa762351041e014425f')
        data = page.text
        soup = BeautifulSoup(data, 'html.parser')
        links = soup.find_all('a', {"class" : "topictitle"})
        i = 0

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
                        print(ThreadName + " appears to be a new release")
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
                        
        print("Done, waiting")
        await asyncio.sleep(900)
        print("Finished waiting")