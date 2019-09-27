# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

import pytest
from scholar import SSSScholar
from affiliation import SSSAffiliation
from scholar_miner import ScholarMiner
from scholar_analyzer import ScholarAnalyzer
from scholar_tabulator import ScholarTabulator
import os.path
from datetime import date

class TestClass:

    def setup_method(self, module):
        self.scholars = []
        self.affiliations = []
        self.filename_prefix = str(date.today()) + "_swese_"
        self.test_nonsense = ["ABCDEFGH", "A¿£$‰"]

    def add_swese_scholars(self, process_list, affiliation):
        for name in process_list:
            self.scholars.append(SSSScholar(name, affiliation))
            tmp_aff = SSSAffiliation(affiliation)
            if tmp_aff not in self.affiliations:
                tmp_aff.nbr_scholars += 1
                self.affiliations.append(tmp_aff)
            else:
                curr = next((x for x in self.affiliations if affiliation == x.name), None)
                curr.nbr_scholars += 1

    def test_nonsense(self):
        self.add_swese_scholars(self.test_nonsense, "N/A")
        self.miner = ScholarMiner(self.filename_prefix, self.scholars, self.affiliations)
        self.miner.process_group()
        self.scholars = self.miner.get_scholars()

        # TC1: Test that DBLP does not return anything
        assert len(self.scholars) == 0
