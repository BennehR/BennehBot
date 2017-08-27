import discord
import asyncio
import time
import datetime
import sqlite3 as lite
import sys
import urllib.request
from bs4 import BeautifulSoup
import requests

con = None
client = discord.Client()

try:
    print('Opening connection to psycoUsers database')

    con = lite.connect('psycoUsers.db')

    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')

    data = cur.fetchone()

    print('SQLite version: %s' % data)
    print('Connection successful')

finally:
    if con:
        con.close()
        print('Closing connection')

def testDef(word):
    strings = word.content.split()
    print('Ignoring the command, you said: ' + strings[1])
    return('Ignoring the command, you said: ' + strings[1])

def dbPull(nameInput):
    strings = nameInput.content.split()
    con = lite.connect('psycoUsers.db')

    name = strings[1]
    cur = con.cursor()
    cur.execute("SELECT screenName, psycoMember FROM users WHERE userName=?", (name,))

    hasResults = False
    for row in cur:
        hasResults = True
        screenNames = row[0]
        psycoMember = row[1]
        con.close()

        return('Discord user "' + strings[1] + '" is also known by "' + screenNames + '". \nIs a psyconautics member?: ' + psycoMember)

    if not hasResults:
        con.close()
        return('User is not known to the psyco database. \n!whosis is case and spelling sensitive.')

def dbAdd(fedInfo):
    strings = fedInfo.content.split(";")
    if len(strings) == 4:
        con = lite.connect('psycoUsers.db')

        usrName = strings[1]
        scrnName = strings[2]
        psyMem = strings[3]
        cur = con.cursor()
        print(usrName + " " + scrnName + " " + psyMem)
        try:
            cur.execute("INSERT INTO users VALUES(?,?,?)", (usrName, scrnName, psyMem))
            con.commit()
            return('User added')
        except lite.IntegrityError as e:
            return('User already exists in the database with that name, use !whois to get details.')
        except lite.Error as e:
            return('Unhandled connection error \n' + e.message)
        finally:
            con.close()
    
    else:
        return('Incorrect number of paramters provided. Please refer to "$psycoAdd help" if required.')

def lodeCheck(server, firstName, secondName):
    page = requests.get('http://na.finalfantasyxiv.com/lodestone/character/?q=' + firstName + "%20" + secondName)
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    links = soup.find_all('a', {"class" : "entry__link"})
    baseUrl = 'http://na.finalfantasyxiv.com'
    charUrl = ''
    fullUrl = ''
    charName = firstName + " " + secondName
    print('Results: ' + str(len(links)))

    if len(links) == 1:
        charUrl = links[0].attrs['href']
        fullUrl = baseUrl + charUrl
        print(fullUrl)
    
        page = requests.get(fullUrl)
        data = page.text
        soup = BeautifulSoup(data, 'html.parser')

        try:
            charTitle = soup.find('p', {"class" : "frame__chara__title"}).text
        except:
            charTitle = 'None'
        
        try:
            charFC = soup.find('div', {"class" : "character__freecompany__name"}).find('h4').text
        except:
            charFC = 'None'

        classGroup = ''
        classNames = soup.find_all('img', {"class" : "js__tooltip"})

        for classes in classNames:
            tooltip = classes.attrs['data-tooltip']
            tooltipBold = "*" + str(tooltip) + "*"
            classLevel = str(classes.nextSibling).strip()
            classGroup = classGroup + tooltipBold + ": " + classLevel + "\n"
        
        imgUrl = soup.find('div', {"class" : "character__detail__image"}).find('a').find('img')['src']
        urllib.request.urlretrieve(imgUrl, "playerImage.jpg")
        print(imgUrl)


        return(charName + 
            "\n**Character title**: " + charTitle + 
            "\n**Character FreeCompany**: " + charFC + 
            "\n**Class Levels**:\n" + 
            classGroup)

    else:
        return('Multiple results found, please narrow your search and check the spelling')

