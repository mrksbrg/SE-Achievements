# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

from scholar_miner import ScholarMiner
import pytest

class TestClass:

    def setup_method(self, module):
        self.scholars = None
        self.test_scholar = {"David Notkin":False}
        self.test_scholar = {"Thomas Olsson":False}
        self.miner = None
        self.miner = ScholarMiner()
        
    def test_dblp_query(self):
        self.miner.process_group(self.test_scholar)
        scholars = self.miner.get_scholars()
        type(scholars)
        print(type(scholars))
        assert scholars != None
    
    def test_notkin_items(self):
        
        print("¤¤¤ WE HAVE MINED: " + str(self.scholars))
        #notkin_stats = self.scholars[0]
        print("¤¤¤ WE KNOW: ")
        #print(notkin_stats)
        #assert len(notkin_stats.publications) == 151
    