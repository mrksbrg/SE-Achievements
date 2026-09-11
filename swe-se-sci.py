# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 2021

@author: Markus Borg
"""

import sys
import os.path
from datetime import date
import csv
from swesesci.scholar import SSSScholar
from swesesci.affiliation import SSSAffiliation
from swesesci.scholar_reader import ScholarReader
from swesesci.scholar_miner import ScholarMiner
from swesesci.scholar_analyzer import ScholarAnalyzer
from swesesci.scholar_tabulator import ScholarTabulator
#from swesesci.scholar_visualizer import ScholarVisualizer

sss_scholars = []
sss_affiliations = []

# Swe-SE-SCI entry point
subdirectory = "output"
try:
    os.mkdir(subdirectory)
except Exception:
    pass
filename_prefix = os.path.join(subdirectory, str(date.today()) + "_sss_")

# 1. Read candidate scholars from CSV-file
print("\n####### Step 1 - Reading candidate scholars #######")
reader = ScholarReader("input_scholars.csv")
sss_scholars, sss_affiliations = reader.read_candidate_scholars()

# 2. Mine the scholars from the local DBLP dump (see download_dblp_dump.py), write the results
print("\n####### Step 2 - Mining scholars #######")
miner = ScholarMiner(filename_prefix, sss_scholars, sss_affiliations)
miner.parse_scholars()
miner.write_results()
sss_scholars = miner.get_scholars()

# 3. Analyze the scholars, remove affiliations with no first-authored SCI publications, write the results
print("\n####### Step 3 - Analyzing scholars #######")
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

# 4. Tabulate the scholars, write the results
print("\n####### Step 4 - Tabulating scholars #######")
sss_scholars.sort(reverse=True)
sss_affiliations.sort(reverse=True)
tabulator = ScholarTabulator(filename_prefix, sss_scholars, sss_affiliations)
tabulator.write_tables()

# 5. Visualize the results, save to files
#visualizer = ScholarVisualizer(filename_prefix)
