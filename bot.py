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
ERRORLOG = config['errorlog']
COMPONENTSFOLDER = config['componentspath']

botName = ("@" + USERNAME + ":" + SERVER.split("//")[1]).lower() # @ + MyBot + https://matrix.org = '@mybot:matrix.org' - this is the username within channel
botModules = BotModules()

def component_callback(room, event): 
    if(event['sender'] == botName): #if event sender is ourselves, ignore completely
        return

    # Check that this is a message
    if(event['type'] == "m.room.message"):
        botModules.CallMethodOnAll("OnMessageReceived", room, event)    
        if(event['content']['body'][0] == '!'): # Test for Command
            botModules.CallMethodOnAll("OnCommandReceived", room, event)       

def help_callback(room, event):
    # provide user with list of usable commands
    helpContents = GetHelpContents(os.path.join(script_dir, HELPFILE))
    room.send_text(helpContents)

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

    #botModules.LoadClasses("H:\Programming\PythonStuff\Jarvis\Components")
    botModules.LoadClasses(os.path.join(script_dir, COMPONENTSFOLDER))
    
    botModules.CallMethodOnAll("Start") # Call start function on all loaded components
    componentHandler = MComponentHandler(component_callback)
    bot.add_handler(componentHandler) # adds component handler that deals with call events at correct time for all components

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
