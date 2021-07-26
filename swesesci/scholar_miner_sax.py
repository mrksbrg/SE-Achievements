# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 2021

@author: Markus Borg
"""

import time
import datetime
import xml.sax
import pandas as pd
from collections import Counter
from .publication import SSSPublication
from .scholar_sax import SSSScholar

class ScholarMiner(xml.sax.ContentHandler):

    def __init__(self, filename_prefix, input_sss_scholars, input_sss_affiliations):
        self.filename_prefix = filename_prefix
        self.input_sss_scholars = input_sss_scholars
        self.input_sss_affiliations = input_sss_affiliations

        # data structures containing the results
        self.sss_scholars = []

        # keep track of all coauthors as they might suggest missing SSS scholars
        self.global_SSS_coauthors = Counter()

        # some information to keep track of while parsing scholars
        self.current_scholar = None
        self.current_scholar_name = ""
        self.current_scholar_running_nbr = -1
        self.current_scholar_affiliation = ""
        self.current_scholar_url = ""

        # some information to keep track of while parsing publications
        self.parsing_publication = False
        #self.parsing_publication_authors = False
        self.tmp_author_pid = ""
        self.current_pub_title = -1
        self.current_pub_journal = -1
        self.current_pub_booktitle = -1
        self.current_pub_year = -1
        self.current_pub_authors = []
        self.current_pub_informal = False

    def parse_scholars(self):
        nbr_scholars = len(self.input_sss_scholars)
        i = 0 # for the progress bar
        print(str(nbr_scholars) + " scholars to parse from DBLP...")
        self.print_progress_bar(i, nbr_scholars)
        parser = xml.sax.make_parser()
        parser.setContentHandler(self)
        for scholar in self.input_sss_scholars:
            i = i + 1
            self.current_scholar_name = scholar.name
            self.current_scholar_running_nbr = scholar.running_number
            self.current_scholar_affiliation = scholar.affiliation
            self.current_scholar_url = scholar.url
            # SAX parse the URL
            parser.parse(scholar.url)
            self.print_progress_bar(i, nbr_scholars)

        # Calculating statistics and removing scholars with no first-authored SCI publications
        print("Calculating statistics...")
        tmp_scholars = []
        counter = 0
        for scholar in self.sss_scholars:
            scholar.calc_stats()
            if scholar.nbr_first_sci > 0:
                tmp_scholars.append(scholar)
            else:
                #curr = next((x for x in self.sss_affiliations if scholar.affiliation == x.name), None)
                #curr.nbr_scholars -= 1
                counter = counter + 1
                print("Removed scholar with no first-authored SCI publications: " + scholar.name)
        self.sss_scholars = tmp_scholars
        if counter > 0:
            print("Done! " + str(counter) + " scholars removed.")
        else:
            print("Done! No scholars were removed.")

    def clear_current_scholar(self):
        self.current_scholar = None

    def clear_current_pub(self):
        self.current_pub_title = -1
        self.current_pub_journal = -1
        self.current_pub_booktitle = -1
        self.current_pub_year = -1
        self.current_pub_authors = []
        self.current_pub_informal = False

    # Get a list of the last decade's titles
    def get_recent_titles(self):
        recent_publications = []
        now = datetime.datetime.now()
        for p in self.publications:
            if int(p.year) >= int(now.year) - 10:
                recent_publications.append(p)
        return recent_publications

    def write_results(self):
        print("Writing results to file")

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
        (pd.DataFrame.from_dict(data=self.global_SSS_coauthors, orient='index').to_csv(self.filename_prefix + "1_coauthors.csv", sep=';', header=False))

        # Write co-authors that are not already among the mined Swedish SE scholars
        diff = {}
        for coauthor in self.global_SSS_coauthors:
            for swese_scholar in self.sss_scholars:
                if coauthor != swese_scholar.name:
                    diff[coauthor] = self.global_SSS_coauthors[coauthor]

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
        return self.global_SSS_coauthors

    # SAX parsing

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        # Opening person
        if tag == "dblpperson":
            author_name = attributes["name"]
            author_id = attributes["pid"]
            dblp_entries = attributes["n"]
            self.current_scholar = SSSScholar(self.current_scholar_name, self.current_scholar_running_nbr, author_id, self.current_scholar_url, self.current_scholar_affiliation, dblp_entries)
            #print("Author Name (ID):", author_name + " (" + str(author_id) + "): " + str(dblp_entries) + " DBLP entries to parse.")
        # Opening journal paper
        elif tag == "article":
            self.parsing_publication = True
            self.clear_current_pub()
            # filter arXiv preprints
            attribute_list = attributes.getNames()
            if "publtype" in attribute_list and attributes["publtype"] == "informal":
                self.current_pub_informal = True  # skipping arXiv preprints
        # Opening conference/workshop paper
        elif tag == "inproceedings":
            self.parsing_publication = True
            self.clear_current_pub()
        # Opening co-author of a publication
        elif tag == "author" and self.parsing_publication:
            # store the author's PID until we end the element
            self.tmp_author_pid = attributes["pid"]

    def endElement(self, tag):
        # Closing person
        if tag == "dblpperson":
            self.sss_scholars.append(self.current_scholar)
        # Closing journal paper
        elif tag == "article" and not self.current_pub_informal:
            # Remove titles containing any of the substrings indicating editorial work
            real_article = True
            title_to_check = self.current_pub_title.lower()
            if title_to_check.find("special issue") >= 0 or title_to_check.find("special section") >= 0 or \
                    title_to_check.find("editorial") >= 0 or title_to_check.find("commentaries on") >= 0 or \
                    title_to_check.find("introduction to section") >= 0 or title_to_check.find(
                "editor's introduction") >= 0 or \
                    title_to_check.find("in this issue") >= 0 or title_to_check.find("foreword to the") >= 0 or \
                    title_to_check.find("erratum") >= 0 or title_to_check.find("corrigendum") >= 0 or \
                    title_to_check.find("correction to") >= 0 or \
                    title_to_check.find("open science initiative of the empirical software engineering journal") >= 0:
                #print("Skipping editorial work and corrections: " + self.current_pub_title)
                real_article = False

            # Remove titles published in ACM SIGSOFT Softw. Eng. Notes
            if self.current_pub_journal == "ACM SIGSOFT Softw. Eng. Notes":
                real_article = False

            if real_article:
                current_publication = SSSPublication(self.current_pub_title, self.current_pub_journal, self.current_pub_booktitle, self.current_pub_year, self.current_pub_authors)
                self.current_scholar.add_publication(current_publication)
            self.parsing_publication = False
        # Closing conference/workshop paper
        elif tag == "inproceedings":
            current_publication = SSSPublication(self.current_pub_title, self.current_pub_journal,
                                                 self.current_pub_booktitle, self.current_pub_year,
                                                 self.current_pub_authors)
            self.current_scholar.add_publication(current_publication)
            self.parsing_publication = False
        # Closing author
        elif tag == "author" and self.parsing_publication:
            self.current_pub_authors.append((self.author, self.tmp_author_pid))
        # Closing title
        elif tag == "title":
            self.current_pub_title = self.title
        # Closing journal
        elif tag == "journal":
            self.current_pub_journal = self.journal
        elif tag == "booktitle":
            self.current_pub_booktitle = self.booktitle
        # Closing year
        elif tag == "year":
            self.current_pub_year = self.year
        # Closing coauthor
        elif tag == "na":
            self.global_SSS_coauthors[self.na] += 1 # add/increment this author to the Counter
        self.CurrentData = ""

    # Overwrite the characters method to get the content of an XML element
    def characters(self, content):
        # remove any non-ASCII characters, e.g., set theory
        encoded_string = content.encode('ascii', 'ignore')
        clean_content = encoded_string.decode()
        if self.CurrentData == "author":
            self.author = clean_content
        elif self.CurrentData == "title":
            self.title = clean_content
        elif self.CurrentData == "journal":
            self.journal = clean_content
        elif self.CurrentData == "booktitle":
            self.booktitle = clean_content
        elif self.CurrentData == "year":
            self.year = clean_content
        elif self.CurrentData == "na":
            self.na = clean_content





    ### OLD

    def process_group(self):
        nbr_remaining = len(self.sss_scholars)
        attempts = 0
        while nbr_remaining > 0 and attempts < 10:  # an extra loop to tackle DBLP flakiness
            attempts += 1
            for scholar in self.sss_scholars:
                try:
                    print("\n### Processing scholar: " + scholar.name + " ###")
                    if scholar.running_number == -1:
                        authors = search(scholar.name, -1)
                        search_res = authors[0]
                    else:
                        print("running number author!")
                        authors = search(scholar.name, scholar.running_number)
                        search_res = authors[0]
                except:
                    print("ERROR: Invalid search result from DBLP. Waiting...")
                    self.clear_all_scholars()
                    time.sleep(5)
                    break

                #print("Here")
                #print(search_res)

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
                            # remove any non-ASCII characters, e.g., set theory
                            encoded_string = p.title.encode('ascii', 'ignore')
                            p.title = encoded_string.decode()

                            # Remove titles containing any of the substrings indicating editorial work
                            title_to_check = str(p.title).lower()

                            if title_to_check.find("special issue") >= 0 or title_to_check.find("special section") >= 0 or \
                               title_to_check.find("editorial") >= 0 or title_to_check.find("commentaries on") >= 0 or \
                               title_to_check.find("introduction to section") >= 0 or title_to_check.find("editor's introduction") >= 0 or \
                               title_to_check.find("in this issue") >= 0 or title_to_check.find("foreword to the") >= 0 or \
                               title_to_check.find("erratum") >= 0 or title_to_check.find("corrigendum") >= 0 or \
                               title_to_check.find("correction to") >= 0 or \
                               title_to_check.find("open science initiative of the empirical software engineering journal") >= 0:
                                print("Skipping editorial work and corrections: " + p.title)
                                continue

                            if p.journal == "CoRR":  # skip ArXiv preprints
                                continue
                            if p.journal == "ACM SIGSOFT Software Engineering Notes":  # skip SE Notes
                                continue
                        #elif p.type == "inproceedings": # This is what conference proceedings look like
                        #    encoded_string = p.title.encode('ascii', 'ignore')
                        #    p.title = encoded_string.decode()
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

        # Calculate all statistics and remove scholars with no first-authored SCI publications
        print("\nRemoving scholars that have no first-authored SCI publication...")
        tmp_scholars = []
        counter = 0
        for scholar in self.sss_scholars:
            scholar.calc_stats()
            if scholar.nbr_first_sci > 0:
                tmp_scholars.append(scholar)
            else:
                curr = next((x for x in self.sss_affiliations if scholar.affiliation == x.name), None)
                curr.nbr_scholars -= 1
                counter = counter + 1
                print("Removed scholar with no first-authored SCI publications: " + scholar.name)
        self.sss_scholars = tmp_scholars
        if counter > 0:
            print("Done! " + str(counter) + " scholars removed.")
        else:
            print("Done! No scholars were removed.")

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