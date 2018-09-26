# import the pickle module
import pickle, os, yaml

script_dir = os.path.dirname(__file__) # Absolute path to this script
config = yaml.safe_load(open(script_dir + "\config.yml"))
ignoreListName = config['ignorelist']

GlobalIgnoreLists = []


class IgnoreList:
    def __init__(self, roomID, ignoredUsers):
        self.roomID = roomID
        self.ignoredUsers = ignoredUsers

def LoadIgnoreList():
    unpicklefile = open(script_dir + "\\" + ignoreListName + ".pkl", 'rb')
    GlobalIgnoreLists = pickle.load(unpicklefile)
    unpicklefile.close()

def SaveIgnoreList():
    file = open(script_dir + "\\" + ignoreListName + ".pkl", 'wb')
    pickle.dump(GlobalIgnoreLists,file)
    file.close()

def AddNewRoom(roomID):
    newRoom = IgnoreList(roomID, [])
    GlobalIgnoreLists.append(newRoom)
    return newRoom

def GetGlobalIgnoreList():
    return GlobalIgnoreLists

fileExists = os.path.isfile(script_dir + "\\" + ignoreListName + ".pkl");
if fileExists == False:
    SaveIgnoreList() # generate a blank pickle file
else:
    LoadIgnoreList()