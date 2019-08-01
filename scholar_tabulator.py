# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 11:21:15 2019

@author: Markus Borg
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape

class ScholarTabulator:
    def __init__(self, filename_prefix, swese_scholars):
        self.filename_prefix = filename_prefix
        self.swese_scholars = swese_scholars

    def write_tables(self):
        env = Environment(
            loader=FileSystemLoader("templates")
        )
        template = env.get_template('big_table.html')
        output = template.render(swese_scholars=self.swese_scholars)
        tmp = open(self.filename_prefix + "3_tabulator_big.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('details_table.html')
        output = template.render(swese_scholars=self.swese_scholars)
        tmp = open(self.filename_prefix + "3_tabulator_details.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('stats_table.html')
        output = template.render(swese_scholars=self.swese_scholars)
        tmp = open(self.filename_prefix + "3_tabulator_stats.html", "w+")
        tmp.write(output)
        tmp.close()


