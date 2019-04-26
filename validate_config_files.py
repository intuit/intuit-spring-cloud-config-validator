#!/usr/bin/python

import sys
import subprocess
import os
import glob2
import json
import yaml

from yamllint.config import YamlLintConfig
from yamllint import linter

import errno
from pyjavaproperties import Properties

# Verion of this script, printed in the output
VERSION = "1.2.0"

class ExecutionContext:
  """Decider of what to execute"""

  @staticmethod
  def isOnGithub():
    """Returns whether the current execution is on github
       based on the environment variable $GIT_DIR."""
    return os.environ.get('GIT_DIR')

  @staticmethod
  def isOnTestCases():
    """Verifies if the unit tests have been loaded for execution using python or the 'discover' feature (python 2.7+).
        * python -m tests.test_invalid_matrix_json_validation
        * python -m unittest discover -v tests
    """
    # http://stackoverflow.com/questions/4858100/how-to-list-imported-modules/4858123#4858123
    return 'unittest' in sys.modules.keys() or 'tests.sys' in sys.modules.keys()

  @staticmethod
  def getCurrentDirPath():
    """Calculates the current directory to validate based on the execution
       * If we are executing tests, it will be CURRENT_PATH/tests
       * Current directory is set by default
       * If it is provided by parameter, then we change it.
       * If it is executed as a Github Enterprise as a pre-receive hook
    """
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
      print "=> Validating repo " + currentDirPath

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

      # Deleting a branch should NOT validate anything... skipping...
      if "0000000" in commit:
        print "Deleting branch... Skip validation"
        exit(0)

      if "0000000" in base:
        print "Validating new branch..."

      print "Processing commit=" + commit + " ref=" + ref

      currentDirPath = Validator.processPreReceivehookFilesInGithub(base, commit)
      if "0000000" not in base:
        print "=> Validating " + base + ".." + commit

      else:
        print "=> Validating SHA " + commit

    return currentDirPath

class GitRepo:
  """Wrapper for Github Repo-related methods"""

  # Execute any git command in python
  @staticmethod
  def git(args):
    """Executes a git command"""

    environ = os.environ.copy()
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, env=environ)
    return proc.communicate()

  # The set of files changed in the current changes
  @staticmethod
  def listConfigFilesInGitCommits(base, commit):
    """Gets the list of all files changed in the current commit"""

    # http://stackoverflow.com/questions/1552340/how-to-list-the-file-names-only-that-changed-between-two-commits
    # https://robots.thoughtbot.com/input-output-redirection-in-the-shell
    # git show --pretty="format:" --name-only | cat
    if "0000000000" not in base:
      (results, code) = GitRepo.git(('git', 'show', base + ".." + commit, '--pretty=format:', '--name-only'))

    else:
      # All files in the current revision. No way to know which files changed in new branch
      (results, code) = GitRepo.git(('git', 'ls-tree', '-r', 'HEAD', '--name-only'))

    # Filter the non-empty, non-repeated elements as the command returns a\nb\n\c
    # http://stackoverflow.com/questions/33944647/what-is-the-most-pythonic-way-to-filter-a-set/33944663#33944663
    return [x for x in set(results.strip().split('\n')) if x != '']

  @staticmethod
  def openCommitFileContent(fileName, commit = "HEAD"):
    """Gets the contents of a given fileName"""

    # Show the file at the head
    # git show HEAD:application.properties | cat
    (results, code) = GitRepo.git(('git', 'show', commit + ":" + fileName))
    return results

class ConfigFileValidator:
  """Validator at the configuration file level, defined by file extension"""

  # http://stackoverflow.com/questions/11294535/verify-if-a-string-is-json-in-python/11294685#11294685
  @staticmethod
  def isJsonFileValid(filePath):
    """Verifies if a given json file is valid"""

    try:
      with open(filePath) as data_file:
        data = json.load(data_file)
      return True

    except:
      return sys.exc_info()[1]

  # https://bitbucket.org/jnoller/pyjavaproperties
  @staticmethod
  def isPropertiesFileValid(filePath):
    """Verifies if a given properties file is valid"""

    p = Properties()
    try:
      p.load(open(filePath))
      return True

    except:
      return sys.exc_info()[1]

  # http://stackoverflow.com/questions/3971822/yaml-syntax-validator
  @staticmethod
  def isYamlFileValid(filePath):
    """Verifies if a given yaml file is valid"""

    # Rules from https://yamllint.readthedocs.io/en/stable/rules.html#module-yamllint.rules.brackets
    rules = yaml.safe_load("brackets: {min-spaces-inside: -1, max-spaces-inside: -1}\nkey-duplicates: enable\ndocument-start: disable\ntrailing-spaces: disable\nline-length: disable\ncomments-indentation: disable\ncomments: disable\nnew-line-at-end-of-file: disable\nempty-lines: disable\nindentation: disable")
    conf = {'extends': 'default', 'rules': rules}
    yamlLintConfig = YamlLintConfig(yaml.safe_dump(conf))

    # ymlDocs = yaml.load(open(filePath), Loader = yaml.Loader)
    lintError = list(linter.run(open(filePath), yamlLintConfig));

    if lintError:
      return lintError

    else:
      return True

