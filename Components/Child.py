from ComponentParent import Component

class childComponent(Component):
    def __init__(self):
        Component.__init__(self, self)

    def Start(self):
        print("Child - Start")

class notAChild():
    def __init__(self):
        pass

    def Start(self):
        print("Child - Start")

class anotherChildComponent(Component):
    def __init__(self):
        Component.__init__(self, self)

    def Start(self):
        print("anotherChild - Start")