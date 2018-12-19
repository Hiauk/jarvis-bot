from ComponentParent import Component
import requests, bs4

class Weather(Component):
    def __init__(self):
        Component.__init__(self, self)    

    def GetWeatherInfo(self, room, event):
        url = 'https://www.bbc.co.uk/weather/2643743'

        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text,features="html.parser")
        temp = soup.select('.wr-value--temperature--c')
        desc = soup.select('.wr-js-day-content-weather-type-description')
        room.send_text('In London it is currently: ' + temp[0].getText() + ' - ' + desc[0].getText())

    def OnCommandReceived(self, room, event):
        args = event['content']['body'].split()
        commandCharRemoved = args[0][1:] #args[0].
        args.pop(0)
        if(commandCharRemoved == "weather"):
            self.GetWeatherInfo(room, event)