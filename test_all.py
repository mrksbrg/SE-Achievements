# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

import dblp

def test_notkin_items():
    search_res = dblp.search("David Notkin")
    notkin_stats = search_res[0]
    assert len(notkin_stats.publications) == 151
    