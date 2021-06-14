import sys
sys.path.append('../')

from datetime import datetime
from machinelearning.training import Training


class Pattern:
  """
  The user has the ability of training or resetting a new neural
  network. The training is triggered through the client - nodeMCU - server
  Upon creation of the new model, it will be available for predictions.

  The pattern class encapsulates all the necessary steps to train a new model
  as well as keeps track of the timings to avoid the user triggering too many
  times model training.
  """

  def __init__(self):
    self.lastTimeTrained = 0
    self.lastTimeReset = 0
    self.training = Training()

  def train(self):
    newTime = int(datetime.utcnow().timestamp())

    if((newTime - self.lastTimeTrained) > 300):
      self.training.start()
      self.lastTimeTrained = newTime
      return "Finished training"

    else:
      return "Model trained recently, unable to retrain model"

  def deletePatternEntries(self):
    newPatternEntry = ''
    patternData = open('../database/pattern.txt', 'w')
    patternData.write(newPatternEntry)
    patternData.close()

  def reset(self):
    newTime = int(datetime.utcnow().timestamp())

    if((newTime - self.lastTimeReset) > 300):
      self.deletePatternEntries()
      self.training.start(False)
      self.lastTimeReset = newTime
      return "Reset model successfully"
      
    else:
      return "Reset model recently, unable to reset model"
