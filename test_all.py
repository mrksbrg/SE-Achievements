# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

import pytest
from scholar import SSSScholar
from affiliation import SSSAffiliation
from scholar_miner import ScholarMiner
from scholar_tabulator import ScholarTabulator
import os.path
from datetime import date

class TestClass:

    def setup_method(self, module):
        self.scholars = []
        self.affiliations = []
        self.filename_prefix = str(date.today()) + "_swese_"
        self.test_nonsense = ["ABCDEFGH"]
        self.test_scholar = ["David Notkin"]
        self.test_scholars = ["Simon M. Poulding", "Richard C. Holt"]

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
        self.miner = ScholarMiner(self.scholars, self.filename_prefix)
        self.miner.process_group()
        self.scholars = self.miner.get_scholars()

        assert self.scholars[0].dblp_entries == -1

    def test_david_notkin(self):
        self.add_swese_scholars(self.test_scholar, "N/A")
        self.miner = ScholarMiner(self.scholars, self.filename_prefix)
        self.miner.process_group()
        self.scholars = self.miner.get_scholars()
        david = None
        for scholar in self.scholars:
            if scholar.name == "David Notkin":
                david = scholar

        # TC1: Test that DBLP returns a result
        assert self.scholars != None

        # TC2: Test that David Notkin has 151 DBLP entries
        assert david.dblp_entries == 151

        # TC3: Test that the name is correctly processed
        assert david.name == "David Notkin"

        # TC4: Test that David Notkin has 146 publications after cleaning the list
        assert david.nbr_publications == 146

        # TC5: Test that David Notkin has the correct ratios
        assert david.first_ratio == pytest.approx(0.29, 0.01)
        assert david.sci_ratio == pytest.approx(0.24, 0.01)
        assert david.nbr_sci_listed == 35

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

        # TC9: Test analyzer

        # TC10: Test tabulator
        tabulator = ScholarTabulator(self.filename_prefix, self.test_scholar, self.affiliations)
        tabulator.write_tables()

    def test_simon_poulding(self):
        self.add_swese_scholars(self.test_scholars, "N/A")
        self.miner = ScholarMiner(self.scholars, self.filename_prefix)
        self.miner.process_group()
        self.scholars = self.miner.get_scholars()
        simon = None
        for scholar in self.scholars:
            if scholar.name == "Simon M. Poulding":
                simon = scholar

        # TC1: Test that DBLP returns a result
        assert self.scholars != None

        # TC2: Test that Simon Poulding has 48 DBLP entries
        assert simon.dblp_entries == 48

        # TC3: Test that the name is correctly processed
        assert simon.name == "Simon M. Poulding"

        # TC4: Test that Simon Poulding has 44 publications after removing duplicates
        assert simon.nbr_publications == 44

        # TC5: Test that Simon Poulding has the correct ratios
        assert simon.first_ratio == pytest.approx(0.36, 0.01)
        assert simon.sci_ratio == pytest.approx(0.18, 0.01)
        assert simon.nbr_sci_listed == 8

        # TC6: Test write to txt-file
        self.miner.write_results()
        filename_txt = self.filename_prefix + "1_miner.txt"
        filename_csv = self.filename_prefix + "1_miner.csv"
        assert os.path.exists(filename_txt)
        assert os.path.exists(filename_csv)

        # TC7: Test file sizes
        file_stats_txt = os.stat(filename_txt)
        file_stats_csv = os.stat(filename_csv)
        assert file_stats_txt.st_size == pytest.approx(476, 1)
        assert file_stats_csv.st_size == pytest.approx(139, 1)

        # TC10: Test tabulator
        tabulator = ScholarTabulator(self.filename_prefix, self.test_scholar)
        tabulator.write_tables()

    def test_richard_holst(self):
        self.add_swese_scholars(self.test_scholars, "N/A")
        self.miner = ScholarMiner(self.scholars, self.filename_prefix)
        self.miner.process_group()
        self.scholars = self.miner.get_scholars()
        richard = None
        for scholar in self.scholars:
            if scholar.name == "Richard C. Holt":
                richard = scholar

        # TC1: Test that DBLP returns a result
        assert self.scholars != None

        # TC2: Test that Richard Holst has 138 entries
        assert richard.dblp_entries == 138

        # TC3: Test that the name is correctly processed
        assert richard.name == "Richard C. Holt"

        # TC4: Test that Richard Holst has 137 publications after removing duplicates
        assert richard.nbr_publications == 137

        # TC5: Test that Richard Holst has the correct ratios
        assert richard.first_ratio == pytest.approx(0.21, 0.01)
        assert richard.sci_ratio == pytest.approx(0.06, 0.01)
        assert richard.nbr_sci_listed == 8

        # TC6: Test write to files
        self.miner.write_results()
        filename_txt = self.filename_prefix + "1_miner.txt"
        filename_csv = self.filename_prefix + "1_miner.csv"
        assert os.path.exists(filename_txt)
        assert os.path.exists(filename_csv)

        # TC7: Test file size of txt-file
        file_stats_txt = os.stat(filename_txt)
        file_stats_csv = os.stat(filename_csv)
        assert file_stats_txt.st_size == pytest.approx(476, 1)
        assert file_stats_csv.st_size == pytest.approx(139, 1)

        # TC10: Test tabulator
        tabulator = ScholarTabulator(self.filename_prefix, self.test_scholar)
        tabulator.write_tables()