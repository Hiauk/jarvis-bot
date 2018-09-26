# import the pickle module
import pickle, os, yaml

script_dir = os.path.dirname(__file__) # Absolute path to this script
config = yaml.safe_load(open(script_dir + "\config.yml"))
ignoreListName = config['ignorelist']


class IgnoreList:
    GlobalIgnoreLists = []
    def __init__(self, roomID, ignoredUsers):
        self.roomID = roomID
        self.ignoredUsers = ignoredUsers
    def LoadIgnoreList():
        unpicklefile = open(script_dir + "\\" + ignoreListName + ".pkl", 'rb')
        IgnoreList.GlobalIgnoreLists = pickle.load(unpicklefile)
        unpicklefile.close()

    def SaveIgnoreList():
        file = open(script_dir + "\\" + ignoreListName + ".pkl", 'wb')
        pickle.dump(IgnoreList.GlobalIgnoreLists,file)
        file.close()

    def AddNewRoom(roomID):
        newRoom = IgnoreList(roomID, [])
        IgnoreList.GlobalIgnoreLists.append(newRoom)
        IgnoreList.SaveIgnoreList()
        return newRoom

    def AddUser(roomID, userID):
        for anIgnoreList in IgnoreList.GlobalIgnoreLists:
            if anIgnoreList.roomID == roomID:
                anIgnoreList.ignoredUsers.append(userID)
        IgnoreList.SaveIgnoreList()

    def RemoveUser(roomID, userID):
        for anIgnoreList in IgnoreList.GlobalIgnoreLists:
            if anIgnoreList.roomID == roomID:
                anIgnoreList.ignoredUsers.remove(userID)
        IgnoreList.SaveIgnoreList()

    def GetGlobalIgnoreList():
        return IgnoreList.GlobalIgnoreLists

fileExists = os.path.isfile(script_dir + "\\" + ignoreListName + ".pkl");
if fileExists == False:
    IgnoreList.SaveIgnoreList() # generate a blank pickle file
else:
    IgnoreList.LoadIgnoreList()