def potdCheck(dataCenter, classSel):
    classLib = {'gladiator' : '125bf9c1198a3a148377efea9c167726d58fa1a5',
        'paladin' : '125bf9c1198a3a148377efea9c167726d58fa1a5',
        'warrior' : '741ae8622fa496b4f98b040ff03f623bf46d790f',
        'marauder' : '741ae8622fa496b4f98b040ff03f623bf46d790f',
        'darkknight' : 'c31f30f41ab1562461262daa74b4d374e633a790',
        'whitemage' : '56d60f8dbf527ab9a4f96f2906f044b33e7bd349',
        'conjurer' : '56d60f8dbf527ab9a4f96f2906f044b33e7bd349',
        'scholar' : '56f91364620add6b8e53c80f0d5d315a246c3b94',
        'astrologian' : 'eb7fb1a2664ede39d2d921e0171a20fa7e57eb2b',
        'monk' : '46fcce8b2166c8afb1d76f9e1fa3400427c73203',
        'pugilist' : '46fcce8b2166c8afb1d76f9e1fa3400427c73203',
        'dragoon' : 'b16807bd2ef49bd57893c56727a8f61cbaeae008',
        'lancer' : 'b16807bd2ef49bd57893c56727a8f61cbaeae008',
        'ninja' : 'e8f417ab2afdd9a1e608cb08f4c7a1ae3fe4a441',
        'rouge' : 'e8f417ab2afdd9a1e608cb08f4c7a1ae3fe4a441',
        'samurai' : '7c3485028121b84720df20de7772371d279d097d',
        'bard' : 'f50dbaf7512c54b426b991445ff06a6697f45d2a',
        'archer' : 'f50dbaf7512c54b426b991445ff06a6697f45d2a',
        'machinist' : '773aae6e524e9a497fe3b09c7084af165bef434d',
        'blackmage' : 'f28896f2b4a22b014e3bb85a7f20041452319ff2',
        'thaumaturge' : 'f28896f2b4a22b014e3bb85a7f20041452319ff2',
        'summoner' : '9ef51b0f36842b9566f40c5e3de2c55a672e4607',
        'arcanist' : '9ef51b0f36842b9566f40c5e3de2c55a672e4607',
        'redmage' : '55a98ea6cf180332222184e9fb788a7941a03ec3'}


    link1 = 'http://na.finalfantasyxiv.com/lodestone/ranking/deepdungeon/?subtype='
    link2 = classLib[classSel.lower()]
    link3 = '&solo_party=solo&dcgroup='
    link4 = dataCenter
    page = requests.get(link1 + link2 + link3 + link4)
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    rankings = soup.find_all(class_="deepdungeon__ranking__order")
    charNames = soup.find_all(class_="deepdungeon__ranking__name")

    

    outputString = ''
    listPos = 0
    for name in charNames:
        outputString = outputString + str(rankings[listPos].find('p').text) + " - " + str(charNames[listPos].find('h3').get_text()) + "\n"
        listPos = listPos + 1
        
    print(link1 + link2 + link3 + link4)
    print(outputString)
    return(outputString)
    #return('[Debug] Complete, see console.')

def getToken():
    con = lite.connect('psycoUsers.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM clientToken")

    for row in cur:
        clientToken = row[0]
        con.close()
        return(clientToken)

def getAuths(authId):
    con = lite.connect('psycoUsers.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM authUsers")

    authUsers = []
    x = 0
    for row in cur:
        authUsers.append(row[x])
        x = x + 1
    
    con.close()

    if authId in authUsers:
        return(True)
    else:
        return(False)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------') 

@client.event
async def on_message(message):

    if message.content.startswith('!'):
            if message.content.startswith('!hello'):
                msgauth = message.author.name
                await client.send_message(message.channel, 'Hello {}'.format(msgauth))

            elif message.content.startswith('!repeat'):
                await client.send_message(message.channel, testDef(message))

            elif message.content.startswith('!whois'):
                await client.send_message(message.channel, dbPull(message))

            elif message.content.startswith('!test'):
                counter = 0
                tmp = await client.send_message(message.channel, 'Calculating messages...')
                async for log in client.logs_from(message.channel, limit=100):
                    if log.author == message.author:
                        counter += 1
                await client.edit_message(tmp, 'You have {} messages.'.format(counter))

            elif message.content.startswith('!sleep'):
                await asyncio.sleep(5)
                await client.send_message(message.channel, 'Done sleeping')

            elif message.content.startswith('!ping'):
                await client.send_message(message.channel, 'Pong!')

            elif message.content.startswith('!about'):
                await client.send_message(message.channel, 'My name is BennenBot, I was created on 23/08/17.')
                await client.send_message(message.channel, 'I was created out of boredom and interest to learn')
                await client.send_message(message.channel, 'If there is a problem with me, please report it on GitHub ()')

            elif message.content.startswith('!lodestone'):
                strings = message.content.split()
                serverName = strings[1]
                firstName = strings[2]
                secondName = strings[3]
                tmp = await client.send_message(message.channel, 'Looking up ' + firstName + " " + secondName + " on Lodestone...")
                await client.edit_message(tmp, lodeCheck(serverName, firstName, secondName))
                await client.send_file(message.channel, "playerImage.jpg")

            elif message.content.startswith('!potd'):
                strings = message.content.split()
                dataCenter = strings[1]
                charClass = strings[2]
                tmp = await client.send_message(message.channel, 'Looking up the top 25 solo rankings for ' + charClass + ' in POTD...')
                await client.edit_message(tmp, 'Results for solo **' + charClass + "** \n" + potdCheck(dataCenter, charClass))
                
                
            else:
                await client.send_message(message.channel, 'Sorry thats not a !command I recognise')

    elif message.content.startswith('$'):
        if (getAuths(message.author.id)):
            if message.content.startswith('$boom'):
                await client.send_message(message.channel, 'boom shake the room!')

            elif message.content.startswith('$psycoAdd'):
                await client.send_message(message.channel, dbAdd(message))

            else:
                await client.send_message(message.channel, 'Sorry thats not a $command I recognise')

        else:
            await client.send_message(message.channel, 'Sorry, your not authorised to use $ commands')
            await client.send_message(message.channel, 'If you think this is in error, contact "benneh"')


client.run(getToken())
