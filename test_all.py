# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

import pytest
from scholar import SWESEScholar
from scholar_miner import ScholarMiner
import os.path
from datetime import date

class TestClass:

    def setup_method(self, module):
        self.scholars = []
        self.filename_prefix = str(date.today()) + "_swese_"        
        self.test_nonsense = ["ABCDEFGH"]
        self.test_scholar = ["David Notkin"]
        self.test_scholars = ["Simon M. Poulding", "Richard C. Holt"]

    def add_swese_scholars(self, process_list, affiliation):
        for name in process_list:
            self.scholars.append(SWESEScholar(name, affiliation))

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
        print(type(self.scholars))
        print(len(self.scholars))
        print(type(self.scholars[0]))
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
        
        # TC4: Test that David Notkin has 151 publications after cleaning the list
        assert david.get_nbr_publications() == 146
        
        # TC5: Test that David Notkin has 35 publications in SCI-listed journals
        assert david.get_nbr_sci_publications() == 35
        
        # TC6: Test that David Notkin has the correct ratios
        david.calc_stats()
        assert david.first_ratio == pytest.approx(0.2945, 0.001)
        assert david.sci_ratio == pytest.approx(0.2397, 0.001)
        assert david.get_nbr_sci_publications() == 35       
        
        # TC7: Test write results
        self.miner.write_results()
        filename_txt = self.filename_prefix + "1_miner.txt"        
        filename_csv = self.filename_prefix + "1_miner.csv"        
        assert os.path.exists(filename_txt)
        assert os.path.exists(filename_csv)
        
        # TC8: Test file sizes
        file_stats_txt = os.stat(filename_txt)        
        file_stats_csv = os.stat(filename_csv)
        assert file_stats_txt.st_size == pytest.approx(1149, 1)
        assert file_stats_csv.st_size == pytest.approx(67, 1)

        # TC9: Test analyzer


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
#        
#        # TC4: Test that Simon Poulding has 44 publications after removing duplicates
#        assert simon.get_nbr_publications() == 44
#        
#        # TC5: Test that Simon Poulding has 8 publications in SCI-listed journals
#        assert simon.get_nbr_sci_publications() == 8
#    
#        #TC6: Test that Simon Poulding has the correct ratios
#        simon.calc_stats()
#        assert simon._first_ratio == pytest.approx(0.364, 0.001)
#        assert simon._sci_ratio == pytest.approx(0.182, 0.001)
#        assert simon.get_nbr_sci_publications() == 8
#        
#        # TC7: Test write to txt-file
#        self.miner.write_scholars_txt()
#        filename = str(date.today()) + "_SCHOLARS.txt"
#        assert os.path.exists(filename)
#        
#        # TC8: Test file size of txt-file
#        file_stats = os.stat(filename)
#        print(str(file_stats.st_size))
#        assert file_stats.st_size == pytest.approx(476, 1)
#            
#        # TC9: Test write to csv-file
#        self.miner.write_scholars_csv()
#        filename = str(date.today()) + "_SCHOLARS.csv"
#        assert os.path.exists(filename)
#        
#        # TC10: Test file size of csv-file
#        file_stats = os.stat(filename)
#        print(str(file_stats.st_size))
#        assert file_stats.st_size == pytest.approx(139, 1)
#        
#    def test_richard_holst(self):
#        self.miner = ScholarMiner(self.test_scholars)
#        self.miner.process_group()
#        self.scholars = self.miner.get_process_list()
#        richard = self.scholars["Richard C. Holt"]
#
#        # TC1: Test that DBLP returns a result
#        assert self.scholars != None
#        
#        # TC2: Test that Simon Poulding has 48 DBLP entries
#        assert richard.dblp_entries == 138
#        
#        # TC3: Test that the name is correctly processed
#        assert richard.name == "Richard C. Holt"
#        
#        # TC4: Test that Simon Poulding has 44 publications after removing duplicates
#        assert richard.get_nbr_publications() == 137
#        
#        # TC5: Test that Simon Poulding has 8 publications in SCI-listed journals
#        assert richard.get_nbr_sci_publications() == 8
#    
#        #TC6: Test that Simon Poulding has the correct ratios
#        richard.calc_stats()
#        assert richard._first_ratio == pytest.approx(0.2117, 0.001)
#        assert richard._sci_ratio == pytest.approx(0.0584, 0.001)
#        assert richard.get_nbr_sci_publications() == 8
#        
#        # TC7: Test write to txt-file
#        self.miner.write_scholars_txt()
#        filename = str(date.today()) + "_SCHOLARS.txt"
#        assert os.path.exists(filename)
#        
#        # TC8: Test file size of txt-file
#        file_stats = os.stat(filename)
#        print(str(file_stats.st_size))
#        assert file_stats.st_size == pytest.approx(476, 1)
#            
#        # TC9: Test write to csv-file
#        self.miner.write_scholars_csv()
#        filename = str(date.today()) + "_SCHOLARS.csv"
#        assert os.path.exists(filename)
#        
#        # TC10: Test file size of csv-file
#        file_stats = os.stat(filename)
#        print(str(file_stats.st_size))
#        assert file_stats.st_size == pytest.approx(139, 1)