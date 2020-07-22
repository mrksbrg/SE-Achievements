class SSSPublication:
    
    sci_list = ["IEEE Trans. Software Eng.", "Empirical Software Engineering", "ACM Trans. Softw. Eng. Methodol.", "Autom. Softw. Eng.", "Inf. Softw. Technol.", "Requir. Eng.", "Software and Systems Modeling", "Softw. Qual. J.", "J. Syst. Softw.", "J. Softw. Evol. Process.", "Journal of Software Maintenance", "J. Softw. Maintenance Res. Pract.", "Softw. Test. Verification Reliab.", "Softw. Pract. Exp.", "IET Software", "International Journal of Software Engineering and Knowledge Engineering"]
    conf_list = ["ICSE", "FSE"]

    # SWEBOK Knowledge Areas, represented by integer in the self.ka variable
    # -1 = Unclear
    # 0 = Software Requirements
    re_conf_list = ["RE", "REFSQ"]
    re_journal_list = ["Requir. Eng."]
    # 1 = Software Design
    design_conf_list = ["ICSA", "ECSA", "WICSA"]
    # 2 = Software Construction
    constr_conf_list = ["TBD"]
    # 3 = Software Testing
    test_conf_list = ["ICST", "ISSTA"]
    # 4 = Software Maintenance
    maint_conf_list = ["ICSME"]
    # 5 = Software Configuration Management
    cm_conf_list = ["TBD"]
    # 6 = Software Engineering Management
    mgmt_conf_list = ["ESEM", "EASE"]
    # 7 = Software Engineering Process
    process_conf_list = ["ICSSP"]
    # 8 = Software Engineering Models and Methods
    models_conf_list = ["MODELS"]
    # 9 = Software Quality
    quality_conf_list = ["TBD"]
    # 10 = Software Engineering Professional Practice
    practice_conf_list = ["TBD"]
    # 11 = Software Engineering Economics
    economics_conf_list = ["ICSOB"]
    # 12 = Computing Foundations
    comp_conf_list = ["TBD"]
    # 13 = Mathematical Foundations
    maths_conf_list = ["TBD"]
    # 14 = Engineering Foundations
    eng_conf_list = ["TBD"]


    def __init__(self, title, journal, booktitle, year, authors):
        self.title = title
        self.journal = journal
        self.major_conf = False
        self.booktitle = booktitle
        if self.booktitle in self.conf_list:
            self.major_conf = True
        
        self.year = year
        self.authors = authors
        self.sci_listed = False
        if self.journal in self.sci_list:
            self.sci_listed = True

        self.knowl_area = -1
        self.assign_knowledge_areas()

    def assign_knowledge_areas(self):
        # 0 = Requirements Engineering
        if self.booktitle in self.re_conf_list:
            self.knowl_area = 0
        elif self.journal in self.re_journal_list:
            self.knowl_area = 0
        # 1 = Design
        elif self.booktitle in self.design_conf_list:
            self.knowl_area = 1
        # 2 = Construction
        elif self.booktitle in self.constr_conf_list:
            self.knowl_area = 2
        # 1 = Design
        elif self.booktitle in self.test_conf_list:
            self.knowl_area = 3

    def __str__(self):
        if not self.journal is None:
            return self.title + " (" + self.journal + ")"
        else:
            return self.title
        
    def __eq__ (self, other):
        return self.title == other.title

    def __lt__(self, other):
        return self.year > other.year
    
    def __hash__(self):
        return id(self)