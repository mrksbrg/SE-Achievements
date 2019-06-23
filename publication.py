class SEPublication:  
    
    sci_list = ["IEEE Trans. Software Eng.", "Empirical Software Engineering", "ACM Trans. Softw. Eng. Methodol.", "Autom. Softw. Eng.", "Information & Software Technology", "Requir. Eng.", " Software and System Modeling", "Software Quality Journal", "Journal of Systems and Software", "Journal of Software: Evolution and Process", "Softw. Test., Verif. Reliab.", "Softw., Pract. Exper.", "IET Software", "International Journal of Software Engineering and Knowledge Engineering"]

    conf_list = ["ICSE", "ASE", "FSE"]

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
        
    def __str__(self):
        return self.title + " (" + self.journal + ")"
        
    def __eq__ (self, other):
        return self.title == other.title
    
    def __hash__(self):
        return id(self)
    