# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 23:57:13 2019

@author: Markus Borg
"""

from scholar_miner import ScholarMiner
from scholar_analyzer import ScholarAnalyzer
from scholar_writer import ScholarWriter
from scholar_visualizer import ScholarVisualizer 

import os.path
from datetime import date

fast_list = {"Stefan Cedergren":False}
rise_list = {"Niklas Mellegård":False, "Efi Papatheocharous": False, "Mehrdad Saadatmand": False, "Pasqualina Potena": False, "Markus Borg": False, "Ulrik Franke": False,
			  "Ana Magazinius": False, "Joakim Fröberg": False, "Thomas Olsson": False, "Stefan Cedergren": False, "Stig Larsson":False, "Jakob Axelsson": False}
lu_list = {"Per Runeson": False, "Björn Regnell": False, "Martin Höst": False, "Elizabeth Bjarnason": False, "Emelie Engström": False}
bth_list = {"Claes Wohlin": False, "Tony Gorschek": False, "Krzysztof Wnuk": False, "Michael Unterkalmsteiner": False, "Michael Mattsson": False,
			"Mikael Svahnberg": False, "Darja Smite": False, "Michael Felderer": False, "Jürgen Börstler": False, "Emil Alégroth": False, "Ali Nauman": False, "Fabian Fagerholm": False, "Javier Gonzalez Huerta": False, "Muhammad Usman": False}
chalmers_list = {"Rogardt Heldal":False, "Kenneth Lind":False, "Patrizio Pelliccione": False, "Riccardo Scandariato": False, "Miroslaw Staron": False, "Jan-Philipp Steghöfer": False, "Christian Berger": False, "Robert Feldt": False, "Richard Torkar": False, "Ivica Crnkovic": False,
				 "Richard Berntsson-Svensson": False, "Francisco Gomes": False, "Gregory Gay": False, "Michel Chaudron": False, "Jan Bosch": False, "Jennifer Horkoff": False, 
				 "Eric Knauss": False, "Thorsten Berger": False, "Gul Calikli": False, "Regina Hebig": False, "Philipp Leitner":False, "Agneta Nilsson":False}
kth_list = {"Martin Monperrus": False, "Frederic Loiret": False, "Karl Meinke": False, "Benoit Baudry": False, "Pontus Johnson":False, "Robert Lagerström":False, "Mathias Ekstedt":False}
malmo_list = {"Helena Holmström Olsson": False, "Annabella Loconsole": False}
linkoping_list = {"Kristian Sandahl": False}
mdh_list = {"Markus Bohlin":False, "Raffaela Mirandola":False, "Alessio Bucaioni":False, "Hans Hansson": False, "Jan Carlsson": False, "Antonio Cicchetti": False, "Federico Ciccozzi": False, "Séverine Sentilles": False,
			"Kristina Lundqvist": False, "Daniel Sundmark": False, "Wasif Afzal": False, "Adnan Causevic": False, "Eduard Paul Enoiu": False, "Barbara Gallina":False, "Mikael Sjödin":False}
linne_list = {"Jesper Andersson": False, "Morgan Ericsson":False, "Narges Khakpour":False, "Danny Weyns":False, "Welf Löwe":False, "Francesco Flammini":False, "Francis Palma":False, "Andreas Kerren":False, "Rafael Messias Martins":False}
skovde_list = {"Björn Lundell":False, "Sten Andler":False, "Birgitta Lindström":False}
karlstad_list = {"Sebastian Herold":False}
jonkoping_list = {"Anders Adlemo":False}
ericsson_list = {"Sigrid Eldh":False, "Kristian Wiklund":False, "Leif Jonsson":False, "Sahar Tahvili":False}
others_list = {"":False}
merged_list = {**rise_list, **linne_list, **ericsson_list}
all_list = {**rise_list, **lu_list, **bth_list, **chalmers_list, **kth_list, **malmo_list, **linkoping_list, **mdh_list, **linne_list, **skovde_list, **karlstad_list, **ericsson_list}

def write_coauthors_and_candidates():
    try:
        miner.write_coauthors_csv()
        miner.write_candidate_SEScholars_csv(process_list)
    except:
        print("Could not write csv-files with co-authors and candidate SEScholars")

# Prepare the process    
process_list = fast_list
subdirectory = "db"
try:
    os.mkdir(subdirectory)
except Exception:
    pass
filename_prefix = os.path.join(subdirectory, str(date.today()) + "_se_sweden_")

# Mine the scholars 
miner = ScholarMiner(process_list, filename_prefix)
miner.process_group(process_list)
miner.write_results()

write_coauthors_and_candidates()
miner.write_author_titles()

# Analyze the scholars
analyzer = ScholarAnalyzer(str(date.today()) + "_Authors_all_titles.csv")

# Write the scholars
writer = ScholarWriter(None)

# Visualize the results
visualizer = ScholarVisualizer(str(date.today()) + "_Authors_all_titles.csv")
visualizer.preprocess()
visualizer.visualize()
