class SSSPublication:
    
    sci_list = ["IEEE Trans. Software Eng.", "Empir. Softw. Eng.", "ACM Trans. Softw. Eng. Methodol.",
                "Autom. Softw. Eng.", "Inf. Softw. Technol.", "Requir. Eng.", "Softw. Syst. Model.",
                "Softw. Qual. J.", "J. Syst. Softw.", "J. Softw. Evol. Process.", "Softw. Process. Improv. Pract.",
                "Journal of Software Maintenance", "J. Softw. Maintenance Res. Pract.", "Softw. Test. Verification Reliab.",
                "Softw. Pract. Exp.", "IET Software", "Int. J. Softw. Eng. Knowl. Eng."]

    # SWEBOK Knowledge Areas
    # -1 = Unclear
    # 0 = Software Requirements
    re_conf_list = ["RE", "REFSQ"]
    re_journal_list = ["Requir. Eng."]
    # 1 = Software Design
    design_conf_list = ["ICSA", "ECSA", "WICSA", "UIST", "IUI"]
    design_journal_list = ["J. Syst. Archit."]
    # 2 = Software Construction
    constr_conf_list = ["OOPSLA", "ECOOP", "SCAM", "Programming", "Middleware"]
    constr_journal_list = ["Sci. Comput. Program.", "Programming and Computer Software"]
    # 3 = Software Testing
    test_conf_list = ["ICST", "ISSTA"]
    test_journal_list = ["Softw. Test. Verification Reliab."]
    # 4 = Software Maintenance
    maint_conf_list = ["ICSM", "ICSME", "CSMR", "CSMR-WCRE", "WCRE"]
    maint_journal_list = ["J. Softw. Maintenance Res. Pract."]
    # 5 = Software Configuration Management
    cm_conf_list = ["SCM", "SPLC"]
    # 6 = Software Engineering Management
    mgmt_conf_list = ["METRICS", "IWSM/Mensura", "IWSM-Mensura"]
    mgmt_journal_list = ["MIS Quarterly"]
    # 7 = Software Engineering Process
    process_conf_list = ["ICSSP", "XP", "PROFES", "SPICE"]
    process_journal_list = ["J. Softw. Evol. Process.", "Softw. Process. Improv. Pract."]
    # 8 = Software Engineering Models and Methods
    models_conf_list = ["MoDELS", "ER", "FormaliSE", "ISoLA"]
    models_journal_list = ["Software and Systems Modeling"]
    # 9 = Software Quality
    quality_conf_list = ["QRS", "SAFECOMP", "ISSRE", "ARES", "HASE", "ICPE"]
    quality_journal_list = ["Softw. Qual. J.", "IEEE Trans. Reliab."]
    # 10 = Software Engineering Professional Practice
    practice_conf_list = ["ICSE-SEIP", "ICSE-SEIS"]
    practice_journal_list = ["IEEE Softw.", "Softw. Pract. Exp."]
    # 11 = Software Engineering Economics
    economics_conf_list = ["ICSOB", "ICGSE"]
    # 12 = Computing Foundations
    comp_conf_list = ["FASE", "PLDI", "POPL", "IPDPS", "PODC", "SLE"]
    comp_journal_list = ["Formal Asp. Comput.", "Formal Methods Syst. Des"]
    # 13 = Mathematical Foundations
    maths_conf_list = ["SODA", "ITCS", "ESA", "STACS", "ISAAC", "FSTTCS" ]
    maths_journal_list = ["ACM Trans. Algorithms", "Algorithmica"]
    # 14 = Engineering Foundations
    eng_conf_list = ["TBD"]

    # BONUS Categories
    # 15 = ICSE
    flagship_list = ["ICSE"]
    # 16 = Prestigious general conferences
    prestigious_list = ["FSE", "ASE"]
    # 17 = Empiricism
    emp_conf_list = ["ESEM", "EASE"]
    emp_journal_list = ["Empirical Software Engineering"]
    # 18 = Information Systems
    is_conf_list = ["CaiSE", "ICEIS", "HICCS"]
    # 19 = Human Computer Interaction
    hci_conf_list = ["CHI", "INTERACT"]
    # 20 = High Assurance
    assure_conf_list = ["SAFECOMP", "ISSRE", "ARES", "HASE"]
    assure_journal_list = ["IEEE Trans. Reliab.", "IEEE Trans. Dependable Secur. Comput."]
    # 21 = Web Tech
    web_conf_list = ["IEEE ICWS", "SCC", "ICSOC", "ICWE", "WISE", "SOCA"]
    web_journal_list = ["Int. J. Web Serv. Res.", "J. Web Eng.", "IEEE Trans. Network and Service Management"]

    def __init__(self, title, journal, booktitle, year, authors):
        self.title = title
        self.journal = journal
        self.major_conf = False
        self.booktitle = booktitle
        if self.booktitle in self.flagship_list:
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
        elif self.journal in self.design_journal_list:
            self.knowl_area = 1
        # 2 = Construction
        elif self.booktitle in self.constr_conf_list:
            self.knowl_area = 2
        elif self.journal in self.design_journal_list:
            self.knowl_area = 2
        # 3 = Test
        elif self.booktitle in self.test_conf_list:
            self.knowl_area = 3
        elif self.journal in self.test_journal_list:
            self.knowl_area = 3
        # 4 = Maintenance
        elif self.booktitle in self.maint_conf_list:
            self.knowl_area = 4
        elif self.journal in self.maint_journal_list:
            self.knowl_area = 4
        # 5 = Configuration Management
        elif self.booktitle in self.cm_conf_list:
            self.knowl_area = 5
        # 6 = Management
        elif self.booktitle in self.mgmt_conf_list:
            self.knowl_area = 6
        elif self.journal in self.mgmt_journal_list:
            self.knowl_area = 6
        # 7 = Process
        elif self.booktitle in self.process_conf_list:
            self.knowl_area = 7
        elif self.journal in self.process_journal_list:
            self.knowl_area = 7
        # 8 = Models and Methods
        elif self.booktitle in self.models_conf_list:
            self.knowl_area = 8
        elif self.journal in self.models_journal_list:
            self.knowl_area = 8
        # 9 = Quality
        elif self.booktitle in self.quality_conf_list:
            self.knowl_area = 9
        elif self.journal in self.quality_journal_list:
            self.knowl_area = 9
        # 10 = Professional Practice
        elif self.booktitle in self.practice_conf_list:
            self.knowl_area = 10
        elif self.journal in self.practice_journal_list:
            self.knowl_area = 10
        # 11 = Economics
        elif self.booktitle in self.economics_conf_list:
            self.knowl_area = 11
        # 12 = Computing Foundations
        elif self.booktitle in self.comp_conf_list:
            self.knowl_area = 12
        elif self.journal in self.comp_journal_list:
            self.knowl_area = 12
        # 13 = Mathematical Foundations
        elif self.booktitle in self.maths_conf_list:
            self.knowl_area = 13
        elif self.journal in self.maths_journal_list:
            self.knowl_area = 13
        # 14 = Engineering Foundations
        elif self.booktitle in self.eng_conf_list:
            self.knowl_area = 14

        # 15 = ICSE
        elif self.booktitle in self.flagship_list:
            self.knowl_area = 15
        # 16 = Prestigious General Conferences
        elif self.booktitle in self.prestigious_list:
            self.knowl_area = 16
        # 17 = Empiricism
        elif self.booktitle in self.emp_conf_list:
            self.knowl_area = 17
        elif self.journal in self.emp_journal_list:
            self.knowl_area = 17
        # 18 = Information systems
        elif self.booktitle in self.is_conf_list:
            self.knowl_area = 18
        # 19 = Human-Computer Interaction
        elif self.booktitle in self.hci_conf_list:
            self.knowl_area = 19
        # 20 = High Assurance
        elif self.booktitle in self.assure_conf_list:
            self.knowl_area = 20
        elif self.journal in self.assure_journal_list:
            self.knowl_area = 20
        # 21 = Web
        elif self.booktitle in self.web_conf_list:
            self.knowl_area = 21
        elif self.journal in self.web_journal_list:
            self.knowl_area = 21

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