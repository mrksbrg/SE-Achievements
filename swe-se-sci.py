# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 17:19:46 2019

@author: Markus Borg
"""

from scholar import SSSScholar
from affiliation import SSSAffiliation
from scholar_miner import ScholarMiner
from scholar_analyzer import ScholarAnalyzer
from scholar_tabulator import ScholarTabulator
import sys
import os.path
from datetime import date

sss_scholars = []
sss_affiliations = []

def add_sss_scholars(process_list, affiliation):
    for name in process_list:
        sss_scholars.append(SSSScholar(name, affiliation))
        tmp_aff = SSSAffiliation(affiliation)
        if tmp_aff not in sss_affiliations:
            tmp_aff.nbr_scholars += 1
            sss_affiliations.append(tmp_aff)
        else:
            curr = next((x for x in sss_affiliations if affiliation == x.name), None)
            curr.nbr_scholars += 1

if (len(sys.argv) == 1):
    # fast_list = ["Stefan Cedergren", "Joakim Fröberg", "Thomas Olsson"]
    # add_sss_scholars(fast_list, "RISE")
    # fast_list2 = ["Annabella Loconsole"]
    # add_sss_scholars(fast_list2, "MAU")
    # fast_list_3 = ["Kristian Sandahl"]
    # add_sss_scholars(fast_list_3, "Linköping University")
    # big_names = ["Lionel C. Briand", "Barry W. Boehm", "David Lorge Parnas", "Barbara A. Kitchenham", "Brad A. Myers", "Marlon Dumas", "Mark Harman"]
    # add_sss_scholars(big_names, "Misc.")

    rise_list = ["Niklas Mellegård", "Efi Papatheocharous", "Mehrdad Saadatmand", "Pasqualina Potena", "Markus Borg", "Ulrik Franke",
                  "Ana Magazinius", "Joakim Fröberg", "Thomas Olsson", "Stefan Cedergren", "Stig Larsson", "Jakob Axelsson", "Markus Bohlin"]
    add_sss_scholars(rise_list, "RISE Research Institutes of Sweden AB")
    lu_list = ["Per Runeson", "Björn Regnell", "Martin Höst", "Elizabeth Bjarnason", "Emelie Engström", "Christin Lindholm", "Christoph Reichenbach", "Görel Hedin", "Martina Maggio"]
    add_sss_scholars(lu_list, "Lund University")
    bth_list = ["Claes Wohlin", "Tony Gorschek", "Krzysztof Wnuk", "Michael Unterkalmsteiner", "Michael Mattsson",
                "Mikael Svahnberg", "Darja Smite", "Michael Felderer", "Jürgen Börstler", "Emil Alégroth", "Ali Nauman", "Fabian Fagerholm", "Javier Gonzalez Huerta", "Muhammad Usman",
                "Davide Fucci", "Daniel Méndez Fernández", "Nauman Bin Ali"]
    add_sss_scholars(bth_list, "Blekinge Institute of Technology")
    gbg_list = ["Rogardt Heldal", "Kenneth Lind", "Patrizio Pelliccione", "Riccardo Scandariato", "Miroslaw Staron", "Jan-Philipp Steghöfer", "Christian Berger", "Robert Feldt", "Richard Torkar", "Ivica Crnkovic",
                     "Richard Berntsson-Svensson", "Francisco Gomes", "Gregory Gay", "Michel Chaudron", "Jan Bosch", "Jennifer Horkoff",
                     "Eric Knauss", "Thorsten Berger", "Gul Calikli", "Regina Hebig", "Philipp Leitner", "Agneta Nilsson"]
    add_sss_scholars(gbg_list, "Chalmers / Gothenburg University")
    kth_list = ["Martin Monperrus", "Frederic Loiret", "Karl Meinke", "Benoit Baudry", "Pontus Johnson", "Robert Lagerström", "Mathias Ekstedt", "Martin Törngren", "David Broman"]
    add_sss_scholars(kth_list, "KTH Royal Institute of Technology")
    su_list = ["Janis Stirna", "Jelena Zdravkovic"]
    add_sss_scholars(su_list, "Stockholm University")
    malmo_list = ["Helena Holmström Olsson", "Annabella Loconsole", "Patrik Berander", "Carl Magnus Olsson", "Jeanette Eriksson"]
    add_sss_scholars(malmo_list, "Malmö University")
    linkoping_list = ["Kristian Sandahl", "Peter Fritzson", "Mariam Kamkar"]
    add_sss_scholars(linkoping_list, "Linköping University")
    mdh_list = ["Markus Bohlin", "Raffaela Mirandola", "Alessio Bucaioni", "Hans Hansson", "Jan Carlsson", "Antonio Cicchetti", "Federico Ciccozzi", "Séverine Sentilles",
                "Kristina Lundqvist", "Daniel Sundmark", "Wasif Afzal", "Adnan Causevic", "Eduard Paul Enoiu", "Barbara Gallina", "Mikael Sjödin", "Daniel Flemström"]
    add_sss_scholars(mdh_list, "Mälardalen University")
    linne_list = ["Jesper Andersson", "Morgan Ericsson", "Narges Khakpour", "Danny Weyns", "Welf Löwe", "Francesco Flammini", "Francis Palma", "Andreas Kerren", "Rafael Messias Martins"]
    add_sss_scholars(linne_list, "Linneaus Univerity")
    skovde_list = ["Björn Lundell", "Sten Andler", "Birgitta Lindström", "Henrik Gustavsson", "Jonas Gamalielsson", "Simon Butler"]
    add_sss_scholars(skovde_list, "Skövde University")
    karlstad_list = ["Sebastian Herold"]
    add_sss_scholars(karlstad_list, "Karlstad University")
    jonkoping_list = ["Anders Adlemo", "Niklas Lavesson"]
    add_sss_scholars(jonkoping_list, "Jönköping University")
    orebro_list = ["Panagiota Chatzipetrou"]
    add_sss_scholars(orebro_list, "Örebro University")
    halmstad_university = ["Walid Taha"]
    add_sss_scholars(halmstad_university, "Halmstad University")

else:
    custom_list = []
    custom_list.append(sys.argv[1])
    add_sss_scholars(custom_list, "N/A")

# Prepare the process
subdirectory = "db"
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
