# -*- coding: utf-8 -*-
"""
Created on Sat May 8 2021

@author: Markus Borg
"""

import sys
import os.path
from datetime import date
from swesesci.scholar import SSSScholar
from swesesci.affiliation import SSSAffiliation
from swesesci.scholar_miner import ScholarMiner
from swesesci.scholar_analyzer import ScholarAnalyzer
from swesesci.scholar_tabulator import ScholarTabulator

sss_scholars = []
sss_affiliations = []

def add_sss_scholars(process_list, affiliation):
    for name in process_list:
        words = name.split()
        # check if author has a running number
        if not words[len(words)-1].isdigit():
            sss_scholars.append(SSSScholar(name, -1, affiliation))
            tmp_aff = SSSAffiliation(affiliation)
            if tmp_aff not in sss_affiliations:
                tmp_aff.nbr_scholars += 1
                sss_affiliations.append(tmp_aff)
            else:
                curr = next((x for x in sss_affiliations if affiliation == x.name), None)
                curr.nbr_scholars += 1
        else:
            # author has a running number
            tmp_scholar = SSSScholar(' '.join(map(str, words[0:len(words)-1])), str(words[len(words)-1]), affiliation)
            sss_scholars.append(tmp_scholar)
            tmp_aff = SSSAffiliation(affiliation)
            if tmp_aff not in sss_affiliations:
                tmp_aff.nbr_scholars += 1
                sss_affiliations.append(tmp_aff)
            else:
                curr = next((x for x in sss_affiliations if affiliation == x.name), None)
                curr.nbr_scholars += 1

# Swe-SE-SCI entry point
if (len(sys.argv) == 1):
    # fast_list = ["Stefan Cedergren", "Joakim Fröberg", "Thomas Olsson 0001"]
    # add_sss_scholars(fast_list, "RISE")
    # fast_list2 = ["Philipp Haller", "David Broman", "Paris Carbone", "Elena Troubitsyna", "Richard Glassey", "Musard Balliu"]
    # add_sss_scholars(fast_list2, "MAU")
    # bfast_list_3 = ["Danny Weyns"]
    # add_sss_scholars(fast_list_3, "Linköping University")
    # big_names = ["Lionel C. Briand", "Barry W. Boehm", "David Lorge Parnas", "Barbara A. Kitchenham", "Brad A. Myers", "Marlon Dumas", "Mark Harman"]
    # add_sss_scholars(big_names, "Misc.")

    sweden_list = ["Robert Feldt", "Tony Gorschek", "Daniel Méndez Fernández", "Martin Monperrus", "Per Runeson", "Markus Borg"]
    add_sss_scholars(sweden_list, "Sweden")
    usa_list = ["Thomas Zimmermann 0001", "Atif M. Memon", "Laurie A. Williams", "Barry W. Boehm", "Jeffrey C. Carver", "Scott D. Fleming",
                   "Miryung Kim", "Andrian Marcus", "Tim Menzies", "Audris Mockus", "Emerson R. Murphy-Hill", "Nachiappan Nagappan",
                   "A. Jefferson Offutt", "Denys Poshyvanyk", "Gregg Rothermel", "Elaine J. Weyuker", "Tingting Yu", "René Just"]
    add_sss_scholars(usa_list, "Canada")
    usa_list = ["Daniel M. Berry", "Daniela E. Damian", "Ahmed E. Hassan", "Martin P. Robillard", "Bram Adams", "Daniel Amyot",
                "Neil E. Ernst", "Hadi Hemmati", "Sarah Nadi", "Meiyappan Nagappan", "Lin Tan"]
    add_sss_scholars(usa_list, "USA")

# Process scholar provided in the argument
else:
    custom_list = []
    custom_list.append(sys.argv[1])
    add_sss_scholars(custom_list, "N/A")

# Prepare the process
subdirectory = "output"
try:
    os.mkdir(subdirectory)
except Exception:
    pass
filename_prefix = os.path.join(subdirectory, str(date.today()) + "_sss_")

# 1. Mine the scholars, write the results
print("####### Step 1 - Mining scholars #######")
miner = ScholarMiner(filename_prefix, sss_scholars, sss_affiliations)
miner.process_group()
miner.write_results()
sss_scholars = miner.get_scholars()

# 2. Analyze the scholars, remove affiliations with no first-authored SCI publications, write the results
print("\n####### Step 2 - Analyzing scholars #######")
for scholar in sss_scholars:
    curr = next((x for x in sss_affiliations if scholar.affiliation == x.name), None)
    curr.nbr_first_sci += scholar.nbr_first_sci
tmp_affiliations = []
for affiliation in sss_affiliations:
    # keep only affiliations with SSS scholars
    if affiliation.nbr_first_sci > 0:
        tmp_affiliations.append(affiliation)
sss_affiliations = tmp_affiliations
analyzer = ScholarAnalyzer(filename_prefix, sss_scholars, sss_affiliations)
analyzer.analyze_individual_research_interests()
analyzer.analyze_affiliation_topics()
analyzer.write_results()

# 3. Tabulate the scholars, write the results
print("\n####### Step 3 - Tabulating scholars #######")
sss_scholars.sort(reverse=True)
sss_affiliations.sort(reverse=True)
tabulator = ScholarTabulator(filename_prefix, sss_scholars, sss_affiliations)
tabulator.write_tables()

# 4. Visualize the results, save to files
#visualizer = ScholarVisualizer(filename_prefix)
