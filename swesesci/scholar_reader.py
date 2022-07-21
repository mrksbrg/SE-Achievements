# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 2022

@author: Markus Borg
"""

import csv
import os.path
from datetime import date
from collections import Counter
from .publication import SSSPublication
from .scholar import SSSScholar
from .affiliation import SSSAffiliation

def string_splitter(scholar_string):
    affiliation = scholar_string[0]
    name = scholar_string[1]
    running_number = scholar_string[2]
    url = scholar_string[3]

    try:
        split1 = url.split("pid/")
        split2 = split1[1].split(".xml")
        pid = split2[0]
    except IndexError:
        print("Invalid format of input XML URL. (" + name + ")")
        return

    return affiliation, name, running_number, pid, url

def get_affiliation_list(scholars, affiliations):
    for scholar in scholars:
        tmp_aff = SSSAffiliation(scholar.affiliation)
        existing_aff = [x for x in affiliations if scholar.affiliation == x.name]

        if len(existing_aff) == 0:
            tmp_aff.nbr_scholars += 1
            affiliations.append(tmp_aff)
        else:
            existing_aff[0].nbr_scholars += 1

    return affiliations

class ScholarReader():

    def __init__(self, csv_filename):
        self.csv_filename = csv_filename

    def read_candidate_scholars(self):
        with open(self.csv_filename, newline="", encoding="utf-8") as f:
            print("Reading file: " + self.csv_filename)
            reader = csv.reader(f)
            candidate_scholars = list(reader)

        sss_scholars = []
        sss_affiliations = []

        scholar_list = list(map(string_splitter, candidate_scholars))
        [sss_scholars.append(SSSScholar(x[1], x[2], x[3], x[4], x[0], -1)) for x in scholar_list]
        sss_affiliations = get_affiliation_list(sss_scholars, sss_affiliations)

        return sss_scholars, sss_affiliations