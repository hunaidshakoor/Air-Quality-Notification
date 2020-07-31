import requests
from datetime import datetime
from twilio.rest import Client

AIR_KEY = '7e5399df-64a9-49db-9542-b4ab8aee87bc'

class AirQuality:

    def __init__(self, city):
        self.city = city
        self.state = 'California'
        self.country = 'USA'

    def get_data(self):
        requrl = 'http://api.airvisual.com/v2/city?city={0}&state={1}&country={2}&key={3}'.format(self.city, self.state, self.country, AIR_KEY)
        response = requests.get(requrl)
        content = response.json()
        return content

    def get_aqi(self):
        content = self.get_data()
        self.aqi = content["data"]["current"]["pollution"]["aqius"]
        isodate = content["data"]["current"]["pollution"]["ts"]
        date = datetime.fromisoformat(isodate[:-1])
        self.date = date.date()
        return self.create_message()

    def aqi_status(self):
        status = None
        if self.aqi < 51:
            status = 'Good, Air Quality is satisfactory'
        elif 51 <= self.aqi < 101:
            status = 'Moderate, Air quality is acceptable. However, ' \
                     'there may be a risk for some people, particularly those who ' \
                     'are unusually sensitive to air pollution.'
        elif 101 <= self.aqi < 151:
            status = 'Unhealthy for sensitive groups. Members of sensitive groups may experience health effects.' \
                     ' The general public is less likely to be affected.'
        elif 151 <= self.aqi < 201:
            status = 'Unhealthy, Some members of the general public may experience health effects; ' \
                     'members of sensitive groups may experience more serious health effects.'
        elif 201 <= self.aqi < 301:
            status = 'Very Unhealthy. The risk of health effects is increased for everyone.'
        else:
            status = 'Hazardous. Health warning of emergency conditions: everyone is more likely to be affected.'
        return status


    def create_message(self):
        status = self.aqi_status()
        message = 'Hello! Today on {0} the Air quality is {1}. \n Status: {2}'.format(self.date, self.aqi, status)
        return message

#Uses twilio API to send SMS
class SendText:

    def __init__(self, message):
        self.SID = 'AC040fbdffa5e8234c789f581a77954971'
        #Add auth Token
        self.Token = ''

        self.message = message

        #Phone number hidden
        self.tonum = ''
        self.fromnum = '+16305230961'

    def send_message(self):
        client = Client(self.SID, self.Token)
        client.api.account.messages.create(to = self.tonum, from_ = self.fromnum,
                              body = self.message)

def main():
    aqi = AirQuality('San Francisco')
    message = aqi.get_aqi()
    send = SendText(message)
    send.send_message()

if __name__ == "__main__":
    main()