#!/usr/bin/python

import sys
import subprocess
import os
import glob
import json
import yaml 
import uuid
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

# List the config files based on the given extension.
def listConfigFiles(dirPath, extension):
  return glob.glob(os.path.join(dirPath, extension))

# Execute any git command in python
# 
def git(args):
    environ = os.environ.copy()
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, env=environ)
    return proc.communicate()

# The set of files changed in the current changes
def listConfigFilesGithub(base, head):
  # http://stackoverflow.com/questions/1552340/how-to-list-the-file-names-only-that-changed-between-two-commits
  # https://robots.thoughtbot.com/input-output-redirection-in-the-shell
  # git show --pretty="format:" --name-only | cat
  (results, code) = git(('git', 'show', base + ".." + head, '--pretty=format:', '--name-only'))

  # Filter the non-empty, non-repeated elements as the command returns a\nb\n\c
  # http://stackoverflow.com/questions/33944647/what-is-the-most-pythonic-way-to-filter-a-set/33944663#33944663
  return [x for x in set(results.strip().split('\n')) if x != '']

def openFileContent(fileName, commit = "HEAD"):
  # Show the file at the head
  # git show HEAD:application.properties | cat
  (results, code) = git(('git', 'show', commit + ":" + fileName))
  return results

# Create the context path for the file if it does not exist
def createContextDir(context):
  dirPath = "/tmp/" + context
  if not os.path.exists(dirPath):
    try:
      os.makedirs(dirPath)

    except OSError as exc: # Guard against race condition
      if exc.errno != errno.EEXIST:
        raise

  return dirPath

# Saves the given content in the file path from the contextDir
def saveFileContent(fileName, content, contextDir):
  filePath = contextDir + "/" + fileName

  # Save the file in the context
  with open(filePath, "w") as text_file:
    text_file.write(content)

  return filePath

def processPrehookFiles():
  # Create a context Id for the process
  context = str(uuid.uuid4())

  # Create the context directory to save the current state of the files
  contextDir = createContextDir(context)

  # List all the files that changed in the base and head
  files = listConfigFilesGithub("HEAD^", "HEAD")

  # Process and validate each individual file

  print "Processing context " + context
  for fileName in files:
    # Open the contents 
    content = openFileContent(fileName)
    # print content

    # Save the contents in the context directory
    filePath = saveFileContent(fileName, content, contextDir)
    # print "File saved at " + filePath

  return contextDir

# Listing all the valid spring cloud configuration files.
def listAllConfigFiles(dirPath):
  configMatches = ["*.json", "*.yaml", "*.yml", "*.properties", ".*matrix*.json"]

  # Get all the types config files based on the matches.
  allConfigs = []
  for configMatch in configMatches:
    allConfigs = allConfigs + listConfigFiles(dirPath, configMatch)

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
def validateConfigs(dirPath):
  # The index of the files and if they are valid name=True | Exception
  fileValidatesIndex = {}

  # Iterate over all config files, validating according to their extension
  for configFileName in listAllConfigFiles(dirPath):
    if configFileName.endswith(".json"):
      fileValidatesIndex[configFileName] = isJsonFileValid(configFileName)

    elif configFileName.endswith(".yml") or configFileName.endswith(".yaml"):
      fileValidatesIndex[configFileName] = isYamlFileValid(configFileName)

    else:
      fileValidatesIndex[configFileName] = isPropertiesFileValid(configFileName)

  return fileValidatesIndex

# Current directory path where this is executing
currentDirPath = os.path.dirname(os.path.realpath(__file__))

onGithub = os.environ.get('GIT_DIR')

# The user can pass the dir as a parameter
if len(sys.argv) > 1:
  if os.path.isdir(sys.argv[1]):
    currentDirPath = sys.argv[1]

# If we are processing the webhook in Github Enterprise
if onGithub:
  currentDirPath = processPrehookFiles()

# Starting the process
print bcolors.BOLD + bcolors.OKBLUE + "##################################################" + bcolors.ENDC
print bcolors.BOLD + bcolors.OKBLUE + "###### Intuit Spring Cloud Config Validator ######" + bcolors.ENDC
print bcolors.BOLD + bcolors.OKBLUE + "##################################################" + bcolors.ENDC
print bcolors.WARNING + "=> Validating directory " + currentDirPath

# Load the validation of the config files
validationIndex = validateConfigs(currentDirPath)

noErrors = True

# Iterate over the index of the verifications
for filePath, isValid in validationIndex.iteritems():
  filePath = filePath if not onGithub else str.replace(filePath, currentDirPath + "/", "")
  if isValid == True:
    # http://www.fileformat.info/info/unicode/char/2714/index.htm
    v = str(u'\u2714'.encode('UTF-8'))
    print bcolors.OKGREEN + v + " File " + filePath + " is valid!" + bcolors.ENDC

  else:
    isValid = isValid if not onGithub else str.replace(str(isValid), currentDirPath + "/", "")
    # Only when we are running in github
    # http://www.fileformat.info/info/unicode/char/2718/index.htm
    x = str(u'\u2718'.encode('UTF-8'))
    print bcolors.FAIL + x + " File " + filePath + " is NOT valid: " + str(isValid) + bcolors.ENDC
    noErrors = False

# Exist with the value for errors
sys.exit(0 if noErrors else 1)
