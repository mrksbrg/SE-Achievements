# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

import pytest
import os.path
import csv
from datetime import date
from swesesci.scholar import SSSScholar
from swesesci.affiliation import SSSAffiliation
from swesesci.scholar_miner import ScholarMiner
from swesesci.scholar_analyzer import ScholarAnalyzer
from swesesci.scholar_tabulator import ScholarTabulator

def string_splitter(scholar_string):
    affiliation = scholar_string[0]
    name = scholar_string[1]
    running_number = scholar_string[2]
    url = scholar_string[3]

    try:
        split1 = url.split("pid/")
        split2 = split1[1].split(".xml")
        pid = split2[0]
    except IndexError:
        print("Invalid format of input XML URL. (" + name + ")")
        raise IndexError

    return affiliation, name, running_number, pid, url

class TestClass_OneScholar:

    def setup_method(self):
        self.sss_scholars = []
        self.sss_affiliations = []
        subdirectory = "output"
        try:
            os.mkdir(subdirectory)
        except Exception:
            pass
        self.filename_prefix = os.path.join(subdirectory, str(date.today()) + "_sss_")

    def get_affiliation_list(self, scholars):
        tmp_list = []
        for scholar in self.sss_scholars:
            tmp_aff = SSSAffiliation(scholar.affiliation)
            existing_aff = tmp_aff in self.sss_affiliations

            if existing_aff is False:
                tmp_aff.nbr_scholars += 1
                tmp_list.append(tmp_aff)
            else:
                existing_aff.nbr_scholars += 1

        return tmp_list

    def test_david_notkin(self):
        with open('test/test_2_onescholar.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            candidate_scholars = list(reader)

        scholar_list = list(map(string_splitter, candidate_scholars))
        [self.sss_scholars.append(SSSScholar(x[1], x[2], x[3], x[4], x[0], -1)) for x in scholar_list]
        self.sss_affiliations = self.get_affiliation_list(self.sss_scholars)

        self.miner = ScholarMiner(self.filename_prefix, self.sss_scholars, self.sss_affiliations)
        self.miner.parse_scholars()
        self.sss_scholars = self.miner.get_scholars()

        david = None
        for scholar in self.sss_scholars:
            if scholar.name == "David Notkin":
                david = scholar

        # TC1: Test that DBLP returns a result
        assert self.sss_scholars != None
        assert len(self.sss_scholars) == 1

        # TC2: Test that David Notkin has 159 DBLP entries
        assert david.dblp_entries == 159

        # TC3: Test that the name is correctly processed
        assert david.name == "David Notkin"

        # TC4: Test that David Notkin has 126 publications after cleaning the list
        assert david.nbr_publications == 126

        # TC5: Test that David Notkin has the correct ratios
        assert david.first_ratio == pytest.approx(0.18, 0.01)
        assert david.sci_ratio == pytest.approx(0.17, 0.01)
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
        analyzer = ScholarAnalyzer(self.filename_prefix, self.sss_scholars, self.sss_affiliations)
        analyzer.analyze_individual_research_interests()
        assert david.sss_contrib == 5.94
        assert david.sss_rating == 21.82

        # TC10: Test tabulator
        tabulator = ScholarTabulator(self.filename_prefix, self.sss_scholars, self.sss_affiliations)
        tabulator.write_tables()
