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
        self.sss_experts = []
        self.sss_experts_re = []
        self.assign_expertise()

    def assign_expertise(self):
        for s in self.sss_scholars:
            for i in range(len(s.knowl_area_badges)):
                print("Checking KA " + str(i))
                if s.knowl_area_badges[i] == 1:
                    print("BRONZE KA: " + str(i) + " " + str(s.knowl_area_badges[i]))
                    if s not in self.sss_experts:
                        self.sss_experts.append(s)
                elif s.knowl_area_badges[i] == 2:
                    print("SILVER KA: " + str(i) + " " + str(s.knowl_area_badges[i]))
                    if s not in self.sss_experts:
                        self.sss_experts.append(s)
                elif s.knowl_area_badges[i] == 3:
                    print("GOLD KA: " + str(i) + " " + str(s.knowl_area_badges[i]))
                    if s not in self.sss_experts:
                        self.sss_experts.append(s)

    def add_to_expert_list(self, scholar, knowl_area, level):
        if knowl_area == 1:
            self.sss_experts_re.append(scholar)

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

        template = env.get_template('affiliations_table.html')
        output = template.render(sss_affiliations=self.sss_affiliations)
        tmp = open(self.filename_prefix + "3_tabulator_affiliations.html", "w+")
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

        # SWEBOK Knowledge Areas
        template = env.get_template('yellow_pages.html')
        output = template.render(sss_scholars=self.sss_experts)
        tmp = open(self.filename_prefix + "3_tabulator_swebok.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages.html')
        output = template.render(sss_scholars=self.sss_experts)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-re.html", "w+")
        tmp.write(output)
        tmp.close()