from ComponentLoader import ComponentContainer

componentContainer = ComponentContainer("H:\\Programming\\PythonStuff\\python_componentpattern\\Components", "Components") 

for aComponent in componentContainer.components.values():
    test = aComponent() # Init a Child component
    callableFunctions = test.GetCallableFunctions()
    for aFunction in callableFunctions.values():
        if(aFunction != None):
            aFunction()

class BotModules():
    def __init__(self):
        self.componentContainers = {} # dictionary containing a folder path against a ComponentContainer
        self.classContainers = {} # dictionary containing instantable class definitions for loaded 
        self.moduleContainer = []
    
    # creates a new component container from the scripts in the given folderPath and loads ut into self.componentContainers
    def LoadClasses(self, folderPath):
        folderName = folderPath.split('\\')
        folderName = folderName[len(folderName)]
        newContainer = ComponentContainer(folderPath, folderName)
        self.classContainers.update({folderPath : newContainer})
    
    @staticmethod
    def Instantiate(module):
        pass

    def CallMethodOnAll(self):
        for aContainer in self.componentContainers.values():
            for aComponent in aContainer.components.values():
                test = aComponent() # Init a Child component
                callableFunctions = test.GetCallableFunctions()
                for aFunction in callableFunctions.values():
                    if(aFunction != None):
                        aFunction()

class Module():
    def __init__(self, filePath, name, classDefinition):
        self.filePath = filePath
        self.name = name
        self.callableFunctions = {}