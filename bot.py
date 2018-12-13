import random
from random import randint

import requests, os, bs4
import yaml
from BotModules import BotModules

from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mregex_handler import MRegexHandler
from matrix_bot_api.mcommand_handler import MCommandHandler
from matrix_bot_api.mcomponent_handler import MComponentHandler

from IgnoreList import *
from HelpList import *

script_dir = os.path.dirname(__file__) # Absolute path to this script
config = yaml.safe_load(open(os.path.join(script_dir, "config.yml")))
USERNAME = config['username']
PASSWORD = config['password']
SERVER = config['server']
HELPFILE = config['helpfile']

botModules = BotModules()

def component_callback(room, event): 
    # Check for message
    if(event['type'] == "m.room.message"):
        botModules.CallMethodOnAll("OnMessageReceived", room, event)    
        if(event['content']['body'][0] == '!'): # Test for Command
            botModules.CallMethodOnAll("OnCommandReceived", room, event)       

def help_callback(room, event):
    # provide user with list of usable commands
    helpContents = GetHelpContents(os.path.join(script_dir, HELPFILE))
    room.send_text(helpContents)

def hi_callback(room, event):
    # Somebody said hi, let's say Hi back
    room.send_text("Hi, " + event['sender'])

def echo_callback(room, event):
    args = event['content']['body'].split()
    args.pop(0)
    
    # Echo what they said back
    room.send_text(' '.join(args))

def weather_callback(room, event):
    url = 'https://www.bbc.co.uk/weather/2643743'

    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text,features="html.parser")
    temp = soup.select('.wr-value--temperature--c')
    desc = soup.select('.wr-js-day-content-weather-type-description')
    room.send_text('In London it is currently: ' + temp[0].getText() + ' - ' + desc[0].getText())

def trains_callback(room, event):
    args = event['content']['body'].split()

    station1 = args[1]
    station2 = args[2]

    url = 'http://ojp.nationalrail.co.uk/service/ldbboard/dep/' + station1 + '/' + station2 +'/To'

    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text,features="html.parser")
    table = soup.find('table')
    table_body = table.find('tbody')
    data = []
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    output = ""
    for row in data:
        if "Details" not in row[3]:
            output += row[0] + ' to ' + row[1] + ' is "' + row[2] + '" on platform ' + row[3] + '.\n'
        else:
            output += row[0] + ' to ' + row[1] + ' is "' + row[2] + '". Platform is not known.\n'

    room.send_text(output)

    #TODO: Tie command functionality into user power levels
def IgnoreUser_callback(room, event):
    args = event['content']['body'].split() #TODO: Data validation / input hardening
    modifier = args[1] #either add, a or remove, r
    ignoreUser = args[2] #username of person to add / remove
    if modifier == "a" or modifier == "add":
        IgnoreList.AddUser(room.room_id, ignoreUser)
        room.send_text("Now ignoring user: " + ignoreUser)
    elif modifier == "r" or modifier == "remove":
        IgnoreList.RemoveUser(room.room_id, ignoreUser)
        room.send_text("Now listening to user: " + ignoreUser)

def main():
    # Create an instance of the MatrixBotAPI
    bot = MatrixBotAPI(USERNAME, PASSWORD, SERVER)

    botModules.LoadClasses("H:\Programming\PythonStuff\Jarvis\Components")
    botModules.CallMethodOnAll("Start")    
    componentHandler = MComponentHandler(component_callback)
    bot.add_handler(componentHandler) # adds component handler that deals with call events at correct time for all components

    hi_handler = MRegexHandler("Hi", hi_callback)
    bot.add_handler(hi_handler)

    echo_handler = MCommandHandler("echo", echo_callback)
    bot.add_handler(echo_handler)

    weather_handler = MCommandHandler("weather", weather_callback)
    bot.add_handler(weather_handler)

    trains_handler = MCommandHandler("trains", trains_callback)
    bot.add_handler(trains_handler)

    ignoreUser_handler = MCommandHandler("ignoreUser", IgnoreUser_callback)
    bot.add_handler(ignoreUser_handler)

    help_handler = MCommandHandler("Help", help_callback)
    bot.add_handler(help_handler)

    # Start polling
    bot.start_polling()

    # Infinitely read stdin to stall main thread while the bot runs in other threads
    go = True
    while go:
        botModules.CallMethodOnAll("Update")
        go = True

if __name__ == "__main__":
    main()
