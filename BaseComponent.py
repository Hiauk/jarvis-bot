import os
import yaml
import copy 

class BaseComponent():
    __implementedFunctions = {} # Holds a dictionary of component types against a list of functions they can implement
    __loadedComponents = {} # Holds values containing loaded components against thier type, used by getComponent
    def __init__(self, componentChild, implementedFunctions):
        self.child = componentChild
        BaseComponent.__implementedFunctions.update({type(componentChild) : implementedFunctions})
        BaseComponent.__loadedComponents.update({type(componentChild) : componentChild})        

    @staticmethod # returns a list of functions that the component parent checks its child implementations for
    def GetImplementableFunctionsList():
        return BaseComponent.__implementedFunctions

    ## Returns: A dictionary containing function names against callable functions from the object, the function value is 'None' if not callable on the object
    ##          dictionary = {functionName, functionReference} e.g. {"Start", Start()}
    def GetCallableFunctions(self):
        callableFunctions = {}
        for aFunction in BaseComponent.__implementedFunctions[type(self.child)]: # For our declared functions that we want to be able to called elsewhere
            retrievedFunction = getattr(self, aFunction, None) # Try to find this function on the object
            if callable(retrievedFunction): # if what we get back is a callable function
                callableFunctions.update({aFunction : retrievedFunction}) # add it to the dictionary against the function name
            else:
                callableFunctions.update({aFunction : None}) # if we get something we can't call back, list 'None' against the function name
        return callableFunctions

    ## Input  : type() of a Component
    ## Returns: Instantiated object of given componentType if one exists, None if not found
    @staticmethod
    def GetComponent(componentType):
        try:
            return BaseComponent.__loadedComponents[componentType]        
        except Exception:
            return None