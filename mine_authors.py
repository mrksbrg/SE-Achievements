# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 23:57:13 2019

@author: Markus Borg
"""

from datetime import date
import dblp

#rise_list = ["Markus Borg", "Ulrik Franke", "Ana Magazinius", "Joakim Fröberg", "Thomas Olsson", "Stefan Cedergren", "Jakob Axelsson"]
#lu_list = ["Per Runeson", "Björn Regnell", "Martin Höst", "Elizabeth Bjarnason", "Emelie Engström"]
bth_list = [ "Efi Papatheocharous"] #"Emil Alégroth", "Ali Nauman", "Fabian Fagerholm", "Javier Gonzalez Huerta", "Muhammad Usman"] #["Claes Wohlin", "Tony Gorschek", "Krzysztof Wnuk", "Michael Unterkalmsteiner", "Michael Mattsson", "Mikael Svahnberg", "Darja Smite", "Michael Felderer", "Jürgen Börstler"]
chalmers_list = ["Jean-Philipp Steghöfer", "Christian Berger"] #"Robert Feldt", "Richard Torkar", "Ivica Crnkovic", "Richard Berntsson Svensson", "Francisco Gomes", "Gregory Gay", "Michel Chaudron", "Jan Bosch", "Eric Knauss", "Jennifer Horkoff","Eric Knauss", "Thorsten Berger", 
kth_list = ["Benoit Baudry", "Martin Montperrus"] # "Frederic Loiret", "Karl Meinke"
malmo_list = ["Helena Holmström Olsson", "Annabella Loconsole"]
linkoping_list = ["Kristian Sandahl"]
affiliation_list = bth_list

sci_list = ["IEEE Trans. Software Eng.", "Empirical Software Engineering", "ACM Trans. Softw. Eng. Methodol.", "Autom. Softw. Eng.", "Information & Software Technology", "Requir. Eng.", " Software and System Modeling", "Software Quality Journal", "Journal of Systems and Software", "Journal of Software: Evolution and Process", "Softw. Test., Verif. Reliab.", "Softw., Pract. Exper.", "IET Software", "International Journal of Software Engineering and Knowledge Engineering"]

x = date.today()
print(x.day)
#f = open(str(x) + "_RISE_output.txt","w+")
f = open(str(x) + "_LU_output.txt","w+")
i = 0

for scholar in affiliation_list:
	print(scholar)
	authors = dblp.search(scholar)

	scholar = authors[0]
	nbr_publications = len(scholar.publications)
	top_papers = []
	nbr_arxiv = 0
	nbr_first_authorships = 0
	print("DBLP entries: ", nbr_publications)
	counter = 0
	for p in scholar.publications:
	    print(p.title, " ", p.type, " ", p.journal)
	    # count SCI journals
	    if p.type == "article":
	    	if p.journal == "CoRR":
	    		nbr_arxiv += 1
	    		continue
	    	elif p.journal in sci_list:
	    		top_papers.append(p.title)
	    		print("added!")
	    co_authors = p.authors
	    # count first-authorships
	    if len(co_authors) > 0:
		    if co_authors[0] == affiliation_list[i]:
		    	nbr_first_authorships += 1   
	    counter += 1
	    if counter>=250:
	    	break
	
	nbr_publications -= nbr_arxiv
	seed_ratio = nbr_first_authorships / nbr_publications
	quality_ratio = len(top_papers) / nbr_publications

	result_string = affiliation_list[i] + " (" + str(nbr_publications) + " publ.) \t ### Seed ratio: " + str(seed_ratio) + " \t Quality ratio: " + str(quality_ratio) + "\n"
	print(result_string)

	f.write(result_string) 
	i += 1
	
f.close()

    