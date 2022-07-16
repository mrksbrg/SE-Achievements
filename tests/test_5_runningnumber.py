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

class TestClass_RunningNumber:

    def setup_method(self):
        self.scholars = []
        self.affiliations = []
        subdirectory = "output"
        try:
            os.mkdir(subdirectory)
        except Exception:
            pass
        self.filename_prefix = os.path.join(subdirectory, str(date.today()) + "_sss_")
        self.test_scholar = [("Thomas Olsson", "0001", "https://dblp.org/pid/31/5587-1.xml")]

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

    def test_thomas_olsson(self):
        self.add_sss_scholars(self.test_scholar, "N/A")
        self.miner = ScholarMiner(self.filename_prefix, self.scholars, self.affiliations)
        self.miner.parse_scholars()
        self.scholars = self.miner.get_scholars()
        thomas = None
        for scholar in self.scholars:
            if scholar.name == "Thomas Olsson":
                thomas = scholar

        # TC1: Test that DBLP returns a result
        assert self.scholars != None
        assert len(self.scholars) == 1

        # TC2: Test that Thomas Olsson has at least 40 DBLP entries
        assert thomas.dblp_entries >= 40

        # TC3: Test that the name is correctly processed
        assert thomas.name == "Thomas Olsson"

        # TC4: Test that Thomas Olsson has at least 30 publications after cleaning the list
        assert thomas.nbr_publications >= 30

        # TC5: Test that Thomas Olsson has non-zero ratios
        assert thomas.first_ratio >= 0.01
        assert thomas.sci_ratio >= 0.01
        assert thomas.nbr_sci_publications >= 1

        # TC6: Test write results
        self.miner.write_results()
        filename_txt = self.filename_prefix + "1_miner.txt"
        filename_csv = self.filename_prefix + "1_miner.csv"
        assert os.path.exists(filename_txt)
        assert os.path.exists(filename_csv)

        # TC7: Test file sizes
        file_stats_txt = os.stat(filename_txt)
        file_stats_csv = os.stat(filename_csv)
        assert file_stats_txt.st_size > 0
        assert file_stats_csv.st_size > 0

        # TC8: Test analyzer
        analyzer = ScholarAnalyzer(self.filename_prefix, self.scholars, self.affiliations)
        analyzer.analyze_individual_research_interests()
        assert thomas.sss_contrib >= 1.50
        assert thomas.sss_rating >= 1.00

        # TC10: Test tabulator
        tabulator = ScholarTabulator(self.filename_prefix, self.scholars, self.affiliations)
        tabulator.write_tables()
