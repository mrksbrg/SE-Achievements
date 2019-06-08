# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 23:57:13 2019

@author: Markus Borg
"""

import dblp

authors = dblp.search('markus borg')
markus = authors[0]
print("Publications: ", len(markus.publications))
for p in markus.publications:
    print(p.title, " ", p.type, " ", p.journal)
