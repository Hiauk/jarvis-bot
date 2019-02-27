from BehaviourComponent import BehaviourComponent
import re

class HiResponse(BehaviourComponent):
    def __init__(self):
        BehaviourComponent.__init__(self, self)
    
    def OnMessageReceived(self, room, event):
        if re.search("Hi ", event['content']['body']):
            # Somebody said hi, let's say Hi back
            room.send_text("Hi, " + event['sender'])
