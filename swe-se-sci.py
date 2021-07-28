# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 2021

@author: Markus Borg
"""

import sys
import os.path
from datetime import date
import xml.sax
from swesesci.scholar import SSSScholar
from swesesci.affiliation import SSSAffiliation
from swesesci.scholar_miner import ScholarMiner
from swesesci.scholar_analyzer import ScholarAnalyzer
from swesesci.scholar_tabulator import ScholarTabulator
#from swesesci.scholar_visualizer import ScholarVisualizer

sss_scholars = []
sss_affiliations = []

def add_sss_scholars(process_list, affiliation):
    for person in process_list:
        name = person[0]
        running_number = person[1]
        url = person[2]
        # extract the pid from the url by substringing
        try:
            split1 = url.split("pid/")
            split2 = split1[1].split(".xml")
            pid = split2[0]
        except IndexError:
            print("Invalid format of input XML URL.")
            return

        sss_scholars.append(SSSScholar(name, running_number, pid, url, affiliation, -1))
        tmp_aff = SSSAffiliation(affiliation)
        if tmp_aff not in sss_affiliations:
            tmp_aff.nbr_scholars += 1
            sss_affiliations.append(tmp_aff)
        else:
            curr = next((x for x in sss_affiliations if affiliation == x.name), None)
            curr.nbr_scholars += 1

# Swe-SE-SCI entry point
if (len(sys.argv) == 1):
    test_list = [("Stefan Cedergren", "-1", "https://dblp.org/pid/116/6013.xml")]
    #add_sss_scholars(test_list, "Fast test")
    rise_list = [("Niklas Mellegård", "-1", "https://dblp.org/pid/30/8216.xml"),
                 ("Efi Papatheocharous", "-1", "https://dblp.org/pid/76/302.xml"),
                 ("Mehrdad Saadatmand", "-1", "https://dblp.org/pid/14/9944.xml"),
                 ("Pasqualina Potena", "-1", "https://dblp.org/pid/49/2251.xml"),
                 ("Markus Borg", "-1", "https://dblp.org/pid/47/9384.xml"),
                 ("Ulrik Franke", "-1", "https://dblp.org/pid/71/3754.xml"),
                 ("Ana Magazinius", "-1", "https://dblp.org/pid/46/8694.xml"),
                 ("Jakob Axelsson", "-1", "https://dblp.org/pid/50/6797.xml"),
                 ("Håkan Burden", "-1", "https://dblp.org/pid/02/10779.xml"),
                 ("Peter Wallin", "-1", "https://dblp.org/pid/57/5749.xml"),
                 ("Piotr Tomaszewski", "-1", "https://dblp.org/pid/75/5273.xml"),
                 ("Thomas Olsson", "0001", "https://dblp.org/pid/31/5587-1.xml"),
                 ("Stig Larsson", "0002", "https://dblp.org/pid/77/1925-2.xml")]
    add_sss_scholars(rise_list, "RISE Research Institutes of Sweden")
    lu_list = [("Per Runeson", "-1", "https://dblp.org/pid/24/24.xml"),
               ("Björn Regnell", "-1", "https://dblp.uni-trier.de/pid/09/1284.xml"),
               ("Martin Höst", "-1", "https://dblp.uni-trier.de/pid/07/6594.xml"),
               ("Elizabeth Bjarnason", "-1", "https://dblp.uni-trier.de/pid/19/1459.xml"),
               ("Emelie Engström", "-1", "https://dblp.uni-trier.de/pid/31/2107.xml"),
               ("Christin Lindholm", "-1", "https://dblp.uni-trier.de/pid/20/851.xml"),
               ("Christoph Reichenbach", "-1", "https://dblp.uni-trier.de/pid/98/4527.xml"),
               ("Görel Hedin", "-1", "https://dblp.uni-trier.de/pid/95/987.xml"),
               ("Martina Maggio", "-1", "https://dblp.uni-trier.de/pid/02/8575.xml")]
    add_sss_scholars(lu_list, "Lund University")
    bth_list = [("Claes Wohlin", "-1", "https://dblp.org/pid/w/ClaesWohlin.xml"),
                ("Tony Gorschek", "-1", "https://dblp.org/pid/82/3504.xml"),
                ("Krzysztof Wnuk", "-1", "https://dblp.org/pid/86/2856.xml"),
                ("Michael Unterkalmsteiner", "-1", "https://dblp.org/pid/08/8212.xml"),
                ("Michael Mattsson", "-1", "https://dblp.org/pid/04/6269.xml"),
                ("Mikael Svahnberg", "-1", "https://dblp.org/pid/81/5477.xml"),
                ("Darja Smite", "-1", "https://dblp.org/pid/30/4138.xml"),
                ("Jürgen Börstler", "-1", "https://dblp.org/pid/b/JBorstler.xml"),
                ("Emil Alégroth", "-1", "https://dblp.org/pid/133/4686.xml"),
                ("Nauman Bin Ali", "-1", "https://dblp.org/pid/37/10608.xml"),
                ("Fabian Fagerholm", "-1", "https://dblp.org/pid/78/9972.xml"),
                ("Javier Gonzalez-Huerta", "-1", "https://dblp.org/pid/98/8522.xml"),
                ("Muhammad Usman", "0006", "https://dblp.org/pid/20/241-6.xml"),
                ("Davide Fucci", "-1", "https://dblp.org/pid/70/9016.xml"),
                ("Daniel Méndez Fernández", "-1", "https://dblp.org/pid/69/8522.xml"),
                ("Deepika Badampudi", "-1", "https://dblp.org/pid/130/6487.xml"),
                ("Emilia Mendes", "-1", "https://dblp.org/pid/m/EMendes.xml"),
                ("Ludwik Kuzniarz", "-1", "https://dblp.org/pid/26/532.xml"),
                ("Lars Lundberg", "-1", "https://dblp.org/pid/58/356.xml"),
                ("Niklas Lavesson", "-1", "https://dblp.org/pid/55/1994.xml"),
                ("Ahmad Nauman Ghazi", "-1", "https://dblp.org/pid/156/2314.xml")]
    add_sss_scholars(bth_list, "Blekinge Institute of Technology")
    chalmers_list = [("Philipp Leitner", "0001", "https://dblp.org/pid/03/5268.xml")]
    add_sss_scholars(chalmers_list, "Chalmers / Gothenburg University")
    mdh_list = [("Alessio Bucaioni", "-1", "https://dblp.org/pid/143/4024.xml")]
    add_sss_scholars(mdh_list, "Mälardalen University")

# Process scholar provided in the argument
else:
    specific_scholar = (sys.argv[1], sys.argv[2], sys.argv[3])
    custom_list = []
    custom_list.append(specific_scholar)

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
