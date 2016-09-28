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

def validateConfigs():
  for configFileName in listAllConfigFiles():
    if configFileName.endswith(".json"):
      print "File " + configFileName + " is json"

    elif configFileName.endswith(".yml") or configFileName.endswith(".yaml"):
      print "File " + configFileName + " is yaml"

    else:
      print "File " + configFileName + " is properties"

print "All configs"
print listAllConfigFiles()

validateConfigs()



