from ComponentParent import Component
from ComponentParent import Config
import pickle, os, yaml

class Ignore(Component):
    defaultDataFile = "IgnoreUserData.pkl" # default name for the file storing ignore data
    def __init__(self):
        Component.__init__(self, self)

    def Start(self):
        self.IgnoreData = self.config.GetKey("ignoredata") # get path to helpfile        
        if(self.IgnoreData == None): # if there was none available
            self.__InitConfig()                
        self.LoadIgnoreList() # The file existed before, try to load it
        

    def __InitConfig(self):
        self.IgnoreData = os.path.join(os.path.dirname(__file__), Ignore.defaultDataFile) # Set default value for next time
        self.config.SetKey("ignoredata", self.IgnoreData) # Set default value for next time

    def LoadIgnoreList(self):
        if os.path.isfile(self.IgnoreData) == False: #if there is no data file at stated location
            print("No Ignore Data found at " + self.IgnoreData)
            self.globalIgnoreLists = {} # init the ignore list
            return # no data return
        unpicklefile = open(self.IgnoreData, 'rb')
        self.globalIgnoreLists = pickle.load(unpicklefile)
        unpicklefile.close()
    
    def SaveIgnoreList(self):
        file = open(self.IgnoreData, 'wb')
        pickle.dump(self.globalIgnoreLists,file)
        file.close()
    
    def AddNewRoom(self, roomID):
        self.globalIgnoreLists.update({roomID : []})
        self.SaveIgnoreList()
    
    def AddUser(self, roomID, userID):
        if roomID not in self.globalIgnoreLists: # if there is not entry for current room in ignore Lists
            self.AddNewRoom(roomID) # add the new room
        if userID in self.globalIgnoreLists[roomID]: # if the useris not already being ignored for the given room
            return userID + " is already being ignored!"

        self.globalIgnoreLists[roomID].append(userID) # add the user        
        self.SaveIgnoreList() # save our changes
        return "Now ignoring user: " + userID
    
    def RemoveUser(self, roomID, userID):
        if roomID not in self.globalIgnoreLists: #if there is no list for this room, they are being listened to
            return "User not in ignore list"
        if userID not in self.globalIgnoreLists[roomID]: #if user not in the ignore list
            return "User not in ignore list"

        self.globalIgnoreLists[roomID].remove(userID) # everything valid, remove them
        self.SaveIgnoreList() # saved our changed
        return "Now listening to user: " + userID
        
    
    def GetGlobalIgnoreList(self):
        return self.globalIgnoreLists

    def ProcessCommand(self, room, event):
        args = event['content']['body'].split() #TODO: Data validation / input hardening
        try:
            modifier = args[1] #either add, a or remove, r
            ignoreUser = args[2] #username of person to add / remove
            if modifier == "a" or modifier == "add":
                response = self.AddUser(room.room_id, ignoreUser) # try to add user, get message about how successful we were to send back
                room.send_text(response)
            elif modifier == "r" or modifier == "remove":
                response = self.RemoveUser(room.room_id, ignoreUser) # try to remove user, get message about how successful we were to send back
                room.send_text(response)
        except:
            room.send_text("Error while processing previous Ignore command")

    def OnCommandReceived(self, room, event):
        args = event['content']['body'].split()
        commandCharRemoved = args[0][1:] #args[0].
        args.pop(0)
        if(commandCharRemoved == "Ignore"):
            self.ProcessCommand(room, event)