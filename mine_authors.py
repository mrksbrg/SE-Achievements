# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 23:57:13 2019

@author: Markus Borg
"""

from datetime import date
import time
import dblp
from scopus import AuthorRetrieval

fast_list = {"Ana Magazinius": False, "Joakim Fröberg": False, "Thomas Olsson": False, "Stefan Cedergren": False}
rise_list = {"Efi Papatheocharous": False, "Mehrdad Saadatmand": False, "Pasqualina Potena": False, "Markus Borg": False, "Ulrik Franke": False,
			  "Ana Magazinius": False, "Joakim Fröberg": False, "Thomas Olsson": False, "Stefan Cedergren": False, "Jakob Axelsson": False}
lu_list = {"Per Runeson": False, "Björn Regnell": False, "Martin Höst": False, "Elizabeth Bjarnason": False, "Emelie Engström": False}
bth_list = {"Claes Wohlin": False, "Tony Gorschek": False, "Krzysztof Wnuk": False, "Michael Unterkalmsteiner": False, "Michael Mattsson": False,
			"Mikael Svahnberg": False, "Darja Smite": False, "Michael Felderer": False, "Jürgen Börstler": False} #"Emil Alégroth", "Ali Nauman", "Fabian Fagerholm", "Javier Gonzalez Huerta", "Muhammad Usman"
chalmers_list = {"Patrizio Pelliccione": False, "Riccardo Scandariato": False, "Miroslaw Staron": False, "Jan-Philipp Steghöfer": False, "Christian Berger": False, "Robert Feldt": False, "Richard Torkar": False, "Ivica Crnkovic": False,
				 "Richard Berntsson Svensson": False, "Francisco Gomes": False, "Gregory Gay": False, "Michel Chaudron": False, "Jan Bosch": False, "Eric Knauss": False, "Jennifer Horkoff": False, 
				 "Eric Knauss": False, "Thorsten Berger": False, "Gul Calikli": False, "Regina Hebig": False} #"Philipp Leitner", "Agneta Nilsson"
kth_list = {"Martin Monperrus": False, "Frederic Loiret": False, "Karl Meinke": False, "Benoit Baudry": False}
malmo_list = {"Helena Holmström Olsson": False, "Annabella Loconsole": False}
linkoping_list = {"Kristian Sandahl": False}
mdh_list = {"Hans Hansson": False, "Jan Carlsson": False, "Antonio Cicchetti": False, "Federico Ciccozzi": False, "Séverine Sentilles": False,
			"Kristina Lundqvist": False, "Daniel Sundmark": False, "Wasif Afzal": False, "Adnan Causevic": False, "Eduard Paul Enoiu": False}
linne_list = {"Jesper Andersson": False}
affiliation_list = rise_list

sci_list = ["IEEE Trans. Software Eng.", "Empirical Software Engineering", "ACM Trans. Softw. Eng. Methodol.", "Autom. Softw. Eng.", "Information & Software Technology", "Requir. Eng.", " Software and System Modeling", "Software Quality Journal", "Journal of Systems and Software", "Journal of Software: Evolution and Process", "Softw. Test., Verif. Reliab.", "Softw., Pract. Exper.", "IET Software", "International Journal of Software Engineering and Knowledge Engineering"]

class Scholar:  
    def __init__(self, name):
        self.name = name        
        self.sci_list = list()
        
    def __str__(self):
        return self.name + " (" + str(len(self.sci_list)) + " SCI publications)"
        
    def addPublication(self, pubKey):
        self.pubList.append(pubKey)
        
try:
	x = date.today()
	print(x.day)
	f = open(str(x) + "_output.txt","w+")
	nbr_remaining = len(affiliation_list)
except:
	print("Could not open file.")

while nbr_remaining > 0:
	for scholar, processed in affiliation_list.items():	
		if not processed: # only proceed if the scholar hasn't been processed already
			try:
				print("Processing scholar: " + scholar)
				authors = dblp.search(scholar)
				search_res = authors[0]
			except:
				print("ERROR: Invalid search result from DBLP. Waiting...")
				time.sleep(5)
				break

			# initiate variables
			nbr_publications = len(search_res.publications)
			print("DBLP entries: ", nbr_publications)
			top_papers = []
			nbr_arxiv = 0
			nbr_first_authorships = 0
			nbr_first_top = 0
			total_text = ""
				
			# traverse publications
			for p in search_res.publications:
				try:
					print(p.title, " ", p.type, " ", p.journal)
					co_authors = p.authors
					# count SCI journals and how many as first author
					if p.type == "article":
						if p.journal == "CoRR": #skip ArXiv preprints
				   			nbr_arxiv += 1
				   			continue
						elif p.journal in sci_list:
				   			top_papers.append(p.title)
				   			if (co_authors[0] == scholar):
				   				nbr_first_top += 1
				   				total_text += "-" + p.title + "\n"
						if len(co_authors) > 0:
							if co_authors[0] == scholar:
								nbr_first_authorships += 1
					    #print(co_authors) # used to find authors with a number, e.g., "Thomas Olsson 0001".
				except:
					print("ERROR. Processing one of the papers failed. Waiting...")
					time.sleep(5)
					break
			nbr_publications -= nbr_arxiv
			seed_ratio = nbr_first_authorships / nbr_publications
			quality_ratio = len(top_papers) / nbr_publications

			result_string = "\n" + scholar + " (" + str(nbr_publications) + " publ., First-in-top: " + str(nbr_first_top) + ") \t\t ### Self-made ratio: " + str(seed_ratio) + " \t Quality ratio: " + str(quality_ratio) + "\n"
			result_string += total_text
			processed = True
			print("Scholar processed: " + scholar)
			nbr_remaining -= 1
		f.write(result_string)
	
f.close()

    