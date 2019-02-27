from BehaviourComponent import BehaviourComponent
import os

class Help(BehaviourComponent):
    defaultHelpFileName = "CommandHelp.md"
    def __init__(self):
        BehaviourComponent.__init__(self, self)

    def Start(self):
        self.helpPath = self.config.GetKey("helpfile") # get path to helpfile
        if(self.helpPath == None): # if there was none available
            self.__InitConfig()

    def __InitConfig(self):
        self.helpPath = os.path.join(os.path.dirname(__file__), Help.defaultHelpFileName) # Set default value for next time
        self.config.SetKey("helpfile", self.helpPath) # Set default value for next time
        if(os.path.isfile(self.helpPath) == False): # if no helpfile even exists at this location
            helpFileStream = open(self.helpPath, 'a') # create new helpfile
            helpFileStream.write("Theres nothing here!") # start the file

    def GetHelpContents(self):
        file = open(self.helpPath,"r+")
        text = file.read()
        file.close()
        return text

    def OnCommandReceived(self, room, event):
        args = event['content']['body'].split()
        commandCharRemoved = args[0][1:] #args[0].
        args.pop(0)
        if(commandCharRemoved == "Help"):
            helpText = self.GetHelpContents()
            room.send_text(helpText)