from ComponentParent import Component

class Roll(Component):
    def __init__(self):
        Component.__init__(self, self)    

    def Roll(self, room, event):
        args = event['content']['body'].split()

        dice = args[1]
        info = dice.split("d")
        
        room.send_text('Rolling: ' + info[0] + ' ' + info[1] + ' sided dice')

    def OnCommandReceived(self, room, event):
        args = event['content']['body'].split()
        commandCharRemoved = args[0][1:] #args[0].
        args.pop(0)
        if(commandCharRemoved == "roll"):
            self.Roll(room, event)

    