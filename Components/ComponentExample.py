from BehaviourComponent import BehaviourComponent

class ChildComponent(BehaviourComponent):
    def __init__(self):
        BehaviourComponent.__init__(self, self)

    def Start(self):
        print("TestChild - Start")

    def Update(self):
        pass
        #print("TestChild - Update")
    
    def OnMessageReceived(self, room, event):
        print("room: " + str(room) + "\tevent: " + str(event)) # prints details about all received messages to console
    
    def OnCommandReceived(self, room, event):
        pass