from BaseComponent import BaseComponent
import os
import yaml
import copy 

class ConfigurableComponent(BaseComponent): # extends the BaseComponent class to provide simple access to configuration files to any components that implement this
    def __init__(self, componentChild, implementedFunctions):
        self.child = componentChild
        self.config = Config(Config.FilenameFromType(type(componentChild)))
        BaseComponent.__init__(self, componentChild, implementedFunctions)

class Config():
    configPath = "" # system path to folder with component config files

    def __init__(self, configName):
        path = os.path.join(self.configPath, configName)
        if(Config.__CanAccessConfig(path)): #if config file detected
            self.__configFile = path
        else:            
            self.__configFile = None # No config found, config is created when the first key is set / we don't want to create configs if not required
        self.__configName = configName+".yml"
        self.__config = {}

    def GetKey(self, key):
        if(self.__configFile == None):
            return None # no config, so definately None
        else:
            return self.__TryGetKey(key) # key value or None
    
    def SetKey(self, key, value):
        if(self.__configFile == None): #No config loaded
            self.__InitConfig() # Create the config file
        self.__TrySetKey(key, value)
        

    # Sets ensures that the self.__configPath variable is set and that there is a file at this location (creating it if neccissary)
    def __InitConfig(self):
        path = os.path.join(Config.configPath, self.__configName)
        if(Config.__CanAccessConfig(path)): # check if config exists now
            self.__configFile = path # it exists now for some reason, set it
            return
        else:
            open(path, 'a').close() # create the config file


    ## Loads the yaml contents of the previously set config file self.__configFile into the Config object
    def ReloadConfig(self):
        self.__config = yaml.safe_load(self.__configFile)

    ## Loads the yaml contents of the previously set config file self.__configFile into the Config object and sets the serving file location to the given path
    def LoadConfig(self, pathToConfig):
        self.__config = yaml.safe_load(pathToConfig)
        self.__configFile = pathToConfig
    
    ## Saves the currently help config data to the config file
    def __SaveConfig(self):
        with open(self.__configFile, 'w') as f:
            yaml.dump(self.__config, f)

    ## Checks if a key exists in config file
    ## Returns the keys value pair or None
    def __TryGetKey(self, key):        
        if(key in self.__config): # check if key exists and return as appropriate
            return self.__config[key]
        else:
            return None

    ## Safely updates and saves a given key value to both the objects held config and the config disk file
    ## Data is unchanged if operation unsuccessful
    def __TrySetKey(self, key, value):
        configCopy = copy.deepcopy(self.__config)
        try:
            self.__config.update({key : value})
            self.__SaveConfig()
        except:
            print("ERROR - Unable to set key: " + str(key) + " to Value: " + str(value))
            self.__config = configCopy # if we failed, ensure config data remains unchanged

    ## Returns True or False if a given file can be opened
    @staticmethod
    def __CanAccessConfig(configPath):
        try: # open the config file
            filestream = open(configPath)
            filestream.close()
            return True
        except:
            return False
    
    ## Generates a filename from a given class type
    ## <class 'Components.ComponentExample.ChildComponent'> = ComponentExample_ChildComponent
    @staticmethod
    def FilenameFromType(classType): # input example: <class 'Components.ComponentExample.ChildComponent'>
        splitByApostraphe = str(classType).split("'") # [<class ', Components.ComponentExample.ChildComponent, '>]
        splitByStop = splitByApostraphe[1].split(".") # [Components, ComponentExample, ChildComponent]

        iterSplit = iter(splitByStop)
        # skip the Component part and first valid part (they ALL inherit from components)
        next(iterSplit) 
        next(iterSplit)
        fileName = splitByStop[1] # should always have two things, skip the first so that there is no preceeding "_"
        for namePiece in iterSplit:
            fileName += "_" + namePiece
        return fileName

   
            