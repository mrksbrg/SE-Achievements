# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 21:18:26 2019

@author: Markus Borg
"""

from scholar import SEScholar
from publication import SEPublication
from datetime import date
from collections import Counter
import pandas as pd
import time
import dblp

sci_list = ["IEEE Trans. Software Eng.", "Empirical Software Engineering", "ACM Trans. Softw. Eng. Methodol.", "Autom. Softw. Eng.", "Information & Software Technology", "Requir. Eng.", " Software and System Modeling", "Software Quality Journal", "Journal of Systems and Software", "Journal of Software: Evolution and Process", "Softw. Test., Verif. Reliab.", "Softw., Pract. Exper.", "IET Software", "International Journal of Software Engineering and Knowledge Engineering"]

class ScholarMiner:
    
    def __init__(self):
        self.scholars = {}
        self.coauthors = Counter()
        self.titles = []
            
    def process_group(self, researchers):
        nbr_remaining = len(researchers)
        while nbr_remaining > 0: # an extra loop to tackle DBLP flakiness
            for scholar, processed in researchers.items():	
                if not processed: # only proceed if the scholar hasn't been processed already
                    try:
                        print("\n####### Processing scholar: " + scholar + " #######")
                        authors = dblp.search(scholar)
                        search_res = authors[0]
                    except:
                        print("ERROR: Invalid search result from DBLP. Waiting...")
                        time.sleep(5)
                        break
                                        
                    dblp_entries = len(search_res.publications)
                    print("DBLP entries: ", dblp_entries)          
                    current_scholar = SEScholar(scholar, dblp_entries)
                    self.scholars[scholar] = current_scholar
        				                    
        			# traverse publications
                    i = 0
                    for p in search_res.publications:
                        self.print_progress_bar(i + 1, dblp_entries)
                        try:
                            time.sleep(0.5) # There appears to be some race condition in the dblp package  					
                            if len(p.authors) == 0: #skip papers with 0 authors
                                    continue
                            elif p.type == "article":
                                if p.journal == "CoRR": #skip ArXiv preprints
                                    continue 
                            #elif p.type == "inproceedings": # This is what conference proceedings look like
                                #print(p.booktitle)
                            current_publication = SEPublication(p.title, p.journal, p.booktitle, p.year, p.authors)
                            current_scholar.add_publication(current_publication)
                            self.coauthors = self.coauthors + Counter(p.authors)
                            self.titles.append(p.title)
                            i += 1
                        except:
                            print("ERROR. Processing one of the papers failed. Waiting...")
                            time.sleep(5)
                            break
                                                
                    current_scholar.calc_stats()
                    processed = True
                    nbr_remaining -= 1
    
    # Print progress bar for scholar processing
    def print_progress_bar(self, iteration, total):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   : current iteration
            total       : total iterations
        """
        length = 50 # character length of bar (Int)
        decimals = 1 # number of decimals in percent complete
        fill = '█' # bar fill character (Str)
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % ("Progress:", bar, percent, "Complete "), end = '\r')
        # Print New Line on Complete
        if iteration == total: 
            print()
        
    def get_scholars(self):
        return self.scholars
    
    def write_scholars_txt(self):
        tmp = open(str(date.today()) + "_SCHOLARS.txt","w+")
        for key, value in self.scholars.items():
            tmp.write(value.to_string() + "\n")
            tmp.write(value.sci_publications_to_string())
        tmp.close()
        
    def write_scholars_csv(self):
        tmp = open(str(date.today()) + "_SCHOLARS.csv","w+")
        for key, value in self.scholars.items():
            tmp.write(value.to_csv_line() + "\n")
        tmp.close()
        
    def sort_and_print(self):
        print(sorted(self.scholars.items(), key = 
             lambda kv:(kv[1], kv[0])))
        
    def write_coauthors_csv(self):
        (pd.DataFrame.from_dict(data=self.coauthors, orient='index').to_csv('coauthors.csv', sep=';', header=False))
        