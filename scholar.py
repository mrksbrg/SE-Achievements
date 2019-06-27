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
        return self.name + " (" + str(len(self._publications)) + " publications. First-ratio: " + str(self._first_ratio) + " SCI-ratio: " + str(self._sci_ratio) + " Nbr firsts in SCI: " + str(self._nbr_first_sci) + ")"
        
    def __lt__(self, other):
        return self._first_ratio < other._first_ratio
    
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
            if publ.sci_listed:
                nbr += 1
        return nbr
    
    def get_nbr_main_confs(self):
        nbr = 0
        for publ in self._publications:
            if publ.major_conf:
                nbr += 1
        return nbr
    
    def get_first_author_titles(self):
        first_author_titles = []
        for p in self._publications:
            if (p.authors[0] == self.name):
                first_author_titles.append(p.title)
        return first_author_titles
        
    def sci_publications_to_string(self):
        result = ""
        for publ in self._publications:
            if publ.sci_listed and publ.authors[0] == self.name:
                result += "\t" + str(publ.year) + ": " + publ.title + " (" + str(publ.journal) + ")" + "\n"
        return result
 
    def calc_stats(self):
        nbr_first_author = 0
        nbr_sci_listed = 0
        self._nbr_first_sci = 0
        for publ in self._publications:
            try:
                if publ.sci_listed and publ.authors[0] == self.name:
                    nbr_first_author += 1
                    nbr_sci_listed += 1
                    self._nbr_first_sci += 1       
                elif publ.authors[0] == self.name:
                    nbr_first_author += 1
                elif publ.sci_listed:
                    nbr_sci_listed += 1
            except:
                print("No authors for the publication: " + publ.title)
                
        if self.get_nbr_publications() > 0:
            self._first_ratio = nbr_first_author/self.get_nbr_publications()
            self._sci_ratio = nbr_sci_listed/self.get_nbr_publications()
        print(self.to_string())

    def to_string(self):
        return self.name + " (" + str(len(self._publications)) + " publications. First-ratio: " + str(round(self._first_ratio, 2)) + " SCI-ratio: " + str(round(self._sci_ratio, 2)) + " Nbr firsts in SCI: " + str(self._nbr_first_sci) + " Nbr main confs: " + str(self.get_nbr_main_confs()) + ")"
    
    def to_csv_line(self):
        return self.name + ";" + str(self.dblp_entries) + ";" + str(len(self._publications)) + ";" + str(self._first_ratio) + ";" + str(self._sci_ratio) + ";" + str(self._nbr_first_sci) + ";" + str(self.get_nbr_main_confs())    