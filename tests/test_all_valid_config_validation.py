# -*- coding: utf-8 -*-
import trace, sys
from .context import *
import unittest

FIXTURE_DIR = FIXTURES_DIR_PATH + "/all-valid-config"

class AllSuccessfulTests(unittest.TestCase, ValidationAssertions):
  """Basic test case when all the files are valid."""

  def setUp(self):
    # Load the validation of the config files
    self.validationIndex = ValidatorScript.Validator.validateConfigs(FIXTURE_DIR)

  def test_that_validation_index_is_dictionary(self):
    self.assertTrue(isinstance(self.validationIndex, dict))
    self.assertTrue(len(self.validationIndex) > 0)

  def test_all_properties_are_valid(self):
    print "All config files are valid"
    for filePath, validationObject in self.validationIndex.iteritems():
      printFileValidationStatus(filePath, validationObject)

      # Verify if the directory is in the file path
      self.assertIn(FIXTURE_DIR, filePath)

      # Verify if each file is valid
      self.assertThatConfigIsValid(filePath, validationObject)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(AllSuccessfulTests)
  unittest.TextTestRunner(verbosity=2).run(suite)

  #t = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix], count=1, trace=0)
  #t.runfunc(unittest.main)
  #r = t.results()
  #r.write_results(show_missing=True)
  #unittest.main()
