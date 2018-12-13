from ComponentParent import Component

class Parrot(Component):
    def __init__(self):
        Component.__init__(self, self)

    def Start(self):
        print("Parrot - Start")
    
    def Update(self):
        pass
    
    def OnMessageReceived(self, room, event):
        pass
    
    def OnCommandReceived(self, room, event):        
        args = event['content']['body'].split()
        commandCharRemoved = args[0][1:] #args[0].
        args.pop(0)
        if(commandCharRemoved == "Parrot"):
            room.send_text(' '.join(args))