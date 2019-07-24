# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 11:21:15 2019

@author: Markus Borg
"""

import csv
from jinja2 import Environment, FileSystemLoader


class ScholarTabulator:
    def __init__(self, scholars):
        self.scholars = scholars

    def write_table(self):

        loader = FileSystemLoader('./index.html')
        env = Environment(loader=loader)
        #template = env.get_template('')
        #print(template.render(date='2012-02-8', id='123', position='here', status='Waiting'))
