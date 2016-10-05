# -*- coding: utf-8 -*-
import trace, sys
from .context import ValidatorScript
from .context import FIXTURES_DIR_PATH
import unittest

FIXTURE_DIR = FIXTURES_DIR_PATH + "/all-valid-config"

def isConfigValid(obj):
  return isinstance(obj, bool) and obj == True

class AllSuccessfulTests(unittest.TestCase):
  """Basic test cases."""

  def setUp(self):
    # Load the validation of the config files
    self.validationIndex = ValidatorScript.Validator.validateConfigs(FIXTURE_DIR)

  def test_that_validation_index_is_dictionary(self):
    self.assertTrue(isinstance(self.validationIndex, dict))
    self.assertTrue(len(self.validationIndex) > 0)

  def test_all_properties_are_valid(self):
    for filePath, isValid in self.validationIndex.iteritems():
      print "is " + filePath + " valid? " + str(isValid)
      self.assertIn(FIXTURE_DIR, filePath)
      self.assertTrue(isConfigValid(isValid))

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(AllSuccessfulTests)
  unittest.TextTestRunner(verbosity=2).run(suite)

  #t = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix], count=1, trace=0)
  #t.runfunc(unittest.main)
  #r = t.results()
  #r.write_results(show_missing=True)
  #unittest.main()
