# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

from scholar_miner import ScholarMiner

def test_notkin_items():
    miner = ScholarMiner()
    test = {"David Notkin":False}
    print("¤¤¤ TIME TO MINE!")
    miner.process_group(test)
    print("¤¤¤ Processing complete")
    scholars = miner.get_scholars()
    print("¤¤¤ WE HAVE MINED: " + str(scholars))
    notkin_stats = scholars[0]
    print("¤¤¤ WE KNOW: ")
    print(notkin_stats)
    assert len(notkin_stats.publications) == 151
    