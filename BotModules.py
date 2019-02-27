import os

from ComponentLoader import ComponentContainer
from ComponentParent import Component
#from Components.TestChild import childComponent

class BotModules():
    def __init__(self):
        self.moduleContainer = []
        # Initialise function container with the names of all the potential functions as defined by Component
        self.functionContainer = {} # {functionName, function} - {"Update" : Update()}
        for methodName in Component.GetImplementableFunctionsList():
            self.functionContainer.update({methodName : []})
    
    # creates a new component container from the scripts in the given folderPath and loads ut into self.componentContainers
    def LoadClasses(self, folderPath, configPath):
        folderName = os.path.split(folderPath) # seperate out the folder name from the path
        folderName = folderName[len(folderName)-1]
        newContainer = ComponentContainer(folderPath, folderName, configPath)
        for aComponent in newContainer.components.values():
            newComponent = aComponent() # Init a Child component
            callableFunctions = newComponent.GetCallableFunctions()
            self.moduleContainer.append(newComponent)
            # skim out all of the functions that are unused
            for functionName in callableFunctions.keys():
                if(callableFunctions[functionName] != None):
                    self.functionContainer[functionName].append(callableFunctions[functionName])

    def CallMethodOnAll(self, name, *args):
        for aFunction in self.functionContainer[name]:
            aFunction(*args)

class Module():
    def __init__(self, filePath, name, classDefinition):
        self.filePath = filePath
        self.name = name
        self.callableFunctions = {}

#Testing code
botModules = BotModules()
botModules.LoadClasses("H:\\Programming\\PythonStuff\\Jarvis\\Test", "H:\\Programming\\PythonStuff\\Jarvis\\Test")
print("Start")
botModules.CallMethodOnAll("Start")

#component = Component.GetComponent(childComponent) # also enable class load at top of script
#component.Start()