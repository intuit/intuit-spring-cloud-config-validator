#!/usr/bin/python

import sys
import subprocess
import os
import glob
import json
import yaml 
import uuid
from pyjavaproperties import Properties

# Verion of this script, printed in the output
VERSION = "0.1.2"

# The background colors used below
class ShellColor:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'

class ExecutionContext:
  """Decider of what to execute"""

  @staticmethod
  def isOnGithub():
    """Returns whether the current execution is on github
       based on the environment variable $GIT_DIR."""
    return os.environ.get('GIT_DIR')

  @staticmethod
  def isOnTestCases():
    return 'tests' in sys.modules.keys()

  @staticmethod
  def getCurrentDirPath():
    # http://stackoverflow.com/questions/34598626/how-do-i-check-if-code-is-being-run-from-a-nose-test/34598987#34598987
    if ExecutionContext.isOnTestCases():
      return os.path.dirname(os.path.realpath(__file__)) + "/tests"

    # Current directory path where this is executing
    currentDirPath = os.path.dirname(os.path.realpath(__file__))

    # The user can pass the dir as a parameter
    if len(sys.argv) > 1:
      if os.path.isdir(sys.argv[1]):
        currentDirPath = sys.argv[1]

    # If the execution is on github
    if not ExecutionContext.isOnGithub():
      print ShellColor.WARNING + "=> Validating directory " + currentDirPath

    else:
      # https://help.github.com/enterprise/2.6/admin/guides/developer-workflow/creating-a-pre-receive-hook-script/#writing-a-pre-receive-hook-script
      # It takes no arguments, but for each ref to be updated it receives on standard input a line of the format:
      #      <old-value> SP <new-value> SP <ref-name> LF
      # where 
      # * <old-value> is the old object name stored in the ref,
      # * <new-value> is the new object name to be stored in the ref,
      # * <ref-name> is the full name of the ref. 
      # When creating a new ref, < old-value > is 40 00000000000000000.
      line = sys.stdin.read()
      (base, commit, ref) = line.strip().split()
      print "Processing base=" + base + " commit=" + commit + " ref=" + ref

      currentDirPath = Validator.processPrehookFilesInGithub(base, commit)
      if "0000000" not in base:
        print ShellColor.WARNING + "=> Validating " + base + ".." + commit

      else:
        print ShellColor.WARNING + "=> Validating SHA " + commit

    return currentDirPath

class GitRepo:
  """Wrapper for Github Repo-related methods"""

  # Execute any git command in python
  @staticmethod
  def git(args):
    environ = os.environ.copy()
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, env=environ)
    return proc.communicate()

  # The set of files changed in the current changes
  @staticmethod
  def listConfigFilesInGitCommits(base, commit):
    # http://stackoverflow.com/questions/1552340/how-to-list-the-file-names-only-that-changed-between-two-commits
    # https://robots.thoughtbot.com/input-output-redirection-in-the-shell
    # git show --pretty="format:" --name-only | cat
    if "0000000000" not in base:
      (results, code) = GitRepo.git(('git', 'show', base + ".." + commit, '--pretty=format:', '--name-only'))

    else:
      (results, code) = GitRepo.git(('git', 'show', commit, '--pretty=format:', '--name-only'))

    # Filter the non-empty, non-repeated elements as the command returns a\nb\n\c
    # http://stackoverflow.com/questions/33944647/what-is-the-most-pythonic-way-to-filter-a-set/33944663#33944663
    return [x for x in set(results.strip().split('\n')) if x != '']

  @staticmethod
  def openCommitFileContent(fileName, commit = "HEAD"):
    # Show the file at the head
    # git show HEAD:application.properties | cat
    (results, code) = GitRepo.git(('git', 'show', commit + ":" + fileName))
    return results

class ConfigFileValidator:
  """Validator at the configuration file level, defined by file extension"""

  # http://stackoverflow.com/questions/11294535/verify-if-a-string-is-json-in-python/11294685#11294685
  @staticmethod
  def isJsonFileValid(filePath):
    try:
      with open(filePath) as data_file:
        data = json.load(data_file)
      return True

    except ValueError, invalidJsonError:
      return invalidJsonError

  # https://bitbucket.org/jnoller/pyjavaproperties
  @staticmethod
  def isPropertiesFileValid(filePath):
    p = Properties()
    try:
      p.load(open(filePath))
      return True 

    except UnboundLocalError, invalidPropertiesError:
      return invalidPropertiesError

  # http://stackoverflow.com/questions/3971822/yaml-syntax-validator
  @staticmethod
  def isYamlFileValid(filePath):
    try:
      yaml.load(open(filePath), Loader = yaml.Loader)
      return True

    except yaml.parser.ParserError, invalidYamlError:
      return invalidYamlError

