# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 23:57:13 2019

@author: Markus Borg
"""

from datetime import date
import dblp
from scopus import AuthorRetrieval


rise_list2 = {
			  #"Efi Papatheocharous": False,
			  #"Mehrdad Saadatmand": False,
			  #"Pasqualina Potena": False,
			  #"Markus Borg": False, }
			  #"Ulrik Franke": False,
			  "Ana Magazinius": False,
			  "Joakim Fröberg": False,
			  "Thomas Olsson": False,
			  "Stefan Cedergren": False,
			  #"Jakob Axelsson": False, 
			  }


rise_list = ["Efi Papatheocharous", "Mehrdad Saadatmand", "Pasqualina Potena", "Markus Borg", "Ulrik Franke", "Ana Magazinius", "Joakim Fröberg", "Thomas Olsson", "Stefan Cedergren", "Jakob Axelsson"]
lu_list = ["Per Runeson", "Björn Regnell", "Martin Höst", "Elizabeth Bjarnason", "Emelie Engström"]
bth_list = ["Claes Wohlin", "Tony Gorschek", "Krzysztof Wnuk", "Michael Unterkalmsteiner", "Michael Mattsson", "Mikael Svahnberg", "Darja Smite", "Michael Felderer", "Jürgen Börstler"] #"Emil Alégroth", "Ali Nauman", "Fabian Fagerholm", "Javier Gonzalez Huerta", "Muhammad Usman"
chalmers_list = ["Patrizio Pelliccione", "Riccardo Scandariato", "Miroslaw Staron", "Jan-Philipp Steghöfer", "Christian Berger", "Robert Feldt", "Richard Torkar", "Ivica Crnkovic", "Richard Berntsson Svensson", "Francisco Gomes", "Gregory Gay", "Michel Chaudron", "Jan Bosch", "Eric Knauss", "Jennifer Horkoff","Eric Knauss", "Thorsten Berger", "Gul Calikli", "Regina Hebig"] #"Philipp Leitner", "Agneta Nilsson", "Håkan Burden",
kth_list = ["Martin Monperrus","Frederic Loiret", "Karl Meinke", "Benoit Baudry"]
malmo_list = ["Helena Holmström Olsson", "Annabella Loconsole"]
linkoping_list = ["Kristian Sandahl"]
mdh_list = ["Hans Hansson", "Jan Carlsson", "Antonio Cicchetti", "Federico Ciccozzi", "Séverine Sentilles", "Kristina Lundqvist", "Daniel Sundmark", "Wasif Afzal", "Adnan Causevic", "Eduard Paul Enoiu"]
linne_list = ["Jesper Andersson"]
affiliation_list = rise_list

sci_list = ["IEEE Trans. Software Eng.", "Empirical Software Engineering", "ACM Trans. Softw. Eng. Methodol.", "Autom. Softw. Eng.", "Information & Software Technology", "Requir. Eng.", " Software and System Modeling", "Software Quality Journal", "Journal of Systems and Software", "Journal of Software: Evolution and Process", "Softw. Test., Verif. Reliab.", "Softw., Pract. Exper.", "IET Software", "International Journal of Software Engineering and Knowledge Engineering"]

x = date.today()
print(x.day)
#f = open(str(x) + "_RISE_output.txt","w+")
f = open(str(x) + "_LU_output.txt","w+")
i = 0
nbr_remaining = len(rise_list2)

while nbr_remaining > 0:
	for scholar, processed in rise_list2.items():
		if  not processed:
			print(scholar)
			authors = dblp.search(scholar)

			search_res = authors[0]
			nbr_publications = len(search_res.publications)
			top_papers = []
			nbr_arxiv = 0
			nbr_first_authorships = 0
			nbr_first_top = 0
			print("DBLP entries: ", nbr_publications)
			counter = 0
			for p in search_res.publications:
			    print(p.title, " ", p.type, " ", p.journal)
			    co_authors = p.authors
			    # count SCI journals and how many as first author
			    if p.type == "article":
			    	if p.journal == "CoRR": #skip ArXiv preprints
			    		nbr_arxiv += 1
			    		continue
			    	elif p.journal in sci_list:
			    		top_papers.append(p.title)
			    		print("added!")
			    		if (co_authors[0] == scholar):
			    			nbr_first_top += 1
			    # count ICSE papers?
			    #if p.type == "inproceedings":# and p.journal == "ICSE"
			    	#print("CONF: ", p.publisher)
			    # count first-authorships in general
			    if len(co_authors) > 0:
				    if co_authors[0] == scholar:
				    	nbr_first_authorships += 1   
				    	
			    counter += 1
			    if counter>=1000:
			    	break
			
			nbr_publications -= nbr_arxiv
			seed_ratio = nbr_first_authorships / nbr_publications
			quality_ratio = len(top_papers) / nbr_publications

			result_string = scholar + " (" + str(nbr_publications) + " publ., First-in-top: " + str(nbr_first_top) + ") \t\t ### Self-made ratio: " + str(seed_ratio) + " \t Quality ratio: " + str(quality_ratio) + "\n"
			
			#result_string = affiliation_list[i] + " (" + str(nbr_publications) + " publ., First-in-top: " + str(nbr_first_top) + ") \t\t ### Self-made ratio: " + str(seed_ratio) + " \t Quality ratio: " + str(quality_ratio) + "\n"
			print(result_string)
			processed = True
			nbr_remaining -= 1

		f.write(result_string) 
		i += 1
	
f.close()

    