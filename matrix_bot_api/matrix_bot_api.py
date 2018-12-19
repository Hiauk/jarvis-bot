import traceback
import re
from matrix_client.client import MatrixClient
from matrix_client.api import MatrixRequestError
from IgnoreList import *


class MatrixBotAPI:

    # username - Matrix username
    # password - Matrix password
    # server   - Matrix server url : port
    # rooms    - List of rooms ids to operate in, or None to accept all rooms
    def __init__(self, username, password, server, rooms=None):
        self.username = username

        # Authenticate with given credentials
        self.client = MatrixClient(server)
        try:
            self.client.login_with_password(username, password)
        except MatrixRequestError as e:
            print(e)
            if e.code == 403:
                print("Bad username/password")
        except Exception as e:
            print("Invalid server URL")
            traceback.print_exc()

        # Store allowed rooms
        self.rooms = rooms

        # Store empty list of handlers
        self.handlers = []
        
        # If rooms is None, we should listen for invites and automatically accept them
        if rooms is None:
            self.client.add_invite_listener(self.handle_invite)
            self.rooms = []

            # Add all rooms we're currently in to self.rooms and add their callbacks
            for room_id, room in self.client.get_rooms().items():
                room.add_listener(self.handle_message)
                self.rooms.append(room_id)
                #if room_id == "!tukvxnciRWDbYQTSdw:eaton.uk.net": #Startup Message Example
                   #room.send_text("This is a startup message going out to my fellow bot Devs")  
        else:
            # Add the message callback for all specified rooms
            for room in self.rooms:
                room.add_listener(self.handle_message)
                
    def add_handler(self, handler):
        self.handlers.append(handler)

    def CheckIgnoreSender(self, room, sender):
        allIgnored = IgnoreList.GetGlobalIgnoreList()
        roomExists = False
        for roomIgnore in allIgnored: # find this room from all rooms
            if roomIgnore.roomID == room.room_id:
                roomExists = True
                for ignoredUser in roomIgnore.ignoredUsers:
                    if sender == ignoredUser:
                        return True
        if roomExists == False: #if the room (and hence user) did not exist
            IgnoreList.AddNewRoom(room.room_id) #create empty room entry
        return False # we fell through the for loop looking for user, this is always false

    def handle_message(self, room, event): # this is where the ignore check should really take place
        # Make sure we didn't send this message
        if re.match("@" + self.username, event['sender']):
            return
        if self.CheckIgnoreSender(room, event['sender']) == True:
            return
        
        # Loop through all installed handlers and see if they need to be called
        for handler in self.handlers:
            if handler.test_callback(room, event):
                # This handler needs to be called
                try:
                    handler.handle_callback(room, event)
                except:
                    traceback.print_exc()

    def handle_invite(self, room_id, state):
        print("Got invite to room: " + str(room_id))
        print("Joining...")
        room = self.client.join_room(room_id)

        # Add message callback for this room
        room.add_listener(self.handle_message)

        # Add room to list
        self.rooms.append(room)

    def start_polling(self):
        # Starts polling for messages
        self.client.start_listener_thread()
        return self.client.sync_thread

    