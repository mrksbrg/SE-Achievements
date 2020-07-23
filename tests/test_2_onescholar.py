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
from swesesci.scholar_miner import ScholarMiner
from swesesci.scholar_analyzer import ScholarAnalyzer
from swesesci.scholar_tabulator import ScholarTabulator

class TestClass_OneScholar:

    def setup_method(self):
        self.scholars = []
        self.affiliations = []
        self.filename_prefix = str(date.today()) + "_swese_"
        self.test_scholar = ["David Notkin"]

    def add_sss_scholars(self, process_list, affiliation):
        for name in process_list:
            words = name.split()
            # check if author has a running number
            if not words[len(words) - 1].isdigit():
                self.scholars.append(SSSScholar(name, -1, affiliation))
                tmp_aff = SSSAffiliation(affiliation)
                if tmp_aff not in self.affiliations:
                    tmp_aff.nbr_scholars += 1
                    self.affiliations.append(tmp_aff)
                else:
                    curr = next((x for x in self.affiliations if affiliation == x.name), None)
                    curr.nbr_scholars += 1
            else:
                # author has a running number
                tmp_scholar = SSSScholar(' '.join(map(str, words[0:len(words) - 1])), str(words[len(words) - 1]),
                                         affiliation)
                self.scholars.append(tmp_scholar)
                tmp_aff = SSSAffiliation(affiliation)
                if tmp_aff not in self.affiliations:
                    tmp_aff.nbr_scholars += 1
                    self.scholars.append(tmp_aff)
                else:
                    curr = next((x for x in self.affiliations if affiliation == x.name), None)
                    curr.nbr_scholars += 1

    def test_david_notkin(self):
        self.add_sss_scholars(self.test_scholar, "N/A")
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

        # TC2: Test that David Notkin has 152 DBLP entries
        assert david.dblp_entries == 152

        # TC3: Test that the name is correctly processed
        assert david.name == "David Notkin"

        # TC4: Test that David Notkin has 123 publications after cleaning the list
        assert david.nbr_publications == 123

        # TC5: Test that David Notkin has the correct ratios
        assert david.first_ratio == pytest.approx(0.18, 0.01)
        assert david.sci_ratio == pytest.approx(0.18, 0.01)
        assert david.nbr_sci_publications == 22

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
        assert david.sss_contrib == 5.91
        assert david.sss_rating == 22.14

        # TC10: Test tabulator
        tabulator = ScholarTabulator(self.filename_prefix, self.scholars, self.affiliations)
        tabulator.write_tables()
