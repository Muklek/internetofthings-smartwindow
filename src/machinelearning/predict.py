
from keras.models import model_from_json

class Predict:
  """
  When nodeMCU triggers the auto smartmode or manual
  prediction, the Predict class will load the latest
  model trained and encapsulate all the necessary
  steps to predict whether the window should be open
  or close.
  """

  def __init__(self):
    self.json_name = '../machinelearning/model.json'
    self.weights_name = '../machinelearning/model.h5'

    self.model = None
    self.loadModel()

  def loadModel(self):
    print("Loading model...")
    json_file = open(self.json_name, "r")
    loaded_model_json = json_file.read()
    json_file.close()

    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(self.weights_name)

    self.model = loaded_model

  def getOperation(self, temperature, humidity):
    """
    The prediction will give whether the window should
    be opened or closed. The function will make all the
    necessary steps to clean the input coming from nodeMCU
    and trigger the prediction.

    PARAMS:
    Temperature (string) coming from the nodeMCU sensor reading
    humidity (string) coming from the nodeMCU sensor reading
    """

    temperature = float(temperature)
    humidity = float(humidity)

    data = [[temperature, humidity]]

    print("Started prediction...")
    prediction = self.model.predict_classes(data)

    return prediction[0][0]
