from BehaviourComponent import BehaviourComponent

class Parrot(BehaviourComponent):
    def __init__(self):
        BehaviourComponent.__init__(self, self)

    def Start(self):
        print("Woa, I'm Alive")
    
    def OnCommandReceived(self, room, event):        
        args = event['content']['body'].split()
        commandCharRemoved = args[0][1:] #args[0].
        args.pop(0)
        if(commandCharRemoved == "Parrot"):
            room.send_text(' '.join(args))