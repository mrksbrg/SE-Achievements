class SSSPublication:
    
    sci_list = ["IEEE Trans. Software Eng.", "Empirical Software Engineering", "ACM Trans. Softw. Eng. Methodol.", "Autom. Softw. Eng.", "Inf. Softw. Technol.", "Requir. Eng.", "Software and Systems Modeling", "Softw. Qual. J.", "J. Syst. Softw.", "J. Softw. Evol. Process.", "Journal of Software Maintenance", "J. Softw. Maintenance Res. Pract.", "Softw. Test. Verification Reliab.", "Softw. Pract. Exp.", "IET Software", "International Journal of Software Engineering and Knowledge Engineering"]
    conf_list = ["ICSE", "FSE"]
    ' SWEBOK Knowledge Areas '
    re_conf_list = ["RE", "REFSQ"]
    re_journal_list = ["Requir. Eng."]

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

        self.ka_re = False
        self.assign_knowledge_areas()

    def assign_knowledge_areas(self):
        if self.booktitle in self.re_conf_list:
            self.ka_re = True
        elif self.journal in self.re_journal_list:
            self.ka_re = True

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