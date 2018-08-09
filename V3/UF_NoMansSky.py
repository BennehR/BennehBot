import asyncio
import time
import urllib.request
import requests
import sqlite3 as lite
from bs4 import BeautifulSoup

NMSVers = []

""" async def NMSVerListSetup():
    NMSVers.clear()
    try:
        con = lite.connect('BennehBotDB.db')
        cur = con.cursor()
        cur.execute("SELECT Ver FROM NMS_Versions")
        i = 0

        for versions in cur:
            NMSVers.append(versions[0])

    except lite.Error as e:
        return('Unhandled connection error \n' + e.message)
    finally:
        con.close()
    
    #print(NMSVers)
    #print('----------') """

def NMSVersionCheck():

    #while True:
        #await NMSVerListSetup()

    #This needs indenting once more when added back into a loop
    print('List updated')
    UrlHeader = 'https://www.nomanssky.com/'
    page = requests.get('https://www.nomanssky.com/release-log/')
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    updateEntries = soup.find_all('a', {"class" : "link link--inherit"})
    i = 0

    for entry in updateEntries:
        updateText = entry.find("h2", recursive=True)
        updateText = updateText.text
        #updateLink = entry.findChildren("a", recursive=True)
        updateURL = entry.attrs['href']
        print(updateText + " - " + updateURL)
        #print(updateURL)

    print('Complete')

NMSVersionCheck()

#Existing code for reference before deletion
""" #Loop through the links found by BS
for patch in links:
    PatchName = patch.text

    #If the PatchName is not blank
    if PatchName != "":

        #If the PatchName contains 'Version' trim it out and begin
        if "Version" in PatchName:
            PatchName = PatchName[8:]

            #If the number does not exist in the array of known versions
            #Grab its URL and date submitted then add all this to the DB
            if PatchName not in NMSVers:
                print(PatchName + " appears to be a new release")
                PatchURL = patch.attrs['href']
                PatchURL = UrlHeader + PatchURL[2:]
                PatchSubmitted = patch.parent.text
                SplitLoc = PatchSubmitted.find('»')
                PatchSubmitted = PatchSubmitted[SplitLoc + 2:]
                PatchSubmitted = PatchSubmitted.strip()

                try:
                    con = lite.connect('BennehBotDB.db')
                    cur = con.cursor()
                    cur.execute("INSERT INTO NMS_Versions VALUES(?,?,?,?)", (PatchName, PatchSubmitted, PatchURL, "N/A"))
                    con.commit()
                except lite.Error as e:
                    return('Unhandled connection error \n' + e.message)
                finally:
                    con.close()
                
                #await Channel.send('A new version has been posted to the forum.')
                #await Channel.send(PatchName + " - " + PatchSubmitted + " - " + PatchURL)
                #print('A new version has been posted to the forum.')
                #print(PatchName + " - " + PatchSubmitted + " - " + PatchURL)
                
print("Done, now waiting...")
await asyncio.sleep(900)
print("Finished waiting")"""