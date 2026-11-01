# -*- coding: utf-8 -*-
"""
Created on Sun Nov 1 2026

@author: Markus Borg
"""

from swesesci.scholar_miner import ScholarMiner


class TestClass_EditorialWork:

    def test_editorial_titles(self):
        # TC1: Prefaces, keynotes, and editorials are not papers, whatever the case
        assert ScholarMiner.is_editorial_work("Preface: REFSQ 2020 Posters and Tools Track.")
        assert ScholarMiner.is_editorial_work("Preface.")
        assert ScholarMiner.is_editorial_work("Keynote: Making program analysis useful.")
        assert ScholarMiner.is_editorial_work("Runtime goal models: Keynote.")
        assert ScholarMiner.is_editorial_work("Editorial: In This Issue")

    def test_papers(self):
        # TC2: Ordinary paper titles are kept
        assert not ScholarMiner.is_editorial_work("In Vivo Evaluation of Large-Scale IR-Based Traceability Recovery.")
        assert not ScholarMiner.is_editorial_work("Ergo, SMIRK is safe: a safety case for a machine learning component.")
