# -*- coding: utf-8 -*-
import trace, sys
from .context import *
import unittest

FIXTURE_DIR = FIXTURES_DIR_PATH + "/invalid-matrix-json-column"

class InvalidMatrixFileTests(unittest.TestCase, ValidationAssertions):
  """Basic test case for when the matrix file is invalid."""

  def setUp(self):
    # Load the validation of the config files
    self.validationIndex = ValidatorScript.Validator.validateConfigs(FIXTURE_DIR)

  def test_that_validation_index_is_dictionary(self):
    self.assertTrue(isinstance(self.validationIndex, dict))
    self.assertTrue(len(self.validationIndex) > 0)

  def test_all_matrix_json_files_are_invalid(self):
    print "The android matrix file is invalid"
    for filePath, validationObject in self.validationIndex.iteritems():
      isValid = isConfigValid(validationObject)
      printFileValidationStatus(filePath, validationObject)

      # Verify if the directory is in the file path
      self.assertIn(FIXTURE_DIR, filePath)

      # Only the matrix android file is broken
      if ".matrix-android.json" in filePath:
        self.assertThatConfigIsInvalid(filePath, validationObject)

      else:
        self.assertThatConfigIsValid(filePath, validationObject)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(InvalidMatrixFileTests)
  unittest.TextTestRunner(verbosity=2).run(suite)

  #t = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix], count=1, trace=0)
  #t.runfunc(unittest.main)
  #r = t.results()
  #r.write_results(show_missing=True)
  #unittest.main()
