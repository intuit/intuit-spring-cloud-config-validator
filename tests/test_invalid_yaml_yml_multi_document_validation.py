# -*- coding: utf-8 -*-

# Make sure to append one of the sys paths the current one
# So that we can append context. Evaluated when running the discover mode as
# "python -m unittest discover -v tests"
# http://stackoverflow.com/questions/11536764/how-to-fix-attempted-relative-import-in-non-package-even-with-init-py/19190695#19190695
if __name__ == '__main__' and __package__ is None:
  import sys
  sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from context import *
import unittest

# Test fixture directory containing config files
FIXTURE_DIR = FIXTURES_DIR_PATH + "/invalid-yaml-configs-multiple-documents-per-config"

class InvalidYamlMultiDocumentFileTests(unittest.TestCase, ValidationAssertions):
  """Basic test case for when the yaml files have multiple documents"""

  def setUp(self):
    # Load the validation of the config files
    self.validationIndex = ValidatorScript.Validator.validateConfigs(FIXTURE_DIR)

  def test_that_validation_index_is_dictionary(self):
    self.assertTrue(isinstance(self.validationIndex, dict))
    self.assertTrue(len(self.validationIndex) > 0)

  def test_some_yaml_yml_files_are_invalid(self):
    print(ShellColor.WARNING + "Some Yaml Multi documents are invalid" + ShellColor.ENDC)
    for filePath, validationObject in self.validationIndex.items():
      isValid = isConfigValid(validationObject)
      printFileValidationStatus(filePath, validationObject)

      # Verify if the directory is in the file path
      self.assertIn(FIXTURE_DIR, filePath)

      # Only the matrix android file is broken
      if "sp_boot_sample-dev.yml" in filePath or "sp_boot_sample-e2e.yml" in filePath:
        self.assertThatConfigIsInvalid(filePath, validationObject)

      else:
        self.assertThatConfigIsValid(filePath, validationObject)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(InvalidYamlMultiDocumentFileTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
