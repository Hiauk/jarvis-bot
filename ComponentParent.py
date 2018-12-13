class Component():
    __implementedFunctions = ["Start", "Update", "OnMessageReceived", "OnCommandReceived"]
    __loadedComponents = {} # Holds values containing loaded components against thier type, used by getComponent
    def __init__(self, componentChild):
        self.child = componentChild
        Component.__loadedComponents.update({type(componentChild) : componentChild})

    @staticmethod # returns a list of functions that the component parent checks its child implementations for
    def GetImplementableFunctionsList():
        return Component.__implementedFunctions

    ## Returns: A dictionary containing function names against callable functions from the object, the function value is 'None' if not callable on the object
    ##          dictionary = {functionName, functionReference} e.g. {"Start", Start()}
    def GetCallableFunctions(self):
        callableFunctions = {}
        for aFunction in Component.__implementedFunctions: # For our declared functions that we want to be able to called elsewhere
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
            return Component.__loadedComponents[componentType]        
        except Exception:
            return None
            