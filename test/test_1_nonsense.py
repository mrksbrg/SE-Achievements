# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

import pytest
import os.path
from datetime import date
from swesesci.scholar_reader import ScholarReader

class TestClass_NonSense:

    def setup_method(self):
        self.sss_scholars = []
        self.sss_affiliations = []
        subdirectory = "output"
        try:
            os.mkdir(subdirectory)
        except Exception:
            pass
        self.filename_prefix = os.path.join(subdirectory, str(date.today()) + "_sss_")

    def test_nonsense(self):
        reader = ScholarReader("test/test_1_nonsense.csv")

        # TC1: Test that an exception is raised due to incorrect formatting
        with pytest.raises(IndexError):
            sss_scholars, sss_affiliations = reader.read_candidate_scholars()
