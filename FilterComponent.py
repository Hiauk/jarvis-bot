from ConfigurableComponent import ConfigurableComponent

class FilterComponent(ConfigurableComponent):
    __filterFunctions = ["Start", "OnMessageReceived"]
    def __init__(self, componentChild):
        self.child = componentChild
        ConfigurableComponent.__init__(self, componentChild, FilterComponent.__filterFunctions)