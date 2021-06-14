from keras.models import Sequential
from keras.layers import Dense

class Model:
  """
  The purpose of this class is to encapsulate the model
  creation so when it is required to create a new model
  the system can just call buildModel() and using the
  predifed variables will create the model.
  """
  
  def __init__(self):
    self.loss  = 'binary_crossentropy'
    self.optimizer = 'adam'
    self.metrics = ['accuracy']
    self.activation = ['relu', 'sigmoid']

  def buildModel(self):
    # create model
    model = Sequential()
    model.add(Dense(2, input_dim=2, activation=self.activation[0]))
    model.add(Dense(1, activation=self.activation[1]))
    # Compile model
    model.compile(loss=self.loss, optimizer=self.optimizer, metrics=self.metrics)
    return model

  def getModel(self):
    return self.buildModel()
