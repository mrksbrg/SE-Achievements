import statistics
from sortedcontainers import SortedSet
from .publication import SSSPublication

class SSSScholar:
    def __init__(self, name, affiliation):
        # Some redundancy needed for use with Jinja2
        self.name = name
        self.affiliation = affiliation
        self.research_interests = []
        self.research_interests_string = ""

        self.signature_works = []
        self.sss_contrib = -1
        self.sss_rating = -1

        self.dblp_entries = -1
        self.publications = SortedSet()
        self.nbr_publications = -1
        self.first_ratio = -1
        self.sci_ratio = -1
        self.nbr_sci_publications = -1
        self.nbr_first_sci = -1
                
    def __str__(self):
        return self.name + " (" + str(len(self.publications)) + " publications)"
    
    def __repr__(self):
        return self.name + " (" + str(len(self.publications)) + " publications. First-ratio: " + str(self.first_ratio)\
               + "SCI-ratio: " + str(self.sci_ratio) + " Nbr firsts in SCI: " + str(self.nbr_first_sci) + ") "

    def __lt__(self, other):
        return self.sss_rating < other.sss_rating

    def clear(self):
        self.research_interests = []
        self.research_interests_string = ""
        self.signature_works = []
        self.sss_contrib = -1
        self.sss_rating = -1
        self.dblp_entries = -1
        self.publications = SortedSet()
        self.nbr_publications = -1
        self.first_ratio = -1
        self.sci_ratio = -1
        self.nbr_sci_publications = -1
        self.nbr_first_sci = -1

    def add_publication(self, publ):
        if not isinstance(publ, SSSPublication):
            raise TypeError("Error: do not add anything but instances of publication.SEPublication to the collection")
        if self.nbr_first_sci == -1:
            self.nbr_first_sci = 0
        if self.nbr_publications == -1:
            self.nbr_publications = 0
        self.publications.add(publ)
        self.nbr_publications += 1
        if publ.sci_listed:
            self.nbr_first_sci += 1
    
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
                result += str(publ.year) + ": " + publ.title + " (" + str(publ.journal) + ")" + "\n"
        return result

    def append_research_interest(self, research_interest):
        self.research_interests.append(research_interest)

    def calc_stats(self):
        ''' Calculating statistics for the scholar. Shall be called after ScholarMiner is done. '''
        nbr_first_author = 0
        self.nbr_sci_publications = 0
        self.nbr_first_sci = 0
        for publ in self.publications:
            try:
                if publ.sci_listed and publ.authors[0] == self.name:
                    nbr_first_author += 1
                    self.nbr_sci_publications += 1
                    self.nbr_first_sci += 1
                elif publ.authors[0] == self.name:
                    nbr_first_author += 1
                elif publ.sci_listed:
                    self.nbr_sci_publications += 1
            except:
                print("No authors for the publication: " + publ.title)

        if self.nbr_publications > 0:
            # Calculate SCI ratio. Round up to 0.01 if needed.
            tmp_ratio = self.nbr_sci_publications / self.nbr_publications
            if tmp_ratio > 0 and tmp_ratio < 0.01:
                self.sci_ratio = 0.01
            else:
                self.sci_ratio = round(self.nbr_sci_publications / self.nbr_publications, 2)

            # Calculate 1st author ratio. Round up to 0.01 if needed.
            tmp_ratio = nbr_first_author / self.nbr_publications
            if tmp_ratio > 0 and tmp_ratio < 0.01:
                self.first_ratio = 0.01
            else:
                self.first_ratio = round(nbr_first_author / self.nbr_publications, 2)

        print(self.to_string())

        # SSS Contribution = first-authored SCI + 0.1 * first-authored non-SCI
        self.sss_contrib = self.nbr_first_sci + 0.1 * (self.nbr_sci_publications - self.nbr_first_sci) + 0.01 * (self.nbr_publications - self.nbr_sci_publications)
        self.sss_contrib = round(self.sss_contrib, 2)

        # SSS Rating = #publications * harmonic mean of sci-ratio and 1st-ratio
        if self.sci_ratio+self.first_ratio != 0:
            harmonic_mean = statistics.harmonic_mean(self.sci_ratio, self.first_ratio)
            #weighted_harmonic_mean = (2 * self.sci_ratio * self.first_ratio) / (self.sci_ratio + self.first_ratio)
            #statistics.harmonic_mean(self.sci_ratio, self.first_ratio)
            self.sss_rating = round(self.nbr_publications * harmonic_mean, 2)
        else:
            self.sss_rating = 0

    def calc_titles(self):
        self.research_interests_string = self.research_interests_to_string()
        self.signature_works = self.sci_publications_to_string()

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