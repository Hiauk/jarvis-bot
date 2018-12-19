from ComponentParent import Component
import requests, bs4

class Train(Component):
    def __init__(self):
        Component.__init__(self, self)    

    def GetTrainInfo(self, room, event):
        args = event['content']['body'].split()

        station1 = args[1]
        station2 = args[2]

        url = 'http://ojp.nationalrail.co.uk/service/ldbboard/dep/' + station1 + '/' + station2 +'/To'

        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text,features="html.parser")
        table = soup.find('table')
        table_body = table.find('tbody')
        data = []
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

        output = ""
        for row in data:
            if "Details" not in row[3]:
                output += row[0] + ' to ' + row[1] + ' is "' + row[2] + '" on platform ' + row[3] + '.\n'
            else:
                output += row[0] + ' to ' + row[1] + ' is "' + row[2] + '". Platform is not known.\n'

        room.send_text(output)

    def OnCommandReceived(self, room, event):
        args = event['content']['body'].split()
        commandCharRemoved = args[0][1:] #args[0].
        args.pop(0)
        if(commandCharRemoved == "train"):
            self.GetTrainInfo(room, event)