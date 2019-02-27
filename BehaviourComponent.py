from ConfigurableComponent import ConfigurableComponent

class BehaviourComponent(ConfigurableComponent):
    __behaviourFunctions = ["Start", "Update", "OnMessageReceived", "OnCommandReceived"]
    def __init__(self, componentChild):
        self.child = componentChild
        ConfigurableComponent.__init__(self, componentChild, BehaviourComponent.__behaviourFunctions)