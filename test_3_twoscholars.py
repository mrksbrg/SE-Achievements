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

class TestClass_TwoScholars:

    def setup_method(self):
        self.scholars = []
        self.affiliations = []
        self.filename_prefix = str(date.today()) + "_swese_"
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

    def test_simon_poulding(self):
        self.add_swese_scholars(self.test_scholars, "N/A")
        self.miner = ScholarMiner(self.filename_prefix, self.scholars, self.affiliations)
        self.miner.process_group()
        self.scholars = self.miner.get_scholars()
        simon = None
        for scholar in self.scholars:
            if scholar.name == "Simon M. Poulding":
                simon = scholar

        # TC1: Test that DBLP returns a result
        assert len(self.scholars) == 1

        # TC2: Test that Simon Poulding has 48 DBLP entries
        assert simon.dblp_entries == 48

        # TC3: Test that the name is correctly processed
        assert simon.name == "Simon M. Poulding"

        # TC4: Test that Simon Poulding has 42 publications after cleaning the list
        assert simon.nbr_publications == 42

        # TC5: Test that Simon Poulding has the correct ratios
        assert simon.first_ratio == pytest.approx(0.38, 0.01)
        assert simon.sci_ratio == pytest.approx(0.14, 0.01)
        assert simon.nbr_sci_publications == 6

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
        analyzer = ScholarAnalyzer(self.filename_prefix, self.scholars, self.affiliations)
        analyzer.analyze_individual_research_interests()
        assert simon.sss_contrib == 2.76
        assert simon.sss_rating == 8.59

        # TC10: Test tabulator
        tabulator = ScholarTabulator(self.filename_prefix, self.test_scholars, self.affiliations)
        tabulator.write_tables()

    def test_richard_holst(self):
        self.add_swese_scholars(self.test_scholars, "N/A")
        self.miner = ScholarMiner(self.filename_prefix, self.scholars, self.affiliations)
        self.miner.process_group()
        self.scholars = self.miner.get_scholars()
        richard = None
        for scholar in self.scholars:
            if scholar.name == "Richard C. Holt":
                richard = scholar

        # TC1: Test that Richard is removed as a non-SCI first-author
        assert richard is None

        # This part is only relevant if non-SCI first-authors are kept
        # assert len(self.scholars) == 1
        #
        # # TC2: Test that Richard Holst has 138 entries
        # assert richard.dblp_entries == 138
        #
        # # TC3: Test that the name is correctly processed
        # assert richard.name == "Richard C. Holt"
        #
        # # TC4: Test that Richard Holst has 137 publications after removing duplicates
        # assert richard.nbr_publications == 137
        #
        # # TC5: Test that Richard Holst has the correct ratios
        # assert richard.first_ratio == pytest.approx(0.21, 0.01)
        # assert richard.sci_ratio == pytest.approx(0.06, 0.01)
        # assert richard.nbr_sci_publications == 8
        #
        # # TC6: Test write to files
        # self.miner.write_results()
        # filename_txt = self.filename_prefix + "1_miner.txt"
        # filename_csv = self.filename_prefix + "1_miner.csv"
        # assert os.path.exists(filename_txt)
        # assert os.path.exists(filename_csv)
        #
        # # TC7: Test file size of txt-file
        # file_stats_txt = os.stat(filename_txt)
        # file_stats_csv = os.stat(filename_csv)
        # assert file_stats_txt.st_size == pytest.approx(476, 1)
        # assert file_stats_csv.st_size == pytest.approx(139, 1)
        #
        # # TC8: Test analyzer
        # analyzer = ScholarAnalyzer(self.filename_prefix, self.scholars, self.affiliations)
        # analyzer.analyze_individual_research_interests()
        # assert richard.sss_contrib == 2.09
        # assert richard.sss_rating == 12.79
        #
        # # TC10: Test tabulator
        # tabulator = ScholarTabulator(self.filename_prefix, self.test_scholars, self.affiliations)
        # tabulator.write_tables()
