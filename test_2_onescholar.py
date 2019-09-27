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

class TestClass_OneScholar:

    def setup_method(self):
        self.scholars = []
        self.affiliations = []
        self.filename_prefix = str(date.today()) + "_swese_"
        self.test_scholar = ["David Notkin"]

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

    def test_david_notkin(self):
        self.add_swese_scholars(self.test_scholar, "N/A")
        self.miner = ScholarMiner(self.filename_prefix, self.scholars, self.affiliations)
        self.miner.process_group()
        self.scholars = self.miner.get_scholars()
        david = None
        for scholar in self.scholars:
            if scholar.name == "David Notkin":
                david = scholar

        # TC1: Test that DBLP returns a result
        assert self.scholars != None
        assert len(self.scholars) == 1

        # TC2: Test that David Notkin has 151 DBLP entries
        assert david.dblp_entries == 151

        # TC3: Test that the name is correctly processed
        assert david.name == "David Notkin"

        # TC4: Test that David Notkin has 134 publications after cleaning the list
        assert david.nbr_publications == 134

        # TC5: Test that David Notkin has the correct ratios
        assert david.first_ratio == pytest.approx(0.24, 0.01)
        assert david.sci_ratio == pytest.approx(0.17, 0.01)
        assert david.nbr_sci_publications == 23

        # TC6: Test write results
        self.miner.write_results()
        filename_txt = self.filename_prefix + "1_miner.txt"
        filename_csv = self.filename_prefix + "1_miner.csv"
        assert os.path.exists(filename_txt)
        assert os.path.exists(filename_csv)

        # TC7: Test file sizes
        file_stats_txt = os.stat(filename_txt)
        file_stats_csv = os.stat(filename_csv)
        assert file_stats_txt.st_size == pytest.approx(1149, 1)
        assert file_stats_csv.st_size == pytest.approx(67, 1)

        # TC8: Test analyzer
        analyzer = ScholarAnalyzer(self.filename_prefix, self.scholars, self.affiliations)
        analyzer.analyze_individual_research_interests()
        assert david.sss_contrib == 6.11
        assert david.sss_rating == 26.67

        # TC10: Test tabulator
        tabulator = ScholarTabulator(self.filename_prefix, self.test_scholar, self.affiliations)
        tabulator.write_tables()
