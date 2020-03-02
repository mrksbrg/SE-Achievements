class SSSPublication:
    
    sci_list = ["IEEE Trans. Software Eng.", "Empirical Software Engineering", "ACM Trans. Softw. Eng. Methodol.", "Autom. Softw. Eng.", "Inf. Softw. Technol.", "Requir. Eng.", "Software and System Modeling", "Software Quality Journal", "J. Syst. Softw.", "Journal of Software: Evolution and Process", "Journal of Software Maintenance", "Softw. Test., Verif. Reliab.", "Softw., Pract. Exper.", "IET Software", "International Journal of Software Engineering and Knowledge Engineering"]
    conf_list = ["ICSE", "FSE"]

    def __init__(self, title, journal, booktitle, year, authors):
        self.title = self.ensure_ascii(title)
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

    def ensure_ascii(self, string_to_check):
        """
        Replace any non-ASCII character with a whitespace (' ')
        """
        cleaned_string = str(string_to_check)
        try:
            string_to_check.encode('ascii')
            cleaned_string = str(string_to_check)
        except Exception:
            print("Non-ASCII characters in the title: " + string_to_check)
            for i in string_to_check:
                try:
                    i.encode('ascii')
                except Exception:
                    print("Non-ASCII character: " + i)
                    cleaned_string = cleaned_string.replace(i, ' ')
        return cleaned_string

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