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
        self.sss_experts_design = []
        self.sss_experts_constr = []
        self.sss_experts_test = []
        self.sss_experts_maint = []
        self.sss_experts_cm = []
        self.sss_experts_mgmt = []
        self.sss_experts_process = []
        self.sss_experts_models = []
        self.sss_experts_quality = []
        self.sss_experts_practice = []
        self.sss_experts_economics = []
        self.sss_experts_comp = []
        self.sss_test = []
        self.assign_expertise()

    def assign_expertise(self):
        for scholar in self.sss_scholars:
            for knowl_area_id in range(len(scholar.swebok_badges)):
                if scholar.swebok_badges[knowl_area_id] >= 1:
                    self.add_to_expert_lists(scholar, knowl_area_id)
        # add all domain experts to common list
        self.sss_test.append(self.sss_experts_re)
        self.sss_test.append(self.sss_experts_design)

    def add_to_expert_lists(self, scholar, knowl_area_id):
        if scholar not in self.sss_experts:
            self.sss_experts.append(scholar)
        if knowl_area_id == 0:
            self.sss_experts_re.append(scholar)
        if knowl_area_id == 1:
            self.sss_experts_design.append(scholar)
        if knowl_area_id == 2:
            self.sss_experts_constr.append(scholar)
        if knowl_area_id == 3:
            self.sss_experts_test.append(scholar)
        if knowl_area_id == 4:
            self.sss_experts_maint.append(scholar)
        if knowl_area_id == 5:
            self.sss_experts_cm.append(scholar)
        if knowl_area_id == 6:
            self.sss_experts_mgmt.append(scholar)
        if knowl_area_id == 7:
            self.sss_experts_process.append(scholar)
        if knowl_area_id == 8:
            self.sss_experts_models.append(scholar)
        if knowl_area_id == 9:
            self.sss_experts_quality.append(scholar)
        if knowl_area_id == 10:
            self.sss_experts_practice.append(scholar)
        if knowl_area_id == 11:
            self.sss_experts_economics.append(scholar)
        if knowl_area_id == 12:
            self.sss_experts_comp.append(scholar)

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
        template = env.get_template('SWEBOK_table.html')
        output = template.render(sss_scholars=self.sss_experts)
        tmp = open(self.filename_prefix + "3_tabulator_swebok.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages_re.html')
        output = template.render(sss_scholars=self.sss_experts_re)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-re.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages_design.html')
        output = template.render(sss_scholars=self.sss_experts_design)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-design.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages_constr.html')
        output = template.render(sss_scholars=self.sss_experts_constr)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-constr.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages_test.html')
        output = template.render(sss_scholars=self.sss_experts_test)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-test.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages_maint.html')
        output = template.render(sss_scholars=self.sss_experts_maint)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-maint.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages_cm.html')
        output = template.render(sss_scholars=self.sss_experts_cm)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-cm.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages_mgmt.html')
        output = template.render(sss_scholars=self.sss_experts_mgmt)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-mgmt.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages_process.html')
        output = template.render(sss_scholars=self.sss_experts_process)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-process.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages_models.html')
        output = template.render(sss_scholars=self.sss_experts_models)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-models.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages_quality.html')
        output = template.render(sss_scholars=self.sss_experts_quality)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-quality.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages_practice.html')
        output = template.render(sss_scholars=self.sss_experts_practice)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-practice.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages_economics.html')
        output = template.render(sss_scholars=self.sss_experts_economics)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-economics.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages_comp.html')
        output = template.render(sss_scholars=self.sss_experts_comp)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-comp.html", "w+")
        tmp.write(output)
        tmp.close()

        template = env.get_template('yellow_pages_raw.html')
        output = template.render(sss_test=self.sss_test)
        tmp = open(self.filename_prefix + "3_tabulator_swebok-raw.html", "w+")
        tmp.write(output)
        tmp.close()