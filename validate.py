import os
import glob
import json
from pyjavaproperties import Properties

# The background colors used below
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

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
  try:
    with open(filePath) as data_file:
      data = json.load(data_file)
    return True

  except ValueError, invalidJsonError:
    print invalidJsonError
    return False

# https://bitbucket.org/jnoller/pyjavaproperties
def isPropertiesFileValid(filePath):
  p = Properties()
  try:
    p.load(open(filePath))
    return True 

  except UnboundLocalError, invalidPropertiesError:
    print invalidPropertiesError
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
      fileValidatesIndex[configFileName] = isPropertiesFileValid(configFileName)

  return fileValidatesIndex

print bcolors.BOLD + bcolors.OKBLUE + "##################################################" + bcolors.ENDC
print bcolors.BOLD + bcolors.OKBLUE + "###### Intuit Spring Cloud Config Validator ######" + bcolors.ENDC
print bcolors.BOLD + bcolors.OKBLUE + "##################################################" + bcolors.ENDC

validationIndex = validateConfigs()
for filePath, isValid in validationIndex.iteritems():
  if isValid:
    # http://www.fileformat.info/info/unicode/char/2714/index.htm
    print bcolors.OKGREEN + str(u'\u2714'.encode('UTF-8')) + " File " + filePath + " is valid!" + bcolors.ENDC

  else:
    # http://www.fileformat.info/info/unicode/char/2718/index.htm
    print bcolors.FAIL + str(u'\u2718'.encode('UTF-8')) + " File " + filePath + " is NOT valid!" + bcolors.ENDC
