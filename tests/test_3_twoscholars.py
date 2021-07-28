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

class TestClass_TwoScholars:

    def setup_method(self):
        self.scholars = []
        self.affiliations = []
        self.filename_prefix = str(date.today()) + "_swese_"
        self.test_scholars = [("Simon M. Poulding", "-1", "https://dblp.org/pid/93/6877.xml"),
                              ("Richard C. Holt", "-1", "https://dblp.org/pid/h/RichardCHolt.xml")]

    def add_sss_scholars(self, process_list, affiliation):
        for person in process_list:
            name = person[0]
            running_number = person[1]
            url = person[2]
            # extract the pid from the url by substringing
            try:
                split1 = url.split("pid/")
                split2 = split1[1].split(".xml")
                pid = split2[0]
            except IndexError:
                print("Invalid format of input XML URL.")
                return

            self.scholars.append(SSSScholar(name, running_number, pid, url, affiliation, -1))
            tmp_aff = SSSAffiliation(affiliation)
            if tmp_aff not in self.affiliations:
                tmp_aff.nbr_scholars += 1
                self.affiliations.append(tmp_aff)
            else:
                curr = next((x for x in self.affiliations if affiliation == x.name), None)
                curr.nbr_scholars += 1

    def test_simon_poulding(self):
        self.add_sss_scholars(self.test_scholars, "N/A")
        self.miner = ScholarMiner(self.filename_prefix, self.scholars, self.affiliations)
        self.miner.parse_scholars()
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
        analyzer = ScholarAnalyzer(self.filename_prefix, self.scholars, self.affiliations)
        analyzer.analyze_individual_research_interests()
        assert simon.sss_contrib == 2.84
        assert simon.sss_rating == 8.5

        # TC10: Test tabulator
        tabulator = ScholarTabulator(self.filename_prefix, self.scholars, self.affiliations)
        tabulator.write_tables()

    def test_richard_holst(self):
        self.add_sss_scholars(self.test_scholars, "N/A")
        self.miner = ScholarMiner(self.filename_prefix, self.scholars, self.affiliations)
        self.miner.parse_scholars()
        self.scholars = self.miner.get_scholars()
        richard = None
        for scholar in self.scholars:
            if scholar.name == "Richard C. Holt":
                richard = scholar

        # TC1: Test that Richard is removed as a non-SCI first-author
        assert richard is None
