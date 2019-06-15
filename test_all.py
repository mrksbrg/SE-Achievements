# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

from publication import Publication

def test_get_one():
    assert Publication.get_one() == 1