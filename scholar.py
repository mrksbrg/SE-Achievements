from publication import SEPublication

class SWESEScholar:
    def __init__(self, name, affiliation):
        self.name = name
        self.affiliation = affiliation
        self.research_interests = []

        self.dblp_entries = -1
        self.publications = set()
        self.first_ratio = -1
        self.sci_ratio = -1
        self.nbr_sci_listed = -1
        self.nbr_first_sci = -1
                
    def __str__(self):
        return self.name + " (" + str(len(self.publications)) + " publications)"
    
    def __repr__(self):
        return self.name + " (" + str(len(self.publications)) + " publications. First-ratio: " + str(self.first_ratio)\
               + "SCI-ratio: " + str(self.sci_ratio) + " Nbr firsts in SCI: " + str(self.nbr_first_sci) + ") "

    def __lt__(self, other):
        return self.first_ratio < other._first_ratio
    
    def add_publication(self, publ):
        if not isinstance(publ, SEPublication):
            raise TypeError("Error: do not add anything but instances of publication.SEPublication to the collection")
        self.nbr_first_sci = 0
        self.publications.add(publ)
        if publ.sci_listed:
            self.nbr_first_sci += 1
        
    def get_nbr_publications(self):
        return len(self.publications)
    
    def get_nbr_sci_publications(self):
        nbr = 0
        for publ in self.publications:
            if publ.sci_listed:
                nbr += 1
        return nbr
    
    def get_nbr_main_confs(self):
        nbr = 0
        for publ in self.publications:
            if publ.major_conf:
                nbr += 1
        return nbr
    
    def get_first_author_titles(self):
        first_author_titles = []
        for p in self.publications:
            if (p.authors[0] == self.name):
                first_author_titles.append(p.title)
        return first_author_titles
        
    def sci_publications_to_string(self):
        result = ""
        for publ in self.publications:
            if publ.sci_listed and publ.authors[0] == self.name:
                result += "\t" + str(publ.year) + ": " + publ.title + " (" + str(publ.journal) + ")" + "\n"
        return result

    def append_research_interest(self, research_interest):
        self.research_interests.append(research_interest)

    def calc_stats(self):
        nbr_first_author = 0
        nbr_sci_listed = 0
        self.nbr_first_sci = 0
        for publ in self.publications:
            try:
                if publ.sci_listed and publ.authors[0] == self.name:
                    nbr_first_author += 1
                    nbr_sci_listed += 1
                    self.nbr_first_sci += 1
                elif publ.authors[0] == self.name:
                    nbr_first_author += 1
                elif publ.sci_listed:
                    nbr_sci_listed += 1
            except:
                print("No authors for the publication: " + publ.title)
                
        if self.get_nbr_publications() > 0:
            self.first_ratio = nbr_first_author / self.get_nbr_publications()
            self.sci_ratio = nbr_sci_listed / self.get_nbr_publications()
        print(self.to_string())

    def to_string(self):
        return self.name + " (" + str(len(self.publications)) + " publications. First-ratio: " + str(round(self.first_ratio, 2)) + " SCI-ratio: " + str(round(self.sci_ratio, 2)) + " Nbr firsts in SCI: " + str(self.nbr_first_sci) + " Nbr main confs: " + str(self.get_nbr_main_confs()) + ")"
    
    def to_csv_line(self):
        return self.name + ";" + str(self.dblp_entries) + ";" + str(len(self.publications)) + ";" + str(self.first_ratio) + ";" + str(self.sci_ratio) + ";" + str(self.nbr_first_sci) + ";" + str(self.get_nbr_main_confs())
    
    def research_interests_to_string(self):
        ''' Return a comma separated string by concatenating research interests. '''
        result = ""
        for term in self.research_interests:
            result += term + ", "
        return result[:-2] # remove two final chars