import requests
from datetime import datetime


class Fetch:
  """
  The sensor reading failure recovery nodeMCU will request data
  about the weather and update the internal state so it can continue
  performing. Weather data is fetched from openweathermap and it's cached
  to avoid too many requests from the nodeMCU.
  The Fetch class encapsulates all the functions and necessary steps to clean
  the data and return only the data requested.
  The Fetch class also keeps track of the time and every 5 minutes request new
  data from the openweathermap (when it's required).
  """

  def __init__(self):

    self.lastTimeFetched = 0
    self.hourlyData = None
    self.minuteData = None

    self.url = 'https://api.openweathermap.org/data/2.5/'
    self.units = 'metric'
    self.features = ['minute', 'hourly', 'daily', 'alert']
    self.cities = [{'country':'uk','name':'Portsmouth','lat':'50.799','lon':'-1.0913'}]
    self.token = '13480858be03647773545238cf2262ce'


  def buildUrl(self, callType):

    url = self.url + callType + '?'

    if(callType == 'onecall'):
      url += 'lat=' + self.cities[0]['lat'] + '&lon=' + self.cities[0]['lon']
      url += '&units=' + self.units
      url += '&exclude=' + self.features[1] + ',' + self.features[2] + ',' + self.features[3]
      url += '&appid=' + self.token
    else:
      url += 'q=' + self.cities[0]['name'] + ',' + self.cities[0]['country']
      url += '&units=' + self.units
      url += '&appid=' + self.token

    return url

  def fetchWeatherData(self, callType):

    newTime = int(datetime.utcnow().timestamp())

    if((callType == 'onecall' and self.minuteData == None) or 
       (callType == 'weather' and self.hourlyData == None) or
       ((newTime - self.lastTimeFetched) > 300)):

      url = self.buildUrl(callType)

      try:
        print("Fetching weather data from openweathermap")
        response = requests.get(url)
      except:
        print("Error fetching data from: " + url)
        return False
      
      data = response.json()
      self.lastTimeFetched = newTime

      if(callType == 'onecall'):
        self.minuteData = data
      else:
        self.hourlyData = data

    return True

  def getWeatherData(self,  dataType, callType):

    fetched = self.fetchWeatherData(callType)

    if(not fetched):
      return "Unable to fetch data from server"

    elif(callType == 'onecall'):
      if(dataType == 'temperature'):
        return self.minuteData['current']['temp']

      elif(dataType == 'humidity'):
        return self.minuteData['current']['humidity']

      elif(dataType == 'sunset'):
        return self.minuteData['current']['sunset']
    
    elif(callType == 'weather'):
      if(dataType == 'temperature'):
        return self.hourlyData['main']['temp']

      elif(dataType == 'humidity'):
        return self.hourlyData['main']['humidity']

      elif(dataType == 'sunset'):
        return self.hourlyData['sys']['sunset']

      elif(dataType == 'sunrise'):
        return self.hourlyData['sys']['sunrise']

    return "Data not available"
