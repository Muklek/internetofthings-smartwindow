import sys
sys.path.append('../')

from machinelearning.predict import Predict


class Auto:
  """
  The nodeMCU can trigger automatically to predict whether the window should
  be open or close based on the temperature and humidity DTH 11 sensor readings.
  The user can also trigger a manual prediction from the client.
  Auto class encapsulates the prediction class and loads the model.
  """
  def __init__(self):
    self.prediction = Predict()

  def getOperation(self, temperature, humidity):
    """
    The params are coming from the NodeMCU sensor readings
    temperature (string) - temperature reading from the DHT11 sensor
    humidity (string) - humidity reading from the DHT11 sensor
    """
    return str(self.prediction.getOperation(temperature,humidity))
