# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

import pytest

from scholar_miner import ScholarMiner

class TestClass:

    def setup_method(self, module):
        self.scholars = None
        self.test_scholar = {"David Notkin":False, "Simon M. Poulding":False}
        self.miner = ScholarMiner()
        
    def test_david_notkin(self):
        self.miner.process_group(self.test_scholar)
        self.scholars = self.miner.get_scholars()
        david = self.scholars["David Notkin"]

        # TC1: Test that DBLP returns a result
        assert self.scholars != None
        
        # TC2: Test that David Notkin has 151 DBLP entries
        assert david.dblp_entries == 151
        
        # TC3: Test that the name is correctly processed
        assert david.name == "David Notkin"
        
        # TC4: Test that David Notkin has 151 publications after removing duplicates
        assert david.get_nbr_publications() == 151
        
        # TC5: Test that David Notkin has 35 publications in SCI-listed journals
        assert david.get_nbr_sci_publications() == 35
        
        # TC6: Test that David Notkin has the correct ratios
        david.calc_stats()
        assert david._first_ratio == pytest.approx(0.285, 0.001)
        assert david._sci_ratio == pytest.approx(0.232, 0.001)
        assert david.get_nbr_sci_publications() == 35        
        
        
#    def test_simon_poulding(self):
#        self.miner.process_group(self.test_scholar)
#        self.scholars = self.miner.get_scholars()
#        simon = self.scholars["Simon M. Poulding"]
#
#        # TC1: Test that DBLP returns a result
#        assert self.scholars != None
#        
#        # TC2: Test that Simon Poulding has 48 DBLP entries
#        assert simon.dblp_entries == 48
#        
#        # TC3: Test that the name is correctly processed
#        assert simon.name == "Simon M. Poulding"
#        
#        # TC4: Test that Simon Poulding has 48 publications after removing duplicates
#        assert simon.get_nbr_publications() == 44
#        
#        # TC5: Test that David Notkin has 35 publications in SCI-listed journals
#        assert simon.get_nbr_sci_publications() == 8
    