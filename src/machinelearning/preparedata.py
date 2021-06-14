class Preparedata:
  """
  Before training a new neural network is necessary to prepare
  the data. Data is collected from the database/baseline.txt
  and database/pattern.txt - the baseline is used if there are
  no data in the pattern which can happen when the user resets
  the neural network and current pattern data.
  """

  def __init__(self):
    self.patterns = []
    self.baseline = []

  def getData(self):
    patternData = open('../database/pattern.txt', 'r')

    for line in patternData:
      self.patterns.append(line)

    patternData.close()

    baselineData = open('../database/baseline.txt', 'r')
    for line in baselineData:
      self.baseline.append(line)

    baselineData.close()

  def mergeTrainigData(self, merge):
    """
    Merge is refered to the merging database of baseline.txt and
    pattern.txt - The user has the ability to train a new baseline
    model and reset the data.

    PARAMS:
    merge (boolean) whether is necessary to merge the pattern data
    """
    
    self.getData()

    trainingData = open('../machinelearning/training.csv', 'w')
    
    if(merge == True):
      for data in self.patterns:
        trainingData.write(data)

    for data in self.baseline:
      trainingData.write(data)

    trainingData.close()

    self.patterns = []
    self.baseline = []
