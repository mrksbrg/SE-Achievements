# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

import pytest
import os.path
import csv
from datetime import date
from swesesci.scholar import SSSScholar
from swesesci.affiliation import SSSAffiliation
from swesesci.scholar_miner import ScholarMiner

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
        raise IndexError

    return affiliation, name, running_number, pid, url

class TestClass_NonSense:

    def setup_method(self):
        self.sss_scholars = []
        self.sss_affiliations = []
        subdirectory = "output"
        try:
            os.mkdir(subdirectory)
        except Exception:
            pass
        self.filename_prefix = os.path.join(subdirectory, str(date.today()) + "_sss_")

    def get_affiliation_list(scholars):
        tmp_list = []
        for scholar in scholars:
            tmp_aff = SSSAffiliation(scholar.affiliation)
            existing_aff = tmp_aff in self.sss_affiliations

            if existing_aff is False:
                tmp_aff.nbr_scholars += 1
                tmp_list.append(tmp_aff)
            else:
                existing_aff.nbr_scholars += 1

        return tmp_list

    def test_nonsense(self):
        with open('test/test_1_nonsense.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            candidate_scholars = list(reader)

        # TC1: Test that an exception is raised due to incorrect formatting
        with pytest.raises(IndexError):
            list(map(string_splitter, candidate_scholars))
