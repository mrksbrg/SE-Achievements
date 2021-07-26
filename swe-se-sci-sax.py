# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 2021

@author: Markus Borg
"""

import sys
import os.path
from datetime import date
import xml.sax
from swesesci.scholar_sax import SSSScholar
from swesesci.affiliation import SSSAffiliation
from swesesci.scholar_miner_sax import ScholarMiner
from swesesci.scholar_analyzer import ScholarAnalyzer
from swesesci.scholar_tabulator import ScholarTabulator
#from swesesci.scholar_visualizer import ScholarVisualizer

sss_scholars = []
sss_affiliations = []

def add_sss_scholars(process_list, affiliation):
    for person in process_list:
        name = person[0]
        url = person[1]
        # extract the pid from the url by substringing
        split1 = url.split("pid/")
        split2 = split1[1].split(".xml")
        pid = split2[0]

        sss_scholars.append(SSSScholar(name, -1, pid, url, affiliation, -1))
        tmp_aff = SSSAffiliation(affiliation)
        if tmp_aff not in sss_affiliations:
            tmp_aff.nbr_scholars += 1
            sss_affiliations.append(tmp_aff)
        else:
            curr = next((x for x in sss_affiliations if affiliation == x.name), None)
            curr.nbr_scholars += 1

# Swe-SE-SCI entry point
if (len(sys.argv) == 1):
    fast_list = [("Stefan Cedergren", "https://dblp.org/pid/116/6013.xml"),
                 ("Markus Borg", "https://dblp.org/pid/47/9384.xml"),
                 ("Krzysztof Wnuk", "https://dblp.org/pid/86/2856.xml"),
                 ("Mehrdad Saadatmand", "https://dblp.org/pid/14/9944.xml")]
    add_sss_scholars(fast_list, "Fast")

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
parser = xml.sax.make_parser()
# turn off namespaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
miner = ScholarMiner(filename_prefix, sss_scholars, sss_affiliations)
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
