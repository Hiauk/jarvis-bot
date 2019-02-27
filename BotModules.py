import os
from ComponentLoader import ComponentContainer
#from Components.TestChild import childComponent

class BotModules():
    def __init__(self):
        self.moduleContainer = []
        # Initialise function container with the names of all the potential functions as defined by Component
        self.functionContainer = {} # {functionName, function} - {"Update" : Update()}
    
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
                    if(self.functionContainer.__contains__(functionName) == False): # if we've never seen this function before
                        self.functionContainer.update({functionName : []}) # init this function in the dictionary
                    self.functionContainer[functionName].append(callableFunctions[functionName]) # add this function to its assigned list in the dictionary


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