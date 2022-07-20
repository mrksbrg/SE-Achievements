# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 2021

@author: Markus Borg
"""

import sys
import os.path
from datetime import date
import csv
import xml.sax
import ssl
from swesesci.scholar import SSSScholar
from swesesci.affiliation import SSSAffiliation
from swesesci.scholar_miner import ScholarMiner
from swesesci.scholar_analyzer import ScholarAnalyzer
from swesesci.scholar_tabulator import ScholarTabulator
#from swesesci.scholar_visualizer import ScholarVisualizer

sss_scholars = []
sss_affiliations = []

def string_splitter(scholar_string):
    affiliation = scholar_string[0]
    name = scholar_string[1]
    running_number = scholar_string[2]
    url = scholar_string[3]

    try:
        split1 = url.split("pid/")
        split2 = split1[1].split(".xml")
        pid = split2[0]
    except IndexError:
        print("Invalid format of input XML URL. (" + name + ")")
        return

    return affiliation, name, running_number, pid, url

def get_affiliation_list(scholars):
    tmp_list = []
    for scholar in scholars:
        tmp_aff = SSSAffiliation(scholar.affiliation)
        existing_aff = tmp_aff in sss_affiliations

        if existing_aff is False:
            tmp_aff.nbr_scholars += 1
            tmp_list.append(tmp_aff)
        else:
            existing_aff.nbr_scholars += 1

    return tmp_list

# Swe-SE-SCI entry point
if (len(sys.argv) == 1):
    with open('input_scholars.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        candidate_scholars = list(reader)

    scholar_list = list(map(string_splitter, candidate_scholars))
    [sss_scholars.append(SSSScholar(x[1], x[2], x[3], x[4], x[0], -1)) for x in scholar_list]
    sss_affiliations = get_affiliation_list(sss_scholars)

# Process scholar provided in the argument
else:
    specific_scholar = (sys.argv[1], sys.argv[2], sys.argv[3])
    custom_list = []
    custom_list.append(specific_scholar)
    add_sss_scholars(custom_list, "N/A")

# 0. Prepare the process
subdirectory = "output"
try:
    os.mkdir(subdirectory)
except Exception:
    pass
filename_prefix = os.path.join(subdirectory, str(date.today()) + "_sss_")

# 1. Mine the scholars, write the results
print("####### Step 1 - Mining scholars #######")
parser = xml.sax.make_parser()
# turn off namespaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
miner = ScholarMiner(filename_prefix, sss_scholars, sss_affiliations)
ssl._create_default_https_context = ssl._create_unverified_context
miner.parse_scholars()
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
