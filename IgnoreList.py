# import the pickle module
import pickle, os, yaml

script_dir = os.path.dirname(__file__) # Absolute path to this script
config = yaml.safe_load(open(os.path.join(script_dir, 'config.yml')))
ignoreListName = config['ignorelist']

class IgnoreList:
    GlobalIgnoreLists = []
    def __init__(self, roomID, ignoredUsers):
        self.roomID = roomID
        self.ignoredUsers = ignoredUsers

    @staticmethod
    def LoadIgnoreList():
        unpicklefile = open(os.path.join(script_dir, ignoreListName + '.pkl'), 'rb')
        IgnoreList.GlobalIgnoreLists = pickle.load(unpicklefile)
        unpicklefile.close()

    @staticmethod
    def SaveIgnoreList():
        file = open(os.path.join(script_dir, ignoreListName + '.pkl'), 'wb')
        pickle.dump(IgnoreList.GlobalIgnoreLists,file)
        file.close()

    @staticmethod
    def AddNewRoom(roomID):
        newRoom = IgnoreList(roomID, [])
        IgnoreList.GlobalIgnoreLists.append(newRoom)
        IgnoreList.SaveIgnoreList()
        return newRoom

    @staticmethod
    def AddUser(roomID, userID):
        for anIgnoreList in IgnoreList.GlobalIgnoreLists:
            if anIgnoreList.roomID == roomID:
                anIgnoreList.ignoredUsers.append(userID)
        IgnoreList.SaveIgnoreList()

    @staticmethod
    def RemoveUser(roomID, userID):
        for anIgnoreList in IgnoreList.GlobalIgnoreLists:
            if anIgnoreList.roomID == roomID:
                anIgnoreList.ignoredUsers.remove(userID)
        IgnoreList.SaveIgnoreList()

    @staticmethod
    def GetGlobalIgnoreList():
        return IgnoreList.GlobalIgnoreLists

# Should this go in bot.py, maybe create a seperate config Init file?
fileExists = os.path.isfile(os.path.join(script_dir, ignoreListName + '.pkl'))
if fileExists == False:
    IgnoreList.SaveIgnoreList() # generate a blank pickle file
else:
    IgnoreList.LoadIgnoreList()