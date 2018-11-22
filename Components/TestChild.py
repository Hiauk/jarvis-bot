from ComponentParent import Component

class childComponent(Component):
    def __init__(self):
        Component.__init__(self, self)

    def Start(self):
        print("TestChild - Start")

    def Update(self):
        print("TestChild - Update")