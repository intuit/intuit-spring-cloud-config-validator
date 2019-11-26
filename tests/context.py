# -*- coding: utf-8 -*-

"""This is the context module that shares functionality.
.. moduleauthor: Marcello_deSales@intuit.com
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the script
import validate_config_files as ValidatorScript

# The background colors used below
class ShellColor:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'

# Expose out a couple of constants for the paths.
APP_DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TESTS_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
FIXTURES_DIR_PATH = TESTS_DIR_PATH + "/fixtures"

def getRelativeFixturePath(absoluteFilePath):
  """This method calculates the relative fixture file path to the application."""
  return str.replace(absoluteFilePath, APP_DIR_PATH + "/", "")

def isConfigValid(obj):
  """Whether the given object returned by the validation is valid.
  :returns: bool -- Whether the given object is valid.
  """ 
  return isinstance(obj, bool) and obj == True

def printFileValidationStatus(filePath, validationObject):
  """Prints the validation status for the given file path"""

  isValid = isConfigValid(validationObject)
  message = str(isValid) if isValid else str(isValid) + " ERROR: " + str(validationObject)

  # https://stackoverflow.com/questions/6812031/how-to-make-unicode-string-with-python3/6812069#6812069 (added , UTF-8 param to str)
  # The V of successful in green
  v = ShellColor.OKGREEN + str('\u2714'.encode('UTF-8'), 'UTF-8')
  # The X of failure in red
  x = ShellColor.FAIL + str('\u2718'.encode('UTF-8'), 'UTF-8')
  shellStatus = v if isValid else x

  print(shellStatus + " is " + getRelativeFixturePath(filePath) + " valid? " + message + ShellColor.ENDC)

class ValidationAssertions:
  """Validation Assertions for the test cases to validate on the values."""

  def assertThatConfigIsValid(self, filePath, isValidObject):
    """Asserts that the given filePath is valid based on its content related to its extension."""

    if not isConfigValid(isValidObject):
      isValid = str.replace(str(isValidObject), FIXTURES_DIR_PATH + "/", "")
      relativeFilePath = getRelativeFixturePath(filePath)
      raise AssertionError('File "' + relativeFilePath + '" is invalid: ' + isValid)

  def assertThatConfigIsInvalid(self, filePath, isValidObject):
    """Asserts that the given filePath is invalid based on its content related to its extension."""

    if isConfigValid(isValidObject):
      relativeFilePath = getRelativeFixturePath(filePath)
      raise AssertionError('File "' + relativeFilePath + '" is valid when it should NOT be')
