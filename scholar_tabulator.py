# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 11:21:15 2019

@author: Markus Borg
"""

import csv
from jinja2 import Environment, FileSystemLoader, select_autoescape



class ScholarTabulator:
    def __init__(self, filename_prefix, swese_scholars):
        self.filename_prefix = filename_prefix
        self.swese_scholars = swese_scholars

    def write_table(self):
        env = Environment(
            loader=FileSystemLoader("templates")
        )
        template = env.get_template('tables.html')
        output = template.render(swese_scholars=self.swese_scholars)
        tmp = open(self.filename_prefix + "3_tabulator.html", "w+")
        tmp.write(output)
        tmp.close()


