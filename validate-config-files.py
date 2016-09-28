#!/usr/bin/python

import sys
import os
import glob
import json
import yaml 
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

# Current directory path where this is executing
currentDirPath = os.path.dirname(os.path.realpath(__file__))

# The user can pass the dir as a parameter
if len(sys.argv) > 1:
  if os.path.isdir(sys.argv[1]):
    currentDirPath = sys.argv[1]

# List the config files based on the given extension.
def listConfigFiles(extension):
  return glob.glob(os.path.join(currentDirPath, extension))

# Listing all the valid spring cloud configuration files.
def listAllConfigFiles():
  configMatches = ["*.json", "*.yaml", "*.yml", "*.properties", ".*matrix*.json"]

  # Get all the types config files based on the matches.
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
    return invalidJsonError

# https://bitbucket.org/jnoller/pyjavaproperties
def isPropertiesFileValid(filePath):
  p = Properties()
  try:
    p.load(open(filePath))
    return True 

  except UnboundLocalError, invalidPropertiesError:
    return invalidPropertiesError

# http://stackoverflow.com/questions/3971822/yaml-syntax-validator
def isYamlFileValid(filePath):
  try:
    yaml.load(open(filePath), Loader = yaml.Loader)
    return True

  except yaml.parser.ParserError, invalidYamlError:
    return invalidYamlError

# Generates an index of the config files and the associated exception, if any
def validateConfigs():
  # The index of the files and if they are valid name=True | Exception
  fileValidatesIndex = {}

  # Iterate over all config files, validating according to their extension
  for configFileName in listAllConfigFiles():
    if configFileName.endswith(".json"):
      fileValidatesIndex[configFileName] = isJsonFileValid(configFileName)

    elif configFileName.endswith(".yml") or configFileName.endswith(".yaml"):
      fileValidatesIndex[configFileName] = isYamlFileValid(configFileName)

    else:
      fileValidatesIndex[configFileName] = isPropertiesFileValid(configFileName)

  return fileValidatesIndex

# Starting the process
print bcolors.BOLD + bcolors.OKBLUE + "##################################################" + bcolors.ENDC
print bcolors.BOLD + bcolors.OKBLUE + "###### Intuit Spring Cloud Config Validator ######" + bcolors.ENDC
print bcolors.BOLD + bcolors.OKBLUE + "##################################################" + bcolors.ENDC
print bcolors.WARNING + "=> Validating directory " + currentDirPath

# Load the validation of the config files
validationIndex = validateConfigs()

noErrors = True

# Iterate over the index of the verifications
for filePath, isValid in validationIndex.iteritems():
  if isValid == True:
    # http://www.fileformat.info/info/unicode/char/2714/index.htm
    v = str(u'\u2714'.encode('UTF-8'))
    print bcolors.OKGREEN + v + " File " + filePath + " is valid!" + bcolors.ENDC

  else:
    # http://www.fileformat.info/info/unicode/char/2718/index.htm
    x = str(u'\u2718'.encode('UTF-8'))
    print bcolors.FAIL + x + " File " + filePath + " is NOT valid: " + str(isValid) + bcolors.ENDC
    noErrors = False

# Exist with the value for errors
sys.exit(0 if noErrors else 1)
