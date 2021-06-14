from datetime import datetime

class Manual:
  """
  Everytime the user triggers a manual opening or closing of windows
  the nodeMCU will send data to the backend to store in the database
  so it can be used for training.
  If the user has enabled pattern saving the data will be saved on pattern.txt
  if the user has disabled pattern saving the data will be saved on manual.txt

  The parameters passing to the functions comes from the sensor readings.
  """
  
  def __init__(self):
    self.manualAction = None
    self.patternAction = None

  def updateDatabase(self, smartMode):
    database = None
    databaseDir = '../database/'
    databaseName = None

    if(smartMode == 'enabled'):
      databaseName = databaseDir + 'pattern.txt'
    else:
      databaseName = databaseDir + 'manual.txt'

    try:
      database = open(databaseName, 'a')

      if(smartMode == 'enabled'):
        database.write(self.patternAction + '\n')

      else:
        database.write(self.manualAction + '\n')

    except:
      print("Unable to write data on database: " + databaseName)
      return False
    finally:
      database.close()
      database = None
    
    return True


  def addNewEntry(self, smartMode, windowOpen, temperature, humidity):
    data = temperature + ',' + humidity + ',' + windowOpen

    if(smartMode == 'enabled'):
      self.patternAction = data
    else:
      self.manualAction = data

    if(self.updateDatabase(smartMode)):
      return 'Database updated'

    return 'Unable to update database'
