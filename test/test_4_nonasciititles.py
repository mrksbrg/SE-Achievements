# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

import os.path
from datetime import date
from swesesci.scholar_reader import ScholarReader
from swesesci.scholar_miner import ScholarMiner
from swesesci.scholar_analyzer import ScholarAnalyzer
from swesesci.scholar_tabulator import ScholarTabulator

class TestClass_NonASCIITitles:

    def setup_method(self):
        self.sss_scholars = []
        self.sss_affiliations = []
        subdirectory = "output"
        try:
            os.mkdir(subdirectory)
        except Exception:
            pass
        self.filename_prefix = os.path.join(subdirectory, str(date.today()) + "_sss_")

        reader = ScholarReader("test/test_4_nonasciititles.csv")
        self.sss_scholars, self.sss_affiliations = reader.read_candidate_scholars()
        self.miner = ScholarMiner(self.filename_prefix, self.sss_scholars, self.sss_affiliations)
        self.miner.parse_scholars()
        self.sss_scholars = self.miner.get_scholars()

    def test_mauro_caporuscio(self):
        mauro = None
        for scholar in self.sss_scholars:
            if scholar.name == "Mauro Caporuscio":
                mauro = scholar

                # TC1: Test that DBLP returns a result
                assert self.sss_scholars != None
                assert len(self.sss_scholars) == 1

                # TC2: Test that Mauro has at least 40 DBLP entries
                assert mauro.dblp_entries >= 40

                # TC3: Test that the name is correctly processed
                assert mauro.name == "Mauro Caporuscio"

                # TC4: Test that Mauro has at least 30 publications after cleaning the list
                assert mauro.nbr_publications >= 30

                # TC5: Test that Mauro has non-zero ratios
                assert mauro.first_ratio >= 0.01
                assert mauro.sci_ratio >= 0.01
                assert mauro.nbr_sci_publications >= 1

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
                analyzer = ScholarAnalyzer(self.filename_prefix, self.sss_scholars, self.sss_affiliations)
                analyzer.analyze_individual_research_interests()
                assert mauro.sss_contrib >= 1.50
                assert mauro.sss_rating >= 1.00

                # TC10: Test tabulator
                tabulator = ScholarTabulator(self.filename_prefix, self.sss_scholars, self.sss_affiliations)
                tabulator.write_tables()
