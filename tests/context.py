# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import validate_config_files as ValidatorScript

TESTS_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
FIXTURES_DIR_PATH = TESTS_DIR_PATH + "/fixtures"
