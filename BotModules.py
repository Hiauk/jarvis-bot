from ComponentLoader import ComponentContainer
from ComponentParent import Component

class BotModules():
    def __init__(self):
        #self.componentContainers = {} # dictionary containing a folder path against a ComponentContainer
        #self.classContainers = {} # dictionary containing instantable class definitions for loaded 
        self.moduleContainer = []
        self.functionContainer = {} # {functionName, function} - {"Update" : Update()}
        for methodName in Component.GetImplementableFunctionsList():
            self.functionContainer.update({methodName : []})
    
    # creates a new component container from the scripts in the given folderPath and loads ut into self.componentContainers
    def LoadClasses(self, folderPath):
        folderName = folderPath.split('\\') # seperate out the folder name from the path
        folderName = folderName[len(folderName)-1]
        newContainer = ComponentContainer(folderPath, folderName)
        for aComponent in newContainer.components.values():
            newComponent = aComponent() # Init a Child component
            callableFunctions = newComponent.GetCallableFunctions()
            self.moduleContainer.append(newComponent)
            # skim out all of the functions that are unused
            for functionName in callableFunctions.keys():
                if(callableFunctions[functionName] != None):
                    self.functionContainer[functionName].append(callableFunctions[functionName])
    
    @staticmethod
    def Instantiate(module):
        pass

    def CallMethodOnAll(self, methodName):
        for aFunction in self.functionContainer[methodName]:
            aFunction()

class Module():
    def __init__(self, filePath, name, classDefinition):
        self.filePath = filePath
        self.name = name
        self.callableFunctions = {}

#Testing code
#botModules = BotModules()
#botModules.LoadClasses("H:\\Programming\\PythonStuff\\python_componentpattern\\Components")
#botModules.CallMethodOnAll("Start")