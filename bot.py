import discord
import asyncio
import time
import datetime
import sqlite3 as lite
import sys
from urllib.request import urlopen
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

#def webScrape(pageLink):
#    page = requests.get(pageLink)
#    tree = html.fromstring(page.content)

#    soup = BeautifulSoup(page)

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
            classLevel = str(classes.nextSibling).strip()
            classGroup = classGroup + tooltip + ": " + classLevel + "\n"
        
        #print(classGroup)



        return(charName + 
            "\nCharacter title: " + charTitle + 
            "\nCharacter FreeCompany: " + charFC + 
            "\nClass Levels:" + 
            classGroup)

    else:
        return('Multiple results found, please narrow your search and check the spelling')

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
                #lodeCheck(serverName, firstName, secondName)
                
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
