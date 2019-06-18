from publication import SEPublication

class SEScholar:  
    def __init__(self, name):
        self.name = name        
        self.publications = set()
        
    def __str__(self):
        return self.name + " (" + str(len(self.publications)) + " publications)"
    
    def __repr__(self):
        return self.name + " (" + str(len(self.publications)) + " publications)"
        
    def add_publication(self, publ):
        if not isinstance(publ, SEPublication):
            raise TypeError("Error: do not add anything but instances of publication.SEPublication to the collection")
        self.publications.add(publ)
        
    def get_nbr_publications(self):
        return len(self.publications)
    
    def get_nbr_sci_publications(self):
        nbr = 0
        for publ in self.publications:
            if publ.sci_listed == True:
                nbr += 1
        return nbr
    