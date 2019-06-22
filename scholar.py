from publication import SEPublication

class SEScholar:  
    def __init__(self, name, dblp_entries):
        self.name = name        
        self.dblp_entries = dblp_entries
        self._publications = set()
        self._first_ratio = -1
        self._sci_ratio = -1
        self._nbr_sci_listed = -1
        self._nbr_first_sci = -1
        
    def __str__(self):
        return self.name + " (" + str(len(self._publications)) + " publications)"
    
    def __repr__(self):
        return self.name + " (" + str(len(self._publications)) + " publications)"
        
    def add_publication(self, publ):
        if not isinstance(publ, SEPublication):
            raise TypeError("Error: do not add anything but instances of publication.SEPublication to the collection")
        self._nbr_first_sci = 0
        self._publications.add(publ)
        if publ.sci_listed:
            self._nbr_first_sci += 1
        
    def get_nbr_publications(self):
        return len(self._publications)
    
    def get_nbr_sci_publications(self):
        nbr = 0
        for publ in self._publications:
            if publ.sci_listed == True:
                nbr += 1
        return nbr
 
    def calc_stats(self):
        nbr_first_author = 0
        nbr_sci_listed = 0
        self._nbr_first_sci = 0
        for publ in self._publications:
            try:
                if publ.sci_listed == True and publ.authors[0] == self.name:
                    nbr_first_author += 1
                    nbr_sci_listed += 1
                    #self._nbr_first_sci += 1       
                elif publ.authors[0] == self.name:
                    nbr_first_author += 1
                elif publ.sci_listed:
                    nbr_sci_listed += 1
            except:
                print("No authors for the publication: " + publ.title)
                
        if self.get_nbr_publications() > 0:
            self._first_ratio = nbr_first_author/self.get_nbr_publications()
            print("Nbr first: " + str(nbr_first_author))
            print("Nbr sci: " + str(nbr_sci_listed) + " Tot number: " + str(self.get_nbr_publications()))
            self._sci_ratio = nbr_sci_listed/self.get_nbr_publications()
