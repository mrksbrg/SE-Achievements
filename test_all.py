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
        self.test_scholar = {"David Notkin":False, "Simon M. Poulding":False, "Richard C. Holt":False}
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
        
        # TC4: Test that David Notkin has 151 publications after cleaning the list
        assert david.get_nbr_publications() == 146
        
        # TC5: Test that David Notkin has 35 publications in SCI-listed journals
        assert david.get_nbr_sci_publications() == 35
        
        # TC6: Test that David Notkin has the correct ratios
        david.calc_stats()
        assert david._first_ratio == pytest.approx(0.2945, 0.001)
        assert david._sci_ratio == pytest.approx(0.2397, 0.001)
        assert david.get_nbr_sci_publications() == 35        
        
        
    def test_simon_poulding(self):
        self.miner.process_group(self.test_scholar)
        self.scholars = self.miner.get_scholars()
        simon = self.scholars["Simon M. Poulding"]

        # TC1: Test that DBLP returns a result
        assert self.scholars != None
        
        # TC2: Test that Simon Poulding has 48 DBLP entries
        assert simon.dblp_entries == 48
        
        # TC3: Test that the name is correctly processed
        assert simon.name == "Simon M. Poulding"
        
        # TC4: Test that Simon Poulding has 44 publications after removing duplicates
        assert simon.get_nbr_publications() == 44
        
        # TC5: Test that Simon Poulding has 8 publications in SCI-listed journals
        assert simon.get_nbr_sci_publications() == 8
    
        #TC6: Test that Simon Poulding has the correct ratios
        simon.calc_stats()
        assert simon._first_ratio == pytest.approx(0.364, 0.001)
        assert simon._sci_ratio == pytest.approx(0.182, 0.001)
        assert simon.get_nbr_sci_publications() == 8
        
    def test_richard_holst(self):
        self.miner.process_group(self.test_scholar)
        self.scholars = self.miner.get_scholars()
        richard = self.scholars["Richard C. Holt"]

        # TC1: Test that DBLP returns a result
        assert self.scholars != None
        
        # TC2: Test that Simon Poulding has 48 DBLP entries
        assert richard.dblp_entries == 138
        
        # TC3: Test that the name is correctly processed
        assert richard.name == "Richard C. Holt"
        
        # TC4: Test that Simon Poulding has 44 publications after removing duplicates
        assert richard.get_nbr_publications() == 137
        
        # TC5: Test that Simon Poulding has 8 publications in SCI-listed journals
        assert richard.get_nbr_sci_publications() == 8
    
        #TC6: Test that Simon Poulding has the correct ratios
        richard.calc_stats()
        assert richard._first_ratio == pytest.approx(0.2117, 0.001)
        assert richard._sci_ratio == pytest.approx(0.0584, 0.001)
        assert richard.get_nbr_sci_publications() == 8    