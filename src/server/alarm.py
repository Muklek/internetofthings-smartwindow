from datetime import datetime

class Alarm:
  """
  When the user requests to open or close window on sunset on sunrise
  nodeMCU will request for the exact amount of seconds left and will
  set an alarm to perform the operation.
  Alarm class encapsulates the necessary fetching and calculations and
  return the exact amount of seconds left.
  """
  def __init__(self, fetch):
    self.fetch = fetch

  def getSunrise(self):
    currentTime = int(datetime.now().timestamp())
    sunriseTime = int(self.fetch.getWeatherData('sunrise', 'weather'))

    return currentTime - sunriseTime

  def getSunset(self):
    currentTime = int(datetime.now().timestamp())
    sunsetTime = int(self.fetch.getWeatherData('sunset', 'weather'))

    return sunsetTime - currentTime

