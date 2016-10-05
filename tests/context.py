# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import validate_config_files as ValidatorScript

APP_DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TESTS_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
FIXTURES_DIR_PATH = TESTS_DIR_PATH + "/fixtures"

def getRelativeFixturePath(absoluteFilePath):
  return str.replace(absoluteFilePath, APP_DIR_PATH + "/", "")

def isConfigValid(obj):
  return isinstance(obj, bool) and obj == True

class ValidationAssertions:

  def assertThatConfigIsValid(self, filePath, isValidObject):
    if not isConfigValid(isValidObject):
      isValid = str.replace(str(isValidObject), FIXTURES_DIR_PATH + "/", "")
      relativeFilePath = getRelativeFixturePath(filePath)
      raise AssertionError('File "' + relativeFilePath + '" is invalid: ' + isValid)

  def assertThatConfigIsInvalid(self, filePath, isValidObject):
    if isConfigValid(isValidObject):
      relativeFilePath = getRelativeFixturePath(filePath)
      raise AssertionError('File "' + relativeFilePath + '" is valid when it should NOT be')


