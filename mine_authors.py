# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 23:57:13 2019

@author: Markus Borg
"""

import dblp

scholar_name = 'Markus Borg'
authors = dblp.search(scholar_name)
markus = authors[0]
sci_list = []
nbr_first_authorships = 0
print("Publications: ", len(markus.publications))
counter = 0
for p in markus.publications:
    print(p.title, " ", p.type, " ", p.journal)
    temp = p.authors
    # count first-authorships
    if len(p.authors) > 0:
	    if temp[0] == scholar_name:
	    	nbr_first_authorships += 1
    # count SCI journals
    if p.type == 'article':
    	sci_list.append(p.title)
    counter += 1
    if counter>=100:
    	break
    	
seed_ratio = nbr_first_authorships / len(markus.publications)
quality_ratio = len(sci_list) / len(markus.publications)

print(scholar_name, " ### Seed ratio: ", seed_ratio, " Quality ratio: ", quality_ratio) 

    