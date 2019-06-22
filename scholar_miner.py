# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 21:18:26 2019

@author: Markus Borg
"""

from scholar import SEScholar
from publication import SEPublication
from datetime import date
import time
import dblp

sci_list = ["IEEE Trans. Software Eng.", "Empirical Software Engineering", "ACM Trans. Softw. Eng. Methodol.", "Autom. Softw. Eng.", "Information & Software Technology", "Requir. Eng.", " Software and System Modeling", "Software Quality Journal", "Journal of Systems and Software", "Journal of Software: Evolution and Process", "Softw. Test., Verif. Reliab.", "Softw., Pract. Exper.", "IET Software", "International Journal of Software Engineering and Knowledge Engineering"]

class ScholarMiner:
    
    def __init__(self):
        self.output_file = open(str(date.today()) + "_output.txt","w+")
        self.scholars = {}
            
    def process_group(self, researchers):
        nbr_remaining = len(researchers)
        while nbr_remaining > 0:
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
                                        
        			# initiate variables
                    dblp_entries = len(search_res.publications)
                    print("DBLP entries: ", dblp_entries)
                    top_papers = []
                    nbr_arxiv = 0
                    nbr_first_authorships = 0
                    nbr_first_top = 0
                    total_text = ""
                    
                    current_scholar = SEScholar(scholar, dblp_entries)
                    self.scholars[scholar] = current_scholar
        				
                    #self.print_progress_bar(0, dblp_entries)
                    
        			# traverse publications
                    i = 0
                    for p in search_res.publications:
                        self.print_progress_bar(i + 1, dblp_entries)
                        try:
                            time.sleep(0.5) # There appears to be some race condition in the dblp package	
                            #print(p.title, " ", p.type, " ", p.journal)
                            co_authors = p.authors
        					# count SCI journals and how many as first author
                            if p.type == "article":
                                if p.journal == "CoRR": #skip ArXiv preprints
                                    nbr_arxiv += 1
                                    continue
                                elif len(co_authors) == 0:
                                    print ("Skipping one paper: " + p.title)
                                    continue
                                elif p.journal in sci_list:
                                    #sci_journal = True
                                    top_papers.append(p.title)
                                    if (co_authors[0] == scholar):
                                        nbr_first_top += 1
                                        total_text += "-" + p.title + "\n"                                                                       
                                if len(co_authors) > 0:
                                    if co_authors[0] == scholar:
                                        nbr_first_authorships += 1
        						#temp.publications.add(Publication(p.title, p.journal, sci_journal, len(co_authors))
        					    #print(co_authors) # used to find authors with a number, e.g., "Thomas Olsson 0001".
                            current_publication = SEPublication(p.title, p.journal, p.authors, False)
                            current_scholar.add_publication(current_publication)
                            i += 1
                        except:
                            print("ERROR. Processing one of the papers failed. Waiting...")
                            time.sleep(5)
                            break
                        
                    dblp_entries -= nbr_arxiv
                    if dblp_entries > 0:
                        seed_ratio = nbr_first_authorships / dblp_entries
                        quality_ratio = len(top_papers) / dblp_entries
                    else:
                        seed_ratio = "N/A"
                        quality_ratio = "N/A"
                        
                    current_scholar.calc_stats()
                    result_string = scholar + " (" + str(dblp_entries) + " publ., First-in-top: " + str(nbr_first_top) + ") \t\t ### Self-made ratio: " + str(seed_ratio) + " \t Quality ratio: " + str(quality_ratio) + "\n"
                    result_string += total_text
                    processed = True
                    print("Scholar processed: " + scholar)
                    nbr_remaining -= 1
                    self.output_file.write(result_string)
            
        self.output_file.close()
    
    # Print iterations progress
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
        print('\r%s |%s| %s%% %s' % ("Progress:", bar, percent, "Complete"), end = '\r')
        # Print New Line on Complete
        if iteration == total: 
            print()
        
    def get_scholars(self):
        return self.scholars
    
    def print_scholars(self):
        tmp = open(str(date.today()) + "_ATTEMPT.txt","w+")
        for scholar in self.scholars.items():
            tmp.write(str(scholar) + "\n")
        tmp.close()