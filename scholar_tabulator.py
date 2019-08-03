# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 11:21:15 2019

@author: Markus Borg
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape

class ScholarTabulator:
    def __init__(self, filename_prefix, sss_scholars, sss_affiliations):
        self.filename_prefix = filename_prefix
        self.sss_scholars = sss_scholars
        self.sss_affiliations = sss_affiliations

    def write_tables(self):
        env = Environment(
            loader=FileSystemLoader("templates")
        )

        template = env.get_template('Swe-SE-SCI.html')
        output = template.render(sss_scholars=self.sss_scholars, sss_affiliations=self.sss_affiliations)
        tmp = open(self.filename_prefix + "3_tabulator_Swe-SE-SCI.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('raw_tables.html')
        output = template.render(sss_scholars=self.sss_scholars, sss_affiliations=self.sss_affiliations)
        tmp = open(self.filename_prefix + "3_tabulator_raw.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('topics_table.html')
        output = template.render(sss_affiliations=self.sss_affiliations)
        tmp = open(self.filename_prefix + "3_tabulator_topics.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('scholars_table.html')
        output = template.render(sss_scholars=self.sss_scholars)
        tmp = open(self.filename_prefix + "3_tabulator_scholars.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('works_table.html')
        output = template.render(sss_scholars=self.sss_scholars)
        tmp = open(self.filename_prefix + "3_tabulator_works.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('stats_table.html')
        output = template.render(sss_scholars=self.sss_scholars)
        tmp = open(self.filename_prefix + "3_tabulator_stats.html", "w+")
        tmp.write(output)
        tmp.close()


