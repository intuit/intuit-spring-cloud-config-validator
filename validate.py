import os
import glob

# Current directory path
currentDirPath = os.path.dirname(os.path.realpath(__file__))

def listConfigFiles(extension):
  return glob.glob(os.path.join(currentDirPath, extension))

def listAllConfigFiles():
  configMatches = ["*.json", "*.yaml", "*.yml", "*.properties", ".*matrix*.json"]

  allConfigs = []
  for configMatch in configMatches:
    allConfigs = allConfigs + listConfigFiles(configMatch)

  return allConfigs

# http://stackoverflow.com/questions/11294535/verify-if-a-string-is-json-in-python/11294685#11294685
def isJsonFileValid(filePath):
  print "Validating " + filePath
  try:
    with open(filePath) as data_file:
      data = json.load(data_file)
    return True

  except ValueError, e:
    return False

def validateConfigs():
  # The index of the files and if they are valid
  fileValidatesIndex = {}

  # Iterate over all config files, validating according to their extension
  for configFileName in listAllConfigFiles():
    if configFileName.endswith(".json"):
      fileValidatesIndex[configFileName] = isJsonFileValid(configFileName)

    elif configFileName.endswith(".yml") or configFileName.endswith(".yaml"):
      fileValidatesIndex[configFileName] = True

    else:
      fileValidatesIndex[configFileName] = True

  return fileValidatesIndex

print "All configs"
print listAllConfigFiles()

validationIndex = validateConfigs()
for filePath, isValid in validationIndex.iteritems():
  if isValid:
    # http://www.fileformat.info/info/unicode/char/2714/index.htm
    print str(u'\u2714'.encode('UTF-8')) + " File " + filePath + " is valid!"
  else:
    # http://www.fileformat.info/info/unicode/char/2718/index.htm
    print str(u'\u2718'.encode('UTF-8')) + " File " + filePath + " is NOT valid!"
