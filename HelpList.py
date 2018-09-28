

def GetHelpContents(filepath):
    file = open(filepath,"r+")
    text = file.read()
    file.close()
    return text