from InheritanceFinder import InheritanceFinder
import ast
import inspect
import os, importlib, re, sys
from collections import namedtuple

class ComponentContainer():
    componentScriptName = "BaseComponent"
    componentClassName = "BaseComponent"
    def __init__(self, folderPath, folderName, configPath):
        self.configPath = configPath # set the system path that loaded components draw their config files from
        self.components = {} # dictionary containing uninitialised script.class names (ChildScript.ChildClass) against a list of uninitalised class objects that implement 'ComponentParent.Component' and were pulled from that script
        self.GetComponentsFromScripts(folderPath, folderName)        

    def GetComponentsFromScripts(self, folderPath, folderName):
        pysearchre = re.compile('.py$', re.IGNORECASE) # create folder filter that get all .py files
        pythonScripts = list(filter(pysearchre.search, os.listdir(folderPath))) # get all .py file from the folderPath directory as a list
        moduleDict = self.LoadScriptsAsModules(pythonScripts, folderName) # create python module from the scripts and load then into a dictionary against their script name
        componentDict = self.CheckScriptsForComponents(folderPath, pythonScripts) # finds all class definitions that implement 'Component' and loads them into a dictionary against their script name
        
        # e.g. {"ChildScript", ["ChildClass","AnotherChildClass"]}
        for scriptName in componentDict.keys(): # scriptName = "ChildScript"
            for componentClass in componentDict[scriptName]: # e.g. componentDict[aKey] = ["ChildClass","AnotherChildClass"], iteration 1 componentClasses = "ChildClass"
                loadedComponentClass = self.GetClassFromModule(moduleDict[scriptName], componentClass) # Get the childComponent class from the generated .Child python module
                self.components.update({scriptName+'.'+componentClass: loadedComponentClass})

    ## Takes a set of script names and the name of the folder they exist in then imports them into the project as a python module in the format pythonScript.packageName
    ## Input:
    ##  pythonScripts:  a list of python scripts {script1.py, script2.py, script3.py}
    ##  packageName:    name of the folder that contains the list of scripts i.e. 'ScriptFolder'
    ## Returns: A dictionary of containing a list of {Script Name : Python Module}
    def LoadScriptsAsModules(self, pythonScripts, packageName):
        moduleDict = {} # initalise a dictionary for return
        form_module = lambda fp: '.' + os.path.splitext(fp)[0] # function to remove trailing file extension from given script
        plugins = map(form_module, pythonScripts) # remove trailing file extensions from the given scripts
        for plugin in plugins:
             if not plugin.startswith('__'): # make sure this is not a python specfic module
                 # Add an entry to the dictionary with the scripts name against its loaded module {Script Name : Python Module}
                 moduleDict.update({plugin[1:len(plugin)] : importlib.import_module(plugin, package=packageName)})
        return moduleDict

    def GetClassFromModule(self, module, className):
        retrivedClass = getattr(module, className) # Get the childComponent class from the generated .Child python module
        return retrivedClass

    def GetClassesFromFile(self, filePath):
        f=open(filePath,'r') # read in entire file
        p = ast.parse(f.read()) # parse through ast to get syntax tree
        classes = [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)] # walk through the syntax tree and extract all the class definitions
        return classes
    
    def CheckScriptsForComponents(self, folderPath, scriptNames):        
        componentDict = {}
        parentFinder = InheritanceFinder()
        for script in scriptNames:
            parentFinder.LoadScript(os.path.join(folderPath, script))
            childClasses = parentFinder.FindChildren(ComponentContainer.componentClassName)
            componentDict.update({ script.split('.')[0] : childClasses }) # add the list of capture childClasses to a dictionary against the script they were from
        return componentDict