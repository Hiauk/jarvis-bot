from BehaviourComponent import BehaviourComponent
import requests, bs4, json

class Weather(BehaviourComponent):
    def __init__(self):
        BehaviourComponent.__init__(self, self)    

    def GetWeatherInfo(self, room, event):
        args = event['content']['body'].split()

        postcode = args[1]

        url = 'https://www.bbc.co.uk/weather/0/' + postcode.lower()
        api_call = requests.get('http://api.postcodes.io/outcodes/' + postcode.lower())
        info = api_call.json()

        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text,features="html.parser")
        temp = soup.select('.wr-value--temperature--c')
        desc = soup.select('.wr-js-day-content-weather-type-description')
        room.send_text('In ' + ", ".join(info['result']['admin_ward']) + ' it is currently: ' + temp[0].getText() + ' - ' + desc[0].getText())

    def OnCommandReceived(self, room, event):
        args = event['content']['body'].split()
        commandCharRemoved = args[0][1:] #args[0].
        args.pop(0)
        if(commandCharRemoved == "weather"):
            self.GetWeatherInfo(room, event)

    