"""
Defines a matrix bot handler that uses regex to determine if message should be handled
"""
import re

from matrix_bot_api.mhandler import MHandler
from IgnoreList import *


class MRegexHandler(MHandler):

    # regex_str - Regular expression to test message against
    #
    # handle_callback - Function to call if messages matches regex
    def __init__(self, regex_str, handle_callback):
        MHandler.__init__(self, self.test_regex, handle_callback)
        self.regex_str = regex_str

    def test_regex(self, room, event):       
        if CheckIgnoreSender(event['sender']) == True: #if the user is in the ignore list
            return False
        # Test the message and see if it matches the regex
        if event['sender'] == "@jarvis:eaton.uk.net" or event['sender'] == "@chucklebot:eaton.uk.net":
            return False
        if event['type'] == "m.room.message":
            if re.search(self.regex_str, event['content']['body']):
                # The message matches the regex, return true
                return True

        return False

def CheckIgnoreSender(room, sender):
    allIgnored = GetGlobalIgnoreList
    thisRoomsIgnoreList = -1
    for roomIgnore in allIgnored: # find this room from all rooms
        if roomIgnore.roomID == room:
            thisRoomsIgnoreList = roomIgnore.ignoredUsers
            break
    if thisRoomsIgnoreList == -1: # room doesn't have an entry!
        AddNewRoom(room)