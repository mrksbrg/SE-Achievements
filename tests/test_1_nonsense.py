# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

import os.path
from datetime import date
from swesesci.scholar import SSSScholar
from swesesci.affiliation import SSSAffiliation
from swesesci.scholar_miner import ScholarMiner

class TestClass_NonSense:

    def setup_method(self):
        self.scholars = []
        self.affiliations = []
        subdirectory = "output"
        try:
            os.mkdir(subdirectory)
        except Exception:
            pass
        self.filename_prefix = os.path.join(subdirectory, str(date.today()) + "_sss_")
        self.test_nonsense = [("ABCDEFGH", "ijklmno", "A¿£$‰")]

    def add_sss_scholars(self, process_list, affiliation):
        for person in process_list:
            name = person[0]
            running_number = person[1]
            url = person[2]
            # extract the pid from the url by substringing
            try:
                split1 = url.split("pid/")
                split2 = split1[1].split(".xml")
                pid = split2[0]
            except IndexError:
                print("Invalid format of input XML URL.")
                return

            self.scholars.append(SSSScholar(name, running_number, pid, url, affiliation, -1))
            tmp_aff = SSSAffiliation(affiliation)
            if tmp_aff not in self.affiliations:
                tmp_aff.nbr_scholars += 1
                self.affiliations.append(tmp_aff)
            else:
                curr = next((x for x in self.affiliations if affiliation == x.name), None)
                curr.nbr_scholars += 1

    def test_nonsense(self):
        self.add_sss_scholars(self.test_nonsense, "N/A")
        self.miner = ScholarMiner(self.filename_prefix, self.scholars, self.affiliations)
        self.miner.parse_scholars()
        self.scholars = self.miner.get_scholars()

        # TC1: Test that DBLP does not return anything
        assert len(self.scholars) == 0
