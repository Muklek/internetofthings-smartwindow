import pandas
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold

import sys
sys.path.append('../machinelearning')

from model import Model
from preparedata import Preparedata

model = Model()
data = Preparedata()

class Training:
  """
  The training class is primary used to encapsulate all the necessary
  steps to train a new neural network: Data processing, model creation,
  model training and model saving.
  """

  def __init__(self):
    self.epochs = 15
    self.batch_size = 10
    self.verbose = 1
    self.dataset_name = '../machinelearning/training.csv'
    
    self.model = model.getModel()

  def loadData(self, merge):
    print("Loading data for training")
    data.mergeTrainigData(merge)
    dataframe = pandas.read_csv(self.dataset_name, header=None)
    dataset = dataframe.values
    inputValues = dataset[:,0:2].astype(float)
    outputValues = dataset[:,2]

    return inputValues, outputValues

  def encodeLabel(self, outputLabels):
    encoder = LabelEncoder()
    encoder.fit(outputLabels)
    encoded_outputLabels = encoder.transform(outputLabels)
    return encoded_outputLabels

  def saveModel(self):
    model_json = self.model.to_json()
    with open("../machinelearning/model.json", "w") as json_file:
      json_file.write(model_json)

    self.model.save_weights("../machinelearning/model.h5")
    print("Model JSON and weights saved")

  def evaluateModel(self, inputVal, outputVal):
    estimator = KerasClassifier(build_fn=self.model,
                                epochs=self.epochs,
                                batch_size=self.batch_size,
                                verbose=self.verbose)
    kfold = StratifiedKFold(n_splits=10, shuffle=True)
    results = cross_val_score(estimator, inputVal, outputVal, cv=kfold)
    return results.mean()*100

  def start(self, merge = True):
    inputVal, outputVal = self.loadData(merge);
    outputVal = self.encodeLabel(outputVal)

    #results = self.evaluateModel(inputVal, outputVal)
    #print("Model accuracy: ", result)

    print("Creating production model")
    self.model.fit(inputVal, outputVal,
                   epochs=self.epochs,
                   batch_size=self.batch_size,
                   verbose=self.verbose)

    self.saveModel()

    self.model = model.getModel()
