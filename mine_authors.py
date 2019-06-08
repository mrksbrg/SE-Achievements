# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 23:57:13 2019

@author: Markus Borg
"""

import dblp

rise_list = ["Markus Borg", "Ulrik Franke", "Ana Magazinius"]
f = open("output.txt","w+")
i = 0

for scholar in rise_list:
	print(scholar)
	authors = dblp.search(scholar)

	scholar = authors[0]
	sci_list = []
	nbr_first_authorships = 0
	print("Publications: ", len(scholar.publications))
	counter = 0
	for p in scholar.publications:
	    print(p.title, " ", p.type, " ", p.journal)
	    co_authors = p.authors
	    # count first-authorships
	    if len(co_authors) > 0:
		    if co_authors[0] == rise_list[i]:
		    	nbr_first_authorships += 1
	    # count SCI journals
	    if p.type == "article":
	    	sci_list.append(p.title)
	    counter += 1
	    if counter>=500:
	    	break
	    	
	seed_ratio = nbr_first_authorships / len(scholar.publications)
	quality_ratio = len(sci_list) / len(scholar.publications)

	result_string = rise_list[i] + " (" + str(len(scholar.publications)) + " publ.) \t ### Seed ratio: " + str(seed_ratio) + " \t Quality ratio: " + str(quality_ratio) + "\n"
	print(result_string)

	f.write(result_string) 
	i += 1
	
f.close()

    