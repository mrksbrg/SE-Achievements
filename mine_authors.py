# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 23:57:13 2019

@author: Markus Borg
"""

from scholar_miner import ScholarMiner

fast_list = {"Annabella Loconsole": False, "Niklas Mellegård":False}
rise_list = {"Niklas Mellegård":False, "Efi Papatheocharous": False, "Mehrdad Saadatmand": False, "Pasqualina Potena": False, "Markus Borg": False, "Ulrik Franke": False,
			  "Ana Magazinius": False, "Joakim Fröberg": False, "Thomas Olsson": False, "Stefan Cedergren": False, "Jakob Axelsson": False}
lu_list = {"Per Runeson": False, "Björn Regnell": False, "Martin Höst": False, "Elizabeth Bjarnason": False, "Emelie Engström": False}
bth_list = {"Claes Wohlin": False, "Tony Gorschek": False, "Krzysztof Wnuk": False, "Michael Unterkalmsteiner": False, "Michael Mattsson": False,
			"Mikael Svahnberg": False, "Darja Smite": False, "Michael Felderer": False, "Jürgen Börstler": False, "Emil Alégroth": False, "Ali Nauman": False, "Fabian Fagerholm": False, "Javier Gonzalez Huerta": False, "Muhammad Usman": False}
chalmers_list = {"Patrizio Pelliccione": False, "Riccardo Scandariato": False, "Miroslaw Staron": False, "Jan-Philipp Steghöfer": False, "Christian Berger": False, "Robert Feldt": False, "Richard Torkar": False, "Ivica Crnkovic": False,
				 "Richard Berntsson Svensson": False, "Francisco Gomes": False, "Gregory Gay": False, "Michel Chaudron": False, "Jan Bosch": False, "Jennifer Horkoff": False, 
				 "Eric Knauss": False, "Thorsten Berger": False, "Gul Calikli": False, "Regina Hebig": False, "Philipp Leitner":False, "Agneta Nilsson":False}
kth_list = {"Martin Monperrus": False, "Frederic Loiret": False, "Karl Meinke": False, "Benoit Baudry": False}
malmo_list = {"Helena Holmström Olsson": False, "Annabella Loconsole": False}
linkoping_list = {"Kristian Sandahl": False}
mdh_list = {"Hans Hansson": False, "Jan Carlsson": False, "Antonio Cicchetti": False, "Federico Ciccozzi": False, "Séverine Sentilles": False,
			"Kristina Lundqvist": False, "Daniel Sundmark": False, "Wasif Afzal": False, "Adnan Causevic": False, "Eduard Paul Enoiu": False, "Barbara Gallina":False}
linne_list = {"Jesper Andersson": False}
ericsson_list = {"Sigrid Eldh":False, "Kristian Wiklund":False, "Leif Jonsson":False, "Sahar Tahvili":False}
others_list = {"":False}
merged_lists = {**rise_list, **linne_list, **ericsson_list}
#merged_lists = {**malmo_list, **linkoping_list}

#sci_list = ["IEEE Trans. Software Eng.", "Empirical Software Engineering", "ACM Trans. Softw. Eng. Methodol.", "Autom. Softw. Eng.", "Information & Software Technology", "Requir. Eng.", " Software and System Modeling", "Software Quality Journal", "Journal of Systems and Software", "Journal of Software: Evolution and Process", "Softw. Test., Verif. Reliab.", "Softw., Pract. Exper.", "IET Software", "International Journal of Software Engineering and Knowledge Engineering"]
        
scholars = {}

miner = ScholarMiner()

miner.process_group(fast_list)
miner.write_scholars()