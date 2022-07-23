# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

import pytest
import os.path
from datetime import date
from swesesci.scholar import SSSScholar
from swesesci.affiliation import SSSAffiliation
from swesesci.scholar_reader import ScholarReader
from swesesci.scholar_miner import ScholarMiner
from swesesci.scholar_analyzer import ScholarAnalyzer
from swesesci.scholar_tabulator import ScholarTabulator

class TestClass_TwoScholars:

    def setup_method(self):
        self.sss_scholars = []
        self.sss_affiliations = []
        subdirectory = "output"
        try:
            os.mkdir(subdirectory)
        except Exception:
            pass
        self.filename_prefix = os.path.join(subdirectory, str(date.today()) + "_sss_")

        reader = ScholarReader("test/test_3_twoscholars.csv")
        self.sss_scholars, self.sss_affiliations = reader.read_candidate_scholars()
        self.miner = ScholarMiner(self.filename_prefix, self.sss_scholars, self.sss_affiliations)
        self.miner.parse_scholars()
        self.sss_scholars = self.miner.get_scholars()
        print(self.sss_scholars)

    def test_two_results(self):
        # TC1: Test that DBLP returns a result
        assert len(self.sss_scholars) == 1

    def test_simon_poulding(self):
        simon = None
        for scholar in self.sss_scholars:
            if scholar.name == "Simon M. Poulding":
                simon = scholar

        # TC2: Test that Simon Poulding has 49 DBLP entries
        assert simon.dblp_entries == 49

        # TC3: Test that the name is correctly processed
        assert simon.name == "Simon M. Poulding"

        # TC4: Test that Simon Poulding has 41 publications after cleaning the list
        assert simon.nbr_publications == 41

        # TC5: Test that Simon Poulding has the correct ratios
        assert simon.first_ratio == pytest.approx(0.37, 0.01)
        assert simon.sci_ratio == pytest.approx(0.17, 0.01)
        assert simon.nbr_sci_publications == 7

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

        # TC8: Test analyzer
        analyzer = ScholarAnalyzer(self.filename_prefix, self.sss_scholars, self.sss_affiliations)
        analyzer.analyze_individual_research_interests()
        assert simon.sss_contrib == 2.84
        assert simon.sss_rating == 8.5

        # TC10: Test tabulator
        tabulator = ScholarTabulator(self.filename_prefix, self.sss_scholars, self.sss_affiliations)
        tabulator.write_tables()

    def test_richard_holst(self):
        richard = None
        for scholar in self.sss_scholars:
            if scholar.name == "Richard C. Holt":
                richard = scholar

        # TC11: Test that Richard is removed as a non-SCI first-author
        assert richard is None
