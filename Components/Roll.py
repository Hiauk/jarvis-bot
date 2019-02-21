from ComponentParent import Component
import random

class Roll(Component):
    def __init__(self):
        Component.__init__(self, self)    

    def Roll(self, room, event):
        args = event['content']['body'].split()

        dice = args[1]
        info = dice.split("d")
        for x in range(int(info[0])):
            room.send_text(str(random.randint(1,int(info[1]) + 1)))

    def OnCommandReceived(self, room, event):
        args = event['content']['body'].split()
        commandCharRemoved = args[0][1:] #args[0].
        args.pop(0)
        if(commandCharRemoved == "roll"):
            self.Roll(room, event)

    