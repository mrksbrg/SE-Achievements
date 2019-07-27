# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 17:19:46 2019

@author: Markus Borg
"""

from scholar import SWESEScholar
from scholar_miner import ScholarMiner
from scholar_analyzer import ScholarAnalyzer
from scholar_tabulator import ScholarTabulator
from scholar_visualizer import ScholarVisualizer
import sys
import os.path
from datetime import date

swese_scholars = []
def add_swese_scholars(process_list, affiliation):
	for name in process_list:
		swese_scholars.append(SWESEScholar(name, affiliation))

if (len(sys.argv) == 1):
    fast_list = ["Stefan Cedergren", "Joakim Fröberg"]
    add_swese_scholars(fast_list, "RISE")
    fast_list2 = ["Annabella Loconsole"]
    add_swese_scholars(fast_list2, "MAU")
    #fast_list_3 = ["Kristian Sandahl"]
    #add_swese_scholars(fast_list_3, "Linköping University")

    # rise_list = ["Niklas Mellegård", "Efi Papatheocharous", "Mehrdad Saadatmand", "Pasqualina Potena", "Markus Borg", "Ulrik Franke",
    #              "Ana Magazinius", "Joakim Fröberg", "Thomas Olsson", "Stefan Cedergren", "Stig Larsson", "Jakob Axelsson"]
    # add_swese_scholars(rise_list, "RISE Research Institutes of Sweden AB")
    # lu_list = ["Per Runeson", "Björn Regnell", "Martin Höst", "Elizabeth Bjarnason", "Emelie Engström"]
    # add_swese_scholars(lu_list, "Lund University")
    # bth_list = ["Claes Wohlin", "Tony Gorschek", "Krzysztof Wnuk", "Michael Unterkalmsteiner", "Michael Mattsson",
    #             "Mikael Svahnberg", "Darja Smite", "Michael Felderer", "Jürgen Börstler", "Emil Alégroth", "Ali Nauman", "Fabian Fagerholm", "Javier Gonzalez Huerta", "Muhammad Usman"]
    # add_swese_scholars(bth_list, "Blekinge Institute of Technology")
    # gbg_list = ["Rogardt Heldal", "Kenneth Lind", "Patrizio Pelliccione", "Riccardo Scandariato", "Miroslaw Staron", "Jan-Philipp Steghöfer", "Christian Berger", "Robert Feldt", "Richard Torkar", "Ivica Crnkovic",
    #                  "Richard Berntsson-Svensson", "Francisco Gomes", "Gregory Gay", "Michel Chaudron", "Jan Bosch", "Jennifer Horkoff",
    #                  "Eric Knauss", "Thorsten Berger", "Gul Calikli", "Regina Hebig", "Philipp Leitner", "Agneta Nilsson"]
    # add_swese_scholars(gbg_list, "Chalmers / Gothenburg University")
    # kth_list = ["Martin Monperrus", "Frederic Loiret", "Karl Meinke", "Benoit Baudry", "Pontus Johnson", "Robert Lagerström", "Mathias Ekstedt"]
    # add_swese_scholars(kth_list, "KTH Royal Institute of Technology")
    # su_list = []
    # add_swese_scholars(su_list, "Stockholm University")
    # malmo_list = ["Helena Holmström Olsson", "Annabella Loconsole"]
    # add_swese_scholars(malmo_list, "Malmö University")
    # linkoping_list = ["Kristian Sandahl"]
    # add_swese_scholars(linkoping_list, "Linköping University")
    # mdh_list = ["Markus Bohlin", "Raffaela Mirandola", "Alessio Bucaioni", "Hans Hansson", "Jan Carlsson", "Antonio Cicchetti", "Federico Ciccozzi", "Séverine Sentilles",
    #             "Kristina Lundqvist", "Daniel Sundmark", "Wasif Afzal", "Adnan Causevic", "Eduard Paul Enoiu", "Barbara Gallina", "Mikael Sjödin"]
    # add_swese_scholars(mdh_list, "Mälardalen University")
    # linne_list = ["Jesper Andersson", "Morgan Ericsson", "Narges Khakpour", "Danny Weyns", "Welf Löwe", "Francesco Flammini", "Francis Palma", "Andreas Kerren", "Rafael Messias Martins"]
    # add_swese_scholars(linne_list, "Linneaus Univerity")
    # skovde_list = ["Björn Lundell", "Sten Andler", "Birgitta Lindström"]
    # add_swese_scholars(skovde_list, "Skövde University")
    # karlstad_list = ["Sebastian Herold"]
    # add_swese_scholars(karlstad_list, "Karlstad University")
    # jonkoping_list = ["Anders Adlemo"]
    # add_swese_scholars(jonkoping_list, "Jönköping University")
else:
    custom_list = []
    custom_list.append(sys.argv[1])
    add_swese_scholars(custom_list, "N/A")

# Prepare the process    
#process_list = fast_list
subdirectory = "db"
try:
    os.mkdir(subdirectory)
except Exception:
    pass
filename_prefix = os.path.join(subdirectory, str(date.today()) + "_swese_")

# 1. Mine the scholars, write the results
print("####### Step 1 - Mining scholars #######")
miner = ScholarMiner(swese_scholars, filename_prefix)
miner.process_group()
miner.write_results()
swese_scholars = miner.get_scholars()

# 2. Analyze the scholars, write the results
print("\n####### Step 2 - Analyzing scholars #######")
analyzer = ScholarAnalyzer(filename_prefix, swese_scholars)
analyzer.analyze_individual_research_interests()
analyzer.analyze_affiliation_topics()
analyzer.write_results()

# 3. Tabulate the scholars, write the results
tabulator = ScholarTabulator(filename_prefix, swese_scholars)
tabulator.write_table()

# 4. Visualize the results, save to files
#visualizer = ScholarVisualizer(filename_prefix)


