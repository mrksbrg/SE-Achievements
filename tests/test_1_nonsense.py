# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

from datetime import date
from swesesci.scholar import SSSScholar
from swesesci.affiliation import SSSAffiliation
from swesesci.scholar_miner import ScholarMiner

class TestClass_NonSense:

    def setup_method(self):
        self.scholars = []
        self.affiliations = []
        self.filename_prefix = str(date.today()) + "_swese_"
        self.test_nonsense = ["ABCDEFGH", "A¿£$‰"]

    def add_sss_scholars(self, process_list, affiliation):
        for name in process_list:
            words = name.split()
            # check if author has a running number
            if not words[len(words) - 1].isdigit():
                self.scholars.append(SSSScholar(name, -1, affiliation))
                tmp_aff = SSSAffiliation(affiliation)
                if tmp_aff not in self.affiliations:
                    tmp_aff.nbr_scholars += 1
                    self.affiliations.append(tmp_aff)
                else:
                    curr = next((x for x in self.affiliations if affiliation == x.name), None)
                    curr.nbr_scholars += 1
            else:
                # author has a running number
                tmp_scholar = SSSScholar(' '.join(map(str, words[0:len(words) - 1])), str(words[len(words) - 1]),
                                         affiliation)
                self.scholars.append(tmp_scholar)
                tmp_aff = SSSAffiliation(affiliation)
                if tmp_aff not in self.affiliations:
                    tmp_aff.nbr_scholars += 1
                    self.scholars.append(tmp_aff)
                else:
                    curr = next((x for x in self.affiliations if affiliation == x.name), None)
                    curr.nbr_scholars += 1

    def test_nonsense(self):
        self.add_sss_scholars(self.test_nonsense, "N/A")
        self.miner = ScholarMiner(self.filename_prefix, self.scholars, self.affiliations)
        self.miner.process_group()
        self.scholars = self.miner.get_scholars()

        # TC1: Test that DBLP does not return anything
        assert len(self.scholars) == 0
