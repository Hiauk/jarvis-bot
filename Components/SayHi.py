from ComponentParent import Component
import re

class HiResponse(Component):
    def __init__(self):
        Component.__init__(self, self)
    
    def OnMessageReceived(self, room, event):
        if re.search("Hi ", event['content']['body']):
            # Somebody said hi, let's say Hi back
            room.send_text("Hi, " + event['sender'])