class Validator:
  """Validates a given set of config files under a given directory."""

  # List the config files based on the given extension.
  @staticmethod
  def listConfigFiles(dirPath, extension):
    """Lists all the config files in a given directory with the given extension"""

    return glob2.glob(os.path.join(dirPath, extension))

  # Saves the given content in the file path from the contextDir
  @staticmethod
  def saveFileContent(fileName, content, contextDir):
    """Saves the file contents in a given directory"""

    filePath = contextDir + "/" + fileName

    # Save the file in the context
    with open(filePath, "w") as text_file:
      text_file.write(content)

    return filePath

  # Create the context path for the file if it does not exist
  @staticmethod
  def createContextDir(context):
    """Creates the context directory related to a value provided"""

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
  def processPreReceivehookFilesInGithub(base, head):
    """Processes the pre-receive hook in the github environment."""

    # Create a context Id for the process
    context = head

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

      # fileName is actually the partial fileName like dir/file.ext
      # We need to create the dirs relative to the file
      if len(fileName.split("/")) > 1:
          # Given "idps/idps-config.sh", idps-config.sh
          fileNameToProcess = fileName.split("/")[-1:]
          # Given "idps/idps-config.sh", idps, the first elements,
          dirNameToProcess = contextDir + "/" + "/".join(fileName.split("/")[:-1])

          # When there's a directory, create it before
          if not os.path.exists(dirNameToProcess):
            try:
              os.makedirs(dirNameToProcess)
            except OSError as exc: # Guard against race condition
              if exc.errno != errno.EEXIST:
                raise

      # Save the contents in the context directory
      filePath = Validator.saveFileContent(fileName, content, contextDir)
      # print "File saved at " + filePath

    return contextDir

  # Listing all the valid spring cloud configuration files.
  @staticmethod
  def listAllConfigFiles(dirPath):
    """Lists all the configuration files in a given directory"""

    # Valid configuration files
    configMatches = ["**/*.json", "**/*.yaml", "**/*.yml", "**/*.properties"]
    print "Filtering Spring Cloud Config Server's files: ", configMatches

    # Get all the types config files based on the matches.
    allConfigs = []
    for configMatch in configMatches:
      allConfigs = allConfigs + Validator.listConfigFiles(dirPath, configMatch)

    return allConfigs

  # Generates an index of the config files and the associated exception, if any
  @staticmethod
  def validateConfigs(dirPath):
    """Validates all the configuration properties in a given directory and returns the validation
        metatadata indexed by file name. The value can be the value or an error message.
    """

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
  """Provides implementation of the test execution in the command-line, printing validation reports"""

  @staticmethod
  def run(dirPath = None):
    """Runs the validation on a given directory, printing the report about each file verified"""

    # Starting the process
    print "#####################################################"
    print "#### Intuit Spring Cloud Config Validator " + VERSION + " #####"
    print "#####################################################"

    #for key in os.environ.keys():
    #  print "%30s %s \n" % (key,os.environ[key])

    currentDirPath = dirPath if dirPath else ExecutionContext.getCurrentDirPath()

    # Load the validation of the config files
    return (currentDirPath, Validator.validateConfigs(currentDirPath))

  @staticmethod
  def explain(currentDirPath, validationIndex):
    """Explains the report based on the indexed results of the validator execution"""

    noErrors = True

    # Iterate over the index of the verifications
    for filePath, isValid in validationIndex.iteritems():
      filePath = filePath if not ExecutionContext.isOnGithub() else str.replace(filePath, currentDirPath + "/", "")
      if isValid == True:
        print "(v) File " + filePath + " is valid!"

      else:
        isValid = isValid if not ExecutionContext.isOnGithub() else str.replace(str(isValid), currentDirPath + "/", "")
        # Only when we are running in github
        print "(x) File " + filePath + " is invalid: " + str(isValid)
        noErrors = False

    # Exist with the value for errors
    sys.exit(0 if noErrors else 1)

# Execute the shell script and explain the validation.
if not ExecutionContext.isOnTestCases():
  (executationDirPath, validationIndex) = ShellExecution.run()
  ShellExecution.explain(executationDirPath, validationIndex)