class Validator:
  """All operations related to the file-system"""

  # List the config files based on the given extension.
  @staticmethod
  def listConfigFiles(dirPath, extension):
    return glob.glob(os.path.join(dirPath, extension))

  # Saves the given content in the file path from the contextDir
  @staticmethod
  def saveCommitFileContent(fileName, content, contextDir):
    filePath = contextDir + "/" + fileName

    # Save the file in the context
    with open(filePath, "w") as text_file:
      text_file.write(content)

    return filePath

  # Create the context path for the file if it does not exist
  @staticmethod
  def createContextDir(context):
    dirPath = "/tmp/" + context
    if not os.path.exists(dirPath):
      try:
        os.makedirs(dirPath)

      except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
          raise

    return dirPath

  # Fetches the names of all files changed in the current hook and
  # process them all.
  @staticmethod
  def processPrehookFilesInGithub(base, head):
    # Create a context Id for the process
    context = str(uuid.uuid4())

    # Create the context directory to save the current state of the files
    contextDir = Validator.createContextDir(context)

    # The environments provided by the Github PR environment
    # https://help.github.com/enterprise/2.6/admin/guides/developer-workflow/creating-a-pre-receive-hook-script/#environment-variables
    # List all the files that changed in the base and head
    files = GitRepo.listConfigFilesInGitCommits(base, head)

    # Process and validate each individual file
    # print "Processing context " + context
    for fileName in files:
      # Open the contents 
      content = GitRepo.openCommitFileContent(fileName, head)
      # print content

      # Save the contents in the context directory
      filePath = Validator.saveCommitFileContent(fileName, content, contextDir)
      # print "File saved at " + filePath

    return contextDir

  # Listing all the valid spring cloud configuration files.
  @staticmethod
  def listAllConfigFiles(dirPath):
    configMatches = ["*.json", "*.yaml", "*.yml", "*.properties", ".*matrix*.json"]

    # Get all the types config files based on the matches.
    allConfigs = []
    for configMatch in configMatches:
      allConfigs = allConfigs + Validator.listConfigFiles(dirPath, configMatch)

    return allConfigs

  # Generates an index of the config files and the associated exception, if any
  @staticmethod
  def validateConfigs(dirPath):
    # The index of the files and if they are valid name=True | Exception
    fileValidatesIndex = {}

    # Iterate over all config files, validating according to their extension
    for configFileName in Validator.listAllConfigFiles(dirPath):
      if configFileName.endswith(".json"):
        fileValidatesIndex[configFileName] = ConfigFileValidator.isJsonFileValid(configFileName)

      elif configFileName.endswith(".yml") or configFileName.endswith(".yaml"):
        fileValidatesIndex[configFileName] = ConfigFileValidator.isYamlFileValid(configFileName)

      else:
        fileValidatesIndex[configFileName] = ConfigFileValidator.isPropertiesFileValid(configFileName)

    return fileValidatesIndex

# When in github, those will be available
#base = os.environ.get('GITHUB_PULL_REQUEST_BASE')
#head = os.environ.get('GITHUB_PULL_REQUEST_HEAD')

class ShellExecution:

  @staticmethod
  def run(dirPath = None):
    # Starting the process
    print ShellColor.BOLD + ShellColor.OKBLUE + "##################################################" + ShellColor.ENDC
    print ShellColor.BOLD + ShellColor.OKBLUE + "###### Spring Cloud Config Validator " + VERSION + " #######" + ShellColor.ENDC
    print ShellColor.BOLD + ShellColor.OKBLUE + "##################################################" + ShellColor.ENDC

    currentDirPath = dirPath if dirPath else ExecutionContext.getCurrentDirPath()

    # Load the validation of the config files
    return (currentDirPath, Validator.validateConfigs(currentDirPath))

  @staticmethod
  def explain(currentDirPath, validationIndex):
    noErrors = True

    # Iterate over the index of the verifications
    for filePath, isValid in validationIndex.iteritems():
      filePath = filePath if not ExecutionContext.isOnGithub() else str.replace(filePath, currentDirPath + "/", "")
      if isValid == True:
        # http://www.fileformat.info/info/unicode/char/2714/index.htm
        v = str(u'\u2714'.encode('UTF-8'))
        print ShellColor.OKGREEN + v + " File " + filePath + " is valid!" + ShellColor.ENDC

      else:
        isValid = isValid if not ExecutionContext.isOnGithub() else str.replace(str(isValid), currentDirPath + "/", "")
        # Only when we are running in github
        # http://www.fileformat.info/info/unicode/char/2718/index.htm
        x = str(u'\u2718'.encode('UTF-8'))
        print ShellColor.FAIL + x + " File " + filePath + " is NOT valid: " + str(isValid) + ShellColor.ENDC
        noErrors = False

    # Exist with the value for errors
    sys.exit(0 if noErrors else 1)

# Execute the shell script and explain the validation.
if not ExecutionContext.isOnTestCases():
  (currentDirPath, validationIndex) = ShellExecution.run()
  ShellExecution.explain(currentDirPath, validationIndex)
