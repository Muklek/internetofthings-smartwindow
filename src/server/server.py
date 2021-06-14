from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from fetch import Fetch
from manual import Manual
from auto import Auto
from pattern import Pattern
from alarm import Alarm


app = FastAPI()
request = Fetch()
database = Manual()
prediction = Auto()
pattern = Pattern()
alarm = Alarm(request)


@app.get("/")
def read_root():
  return RedirectResponse("/docs")


@app.get("/smartwindow/v1/{operation}/pattern")
def read_item(operation):
  """
  The user has the ability of training or resetting a new neural
  network. The training is triggered through the client - nodeMCU - server
  Upon creation of the new model, it will be available for predictions.

  PARAMS:
  operation (string) - train or reset
  """
  if(operation == "train"):
    return pattern.train()

  elif(operation == "reset"):
    return pattern.reset()


@app.get("/smartwindow/v1/manual/patternSave={smartMode}&" +
                                 "windowOpen={windowMode}&" +
                                 "temperature={temperature}&" +
                                 "humidity={humidity}")
def read_item(smartMode,windowMode,temperature,humidity):
  """
  Everytime the user triggers a manual opening or closing of windows
  the nodeMCU will send data to the backend to store in the database
  so it can be used for training.
  If the user has enabled pattern saving the data will be saved on pattern.txt
  if the user has disabled pattern saving the data will be saved on manual.txt

  PARAMS:
  smartmode (string) - enabled or disabled - to save the data for machine learning
  windowMode (string) - open or close - what operation did the user trigger
  temperature (string) - temperature reading from the DHT11 sensor
  humidity (string) - humidity reading from the DHT11 sensor
  """
  return database.addNewEntry(smartMode,windowMode,temperature,humidity)


@app.get("/smartwindow/v1/auto/temperature={temperature}&" +
                               "humidity={humidity}")
def read_item(temperature,humidity):
  """
  The nodeMCU can trigger automatically to predict whether the window should
  be open or close based on the temperature and humidity DTH 11 sensor readings.
  The user can also trigger a manual prediction from the client.

  PARAMS:
  temperature (string) - temperature reading from the DHT11 sensor
  humidity (string) - humidity reading from the DHT11 sensor
  """
  return prediction.getOperation(temperature, humidity)


@app.get("/smartwindow/v1/alarm/{alarmType}")
def read_item(alarmType):
  """
  When the user requests to open or close window on sunset on sunrise
  nodeMCU will request for the exact amount of seconds left and will
  set an alarm to perform the operation.

  PARAMS:
  alarmType (string) - sunrise or sunset
  """
  if(alarmType == 'sunrise'):
    return alarm.getSunrise()
  elif(alarmType =='sunset'):
    return alarm.getSunset()



@app.get("/smartwindow/v1/data/type={dataType}&last={time}")
def read_item(dataType, time):
  """
  The sensor reading failure recovery nodeMCU will request data
  about the weather and update the internal state so it can continue
  performing. Weather data is fetched from openweathermap and it's cached
  to avoid too many requests from the nodeMCU.

  PARAMS:
  type (string) - sunset, sunrise, temperature and humidity
  last (string) - hour or minute - accuracy last hour or last minute
  """
  if(time == 'minute'):
    return request.getWeatherData(dataType, 'onecall')

  elif(time == 'hour'):
    return request.getWeatherData(dataType, 'weather')
