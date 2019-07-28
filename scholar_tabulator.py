# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 11:21:15 2019

@author: Markus Borg
"""

import csv
from jinja2 import Environment, PackageLoader, select_autoescape



class ScholarTabulator:
    def __init__(self, filename_prefix, swese_scholars):
        self.filename_prefix = filename_prefix
        self.swese_scholars = swese_scholars

    def write_table(self):
        print("WRITE TABLE CALLED")
        env = Environment(
            loader=PackageLoader('swese', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('table.html')
        print("Time to call render!")
        output = template.render(swese_scholars=self.swese_scholars)
        tmp = open(self.filename_prefix + "3_tabulator.html", "w+")
        tmp.write(output)
        tmp.close()


