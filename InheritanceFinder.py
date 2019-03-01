from modulefinder import ModuleFinder
import ast
from collections import namedtuple

class InheritanceFinder():
    __classList = []
    __importList = []
    def __init__(self):
        pass

    # Loads a given script as a syntax tree then extracts the internal class and import definitions for use later
    def LoadScript(self, scriptPath):
        Import = namedtuple("Import", ["module", "name", "alias"]) # declare a tuple to contain returned import nodes
        importInfo = []
        f=open(scriptPath,'r') # read in entire file
        p = ast.parse(f.read()) # parse through ast to get syntax tree
        # walk through the syntax tree and extract information pertaining to class definitions and imported scripts
        classNodes = [] 
        for node in ast.walk(p):
            module = []
            if(isinstance(node, ast.ClassDef)): # if the node is a class definition node
                classNodes.append(node) # add it to our definitions list
            # check for import definition nodes
            if isinstance(node, ast.Import): # we don't care about straight imports, we want imported classes i.e. import sys
                module = []
            elif isinstance(node, ast.ImportFrom): # save the class that is imported from i.e. import MyClass from MyPythonScript
                module = node.module.split('.')
            else:
                continue # this is not an import definition, skip to next item in the syntax tree

            for n in node.names:                
                if(len(module) > 0): # store all the imported classes for comparison later
                    importInfo.append(Import(module[0], n.name.split('.')[0], n.asname)) # create tuple from this node
        InheritanceFinder.__classList = classNodes
        InheritanceFinder.__importList = importInfo

    # returns a list of classes in the loaded script that inherit from a given parentClass
    def FindChildren(self, parentClass):
        foundChildren = []
        for childClass in InheritanceFinder.__classList:
            if(self.IsParent(parentClass, childClass.name)):
                foundChildren.append(childClass.name)
        return foundChildren

    # returns true or false if the given childClass's inheritance tree contains a given parentClass
    def IsParent(self, parentClass, childClass):
        childClassNode = None
        for node in InheritanceFinder.__classList: # check if the node we want is part of this class
            if(node.name == childClass):
               childClassNode = node
        if(childClassNode == None or len(childClassNode.bases) == 0): # return false if the either doesn't exist or doesn't inherit anything (its top of the chain!)
            return False    

        matchedImports = {} # match the childClass's base classes (those it directly inherits) to the relevant imports
        for baseClass in childClassNode.bases: 
            for importedClass in InheritanceFinder.__importList:
                # if this import matches the base class 
                if(baseClass.id == importedClass.alias or (baseClass.id == importedClass.name and importedClass.alias == None)):
                    matchedImports.update({baseClass : importedClass})
        #loop through the dictionary and check if any of these base class imports match the class we are looking for
        for importedClass in matchedImports.values():
            if(importedClass.name == parentClass):
                return True
        
        finder = ModuleFinder()
        for importedClass in matchedImports.values():
            foundScript = finder.find_module(importedClass.module,path=None) # contains path to file if found
            parentFinder = InheritanceFinder()
            parentFinder.LoadScript(foundScript[1]) # path to found module
            if(parentFinder.IsParent(parentClass, importedClass.name)): # recusively check if this base class inherits from the parentClass
                return True
        
        return False # we've exhausted all possible inheritance paths and as such this does not inherit from parentClass

#myFinder = InheritanceFinder()
#myFinder.LoadScript("H:\\Programming\\PythonStuff\\Jarvis\\Test\\Parrot.py")
#result = myFinder.IsParent('BaseComponent', 'SecondClass')
#print(result)