# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 21:18:26 2019

@author: Markus Borg
"""

from scholar import SEScholar
from publication import SEPublication
from collections import Counter
import pandas as pd
import time
import dblp

class ScholarMiner:
    
    def __init__(self, scholars, filename_prefix):
        self.scholars = scholars
        self.coauthors = Counter()
        self.processed = []
        for i in scholars:
            self.processed.append(False)
        self.filename_prefix = filename_prefix
        
    def process_group(self):
        nbr_remaining = len(self.scholars)
        attempts = 0
        while nbr_remaining > 0 and attempts < 10: # an extra loop to tackle DBLP flakiness
            attempts += 1
            for scholar, processed in self.scholars.items():	
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
                            
                            # TODO: Store the search_res locally
                            i += 1
                        except:
                            print("ERROR. Processing one of the papers failed. Waiting...")
                            time.sleep(5)
                            break
                        
                    if dblp_entries > 0 and i<dblp_entries:
                        self.print_progress_bar(dblp_entries, dblp_entries)
                    current_scholar.calc_stats()
                    processed = True
                    nbr_remaining -= 1
                    
        if attempts >= 10:
            print("Failed to process scholars")
            
    def write_results(self):
        tmp = open(self.filename_prefix + "1_miner.txt","w+")
        for key, value in self.scholars.items():
            tmp.write(value.to_string() + "\n")
            tmp.write(value.sci_publications_to_string())
        tmp.close()
        
        tmp = open(self.filename_prefix + "1_miner.csv","w+")
        for key, value in self.scholars.items():
            tmp.write(value.to_csv_line() + "\n")
        tmp.close()
        
        # Write co-authors to csv-file
        (pd.DataFrame.from_dict(data=self.coauthors, orient='index').to_csv('coauthors.csv', sep=';', header=False))
        
        # Write co-authors that are not already among the mined Swedish scholars 
        diff = dict(self.scholars.items() ^ self.coauthors.items())
        (pd.DataFrame.from_dict(data=diff, orient='index').to_csv('candidates.csv', sep=';', header=False))
        
        self.write_author_titles()
        
    def write_author_titles(self):
        """ 
        Write all titles from all first authors to csv
        """
        authors_several_rows = open(self.filename_prefix + "_Authors_vs_titles.csv","w+")
        authors_one_row = open(self.filename_prefix + "_Authors_all_titles.csv","w+")
        
        for key, value in self.scholars.items():
            tmp = key + "; "
            for p in value.get_first_author_titles():
                authors_several_rows.write(key + ";" + p + "\n")
                tmp += p + " "
            authors_one_row.write(tmp + "\n")
        authors_several_rows.close()
        authors_one_row.close()    
        
    def get_scholars(self):
        return self.scholars
    
    def get_coauthors(self):
        return self.coauthors
        
    def sort_and_print(self):
        print(sorted(self.scholars.items(), key = 
             lambda kv:(kv[1], kv[0])))
    
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