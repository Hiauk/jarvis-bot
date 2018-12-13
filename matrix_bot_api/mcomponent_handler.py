"""
Defines a matrix bot handler for commands
"""
from matrix_bot_api.mhandler import MHandler

class MComponentHandler(MHandler):

    # handle_callback - Function to call if message contains command
    def __init__(self, handle_callback):
        MHandler.__init__(self, self.test_command, handle_callback)

    # Function called by Matrix bot api to determine whether or not to handle this message
    def test_command(self, room, event):
        return True # We want every message