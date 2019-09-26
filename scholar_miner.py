# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 21:18:26 2019

@author: Markus Borg
"""

from publication import SSSPublication
from collections import Counter
import pandas as pd
import time
import dblp

class ScholarMiner:
    
    def __init__(self, filename_prefix, sss_scholars, sss_affiliations):
        self.filename_prefix = filename_prefix
        self.sss_scholars = sss_scholars
        self.sss_affiliations = sss_affiliations
        self.coauthors = Counter()

    def process_group(self):
        nbr_remaining = len(self.sss_scholars)
        attempts = 0
        while nbr_remaining > 0 and attempts < 10: # an extra loop to tackle DBLP flakiness
            attempts += 1
            for scholar in self.sss_scholars:
                try:
                    print("\n### Processing scholar: " + scholar.name + " ###")
                    authors = dblp.search(scholar.name)
                    search_res = authors[0]
                except:
                    print("ERROR: Invalid search result from DBLP. Waiting...")
                    self.clear_all_scholars()
                    time.sleep(5)
                    break

                dblp_entries = len(search_res.publications)
                print("DBLP entries: ", dblp_entries)
                scholar.dblp_entries = dblp_entries

                # traverse publications
                i = 0
                for p in search_res.publications:
                    self.print_progress_bar(i + 1, dblp_entries)
                    try:
                        time.sleep(0.5)  # There appears to be some race condition in the dblp package
                        if len(p.authors) == 0:  # skip papers with 0 authors
                            continue
                        elif p.type == "article":
                            # todo: remove titles with "special issue, special section, editorial, and erratum"
                            if p.journal == "CoRR":  # skip ArXiv preprints
                                continue
                                # elif p.type == "inproceedings": # This is what conference proceedings look like
                            # print(p.booktitle)
                        current_publication = SSSPublication(p.title, p.journal, p.booktitle, p.year, p.authors)
                        scholar.add_publication(current_publication)
                        self.coauthors = self.coauthors + Counter(p.authors)

                        # TODO: Cache the search_res locally
                        i += 1
                    except Exception as e:
                        print(e)
                        print("ERROR. Processing one of the papers failed. Waiting...")
                        time.sleep(5)
                        break

                if dblp_entries > 0 and i < dblp_entries:
                    self.print_progress_bar(dblp_entries, dblp_entries)
                scholar.calc_stats()
                nbr_remaining -= 1
                    
        if attempts >= 10:
            print("Failed to process scholars")

        # Remove scholars with no first-authored SCI publications
        print("\nRemoving scholars that have no first-authored SCI publication...")
        tmp_scholars = []
        counter = 0
        for scholar in self.sss_scholars:
            if scholar.nbr_first_sci > 0:
                tmp_scholars.append(scholar)
            else:
                curr = next((x for x in self.sss_affiliations if scholar.affiliation == x.name), None)
                curr.nbr_scholars -= 1
                counter = counter + 1
                print("Removed scholar with no first-authored SCI publications: " + scholar.name)
        self.sss_scholars = tmp_scholars
        if counter > 0:
            print("Done! " + counter + " scholars removed.")
        else:
            print("Done! No scholars were removed.")

    def clear_all_scholars(self):
        for scholar in self.sss_scholars:
            scholar.clear()

    def write_results(self):
        tmp = open(self.filename_prefix + "1_miner.txt","w+")
        for scholar in self.sss_scholars:
            tmp.write(scholar.name + "\n")
            tmp.write(scholar.sci_publications_to_string())
        tmp.close()
        
        tmp = open(self.filename_prefix + "1_miner.csv","w+")
        for scholar in self.sss_scholars:
            tmp.write(scholar.to_csv_line() + "\n")
        tmp.close()
        
        # Write concatenated titles per author and affiliation
        self.write_author_and_affiliation_titles()
        
        # Write co-authors to csv-file
        (pd.DataFrame.from_dict(data=self.coauthors, orient='index').to_csv(self.filename_prefix + "1_coauthors.csv", sep=';', header=False))
        
        # Write co-authors that are not already among the mined Swedish SE scholars
        diff = {}
        for coauthor in self.coauthors:
            for swese_scholar in self.sss_scholars:
                if coauthor != swese_scholar.name:
                    diff[coauthor] = self.coauthors[coauthor]

        (pd.DataFrame.from_dict(data=diff, orient='index').to_csv(self.filename_prefix + "1_candidates.csv", sep=';', header=False))

    def write_author_and_affiliation_titles(self):
        """ 
        Write all titles from all first authors to csv
        """

        titles_per_author = open(self.filename_prefix + "1_titles_per_author.csv", "w+")
        titles_per_affiliation = open(self.filename_prefix + "1_titles_per_affiliation.csv", "w+")
        affiliation_titles = self.get_dict_of_affiliations()

        for scholar in self.sss_scholars:
            tmp = scholar.name + "; "
            for p in scholar.get_first_author_titles():
                affiliation_titles[scholar.affiliation] += p + " "
                tmp += p + " "
                titles_per_author.write(tmp + "\n")

        for affiliation, titles in affiliation_titles.items():
            titles_per_affiliation.write(affiliation + ";" + titles + "\n")
        titles_per_author.close()
        titles_per_affiliation.close()

    def get_scholars(self):
        return self.sss_scholars
    
    def get_coauthors(self):
        return self.coauthors
    
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
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print('\r%s |%s| %s%% %s' % ("Progress:", bar, percent, "Complete "), end = '\r')
        # Print New Line on Complete
        if iteration == total: 
            print()

    def get_dict_of_affiliations(self):
        ''' Return a dict with affiliations as keys. All values are empty strings. '''
        affiliations = {}
        for scholar in self.sss_scholars:
            if scholar.affiliation not in affiliations:
                affiliations[scholar.affiliation] = ""
        return affiliations
