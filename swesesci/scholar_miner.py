# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 21:18:26 2019

@author: Markus Borg
"""

import time
import pandas as pd
from collections import Counter
import requests
from lxml import etree
from collections import namedtuple
from .publication import SSSPublication

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
                    authors = search(scholar.name)
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
                            # Remove titles containing any of the substrings indicating editorial work
                            title_to_check = str(p.title).lower()
                            if title_to_check.find("special issue") >= 0 or title_to_check.find("special section") >= 0 or \
                               title_to_check.find("editorial") >= 0 or title_to_check.find("erratum") >= 0 or \
                               title_to_check.find("introduction to section") >= 0 or title_to_check.find("editor's introduction") >= 0:
                                print("Skipping editorial work: " + p.title)
                                continue

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
            print("Done! " + str(counter) + " scholars removed.")
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

DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
DBLP_AUTHOR_SEARCH_URL = DBLP_BASE_URL + 'search/author'

DBLP_PERSON_URL = DBLP_BASE_URL + 'pers/xk/{urlpt}'
DBLP_PUBLICATION_URL = DBLP_BASE_URL + 'rec/bibtex/{key}.xml'

class LazyAPIData(object):
    def __init__(self, lazy_attrs):
        self.lazy_attrs = set(lazy_attrs)
        self.data = None

    def __getattr__(self, key):
        if key in self.lazy_attrs:
            if self.data is None:
                self.load_data()
            return self.data[key]
        raise AttributeError("Error when getting attribute: " + key)

    def load_data(self):
        pass

class Author(LazyAPIData):
    """
    Represents a DBLP author. All data but the author's key is lazily loaded.
    Fields that aren't provided by the underlying XML are None.

    Attributes:
    name - the author's primary name record
    publications - a list of lazy-loaded Publications results by this author
    homepages - a list of author homepage URLs
    homonyms - a list of author aliases
    """
    def __init__(self, urlpt):
        self.urlpt = urlpt
        self.xml = None
        super(Author, self).__init__(['name','publications','homepages',
                                      'homonyms'])

    def load_data(self):
        resp = requests.get(DBLP_PERSON_URL.format(urlpt=self.urlpt))
        # TODO error handling
        xml = resp.content
        self.xml = xml
        root = etree.fromstring(xml)
        data = {
            'name':root.attrib['name'],
            'publications':[Publication(k) for k in
                            root.xpath('/dblpperson/dblpkey[not(@type)]/text()')],
            'homepages':root.xpath(
                '/dblpperson/dblpkey[@type="person record"]/text()'),
            'homonyms':root.xpath('/dblpperson/homonym/text()')
        }
        self.data = data

    def __str__(self):
        return self.name + " - " + self.urlpt

def first_or_none(seq):
    try:
        return next(iter(seq))
    except StopIteration:
        pass

Publisher = namedtuple('Publisher', ['name', 'href'])
Series = namedtuple('Series', ['text','href'])
Citation = namedtuple('Citation', ['reference','label'])

class Publication(LazyAPIData):
    """
    Represents a DBLP publication- eg, article, inproceedings, etc. All data but
    the key is lazily loaded. Fields that aren't provided by the underlying XML
    are None.

    Attributes:
    type - the publication type, eg "article", "inproceedings", "proceedings",
    "incollection", "book", "phdthesis", "mastersthessis"
    sub_type - further type information, if provided- eg, "encyclopedia entry",
    "informal publication", "survey"
    title - the title of the work
    authors - a list of author names
    journal - the journal the work was published in, if applicable
    volume - the volume, if applicable
    number - the number, if applicable
    chapter - the chapter, if this work is part of a book or otherwise
    applicable
    pages - the page numbers of the work, if applicable
    isbn - the ISBN for works that have them
    ee - an ee URL
    crossref - a crossrel relative URL
    publisher - the publisher, returned as a (name, href) named tuple
    citations - a list of (text, label) named tuples representing cited works
    series - a (text, href) named tuple describing the containing series, if
    applicable
    """
    def __init__(self, key):
        self.key = key
        self.xml = None
        super(Publication, self).__init__( ['type', 'sub_type', 'mdate',
                'authors', 'editors', 'title', 'year', 'month', 'journal',
                'volume', 'number', 'chapter', 'pages', 'ee', 'isbn', 'url',
                'booktitle', 'crossref', 'publisher', 'school', 'citations',
                'series'])

    def load_data(self):
        resp = requests.get(DBLP_PUBLICATION_URL.format(key=self.key))
        xml = resp.content
        self.xml = xml
        root = etree.fromstring(xml)
        publication = first_or_none(root.xpath('/dblp/*[1]'))
        if publication is None:
            raise ValueError
        data = {
            'type':publication.tag,
            'sub_type':publication.attrib.get('publtype', None),
            'mdate':publication.attrib.get('mdate', None),
            'authors':publication.xpath('author/text()'),
            'editors':publication.xpath('editor/text()'),
            'title':first_or_none(publication.xpath('title/text()')),
            'year':int(first_or_none(publication.xpath('year/text()'))),
            'month':first_or_none(publication.xpath('month/text()')),
            'journal':first_or_none(publication.xpath('journal/text()')),
            'volume':first_or_none(publication.xpath('volume/text()')),
            'number':first_or_none(publication.xpath('number/text()')),
            'chapter':first_or_none(publication.xpath('chapter/text()')),
            'pages':first_or_none(publication.xpath('pages/text()')),
            'ee':first_or_none(publication.xpath('ee/text()')),
            'isbn':first_or_none(publication.xpath('isbn/text()')),
            'url':first_or_none(publication.xpath('url/text()')),
            'booktitle':first_or_none(publication.xpath('booktitle/text()')),
            'crossref':first_or_none(publication.xpath('crossref/text()')),
            'publisher':first_or_none(publication.xpath('publisher/text()')),
            'school':first_or_none(publication.xpath('school/text()')),
            'citations':[Citation(c.text, c.attrib.get('label',None))
                         for c in publication.xpath('cite') if c.text != '...'],
            'series':first_or_none(Series(s.text, s.attrib.get('href', None))
                      for s in publication.xpath('series'))
        }

        self.data = data

def search(author_str):
    #if author_str == "Thomas Olsson":
    #    resp = requests.get("https://dblp.org/pid/31/5587-1.xml")
    #elif author_str == "Annabella Loconsole2":
    #    resp = requests.get("https://dblp.org/pid/69/4553.xml")
    #else:

    #req = requests.Request('GET', DBLP_AUTHOR_SEARCH_URL, params={'xauthor':author_str})
    #prepared = req.prepare()
    #pretty_print_POST(prepared)

    resp = requests.get(DBLP_AUTHOR_SEARCH_URL, params={'xauthor': author_str})

    #TODO error handling
    #try:
    root = etree.fromstring(resp.content)
    result = [Author(urlpt) for urlpt in root.xpath('/authors/author/@urlpt')]
    #print("Here is the result: " + str(result[0]))
    #except Exception as e:
    #   print(e)
    return result

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
