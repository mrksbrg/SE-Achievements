class Publication:  
    def __init__(self, title, journal, sci, nbr_authors):
        self.title = title        
        self.journal = journal
        self.sci = sci
        self.nbr_authors = nbr_authors
        
    def __str__(self):
        return self.title + " (" + self.journal + ")"
        
    def __eq__ (self, other):
        return self.title == other.title and self.journal == other.journal
    
    def get_one():
        return 1