class Component():
    __implementedFunctions = ["Start", "Update"]
    def __init__(self, componentChild):
        self.child = componentChild        

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