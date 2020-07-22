from sortedcontainers import SortedSet
from .publication import SSSPublication

class SSSScholar:

    def __init__(self, name, running_number, affiliation):
        # Some redundancy needed for use with Jinja2
        self.name = name
        self.running_number = running_number
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

        # SWEBOK Knowledge Areas
        self.knowl_areas = [False] * 14
        self.knowl_area_counters = [0] * 14
        self.knowl_areas_string = ""
                
    def __str__(self):
        if self.running_number == -1:
            return self.name + " (" + str(len(self.publications)) + " publications)"
        else:
            return self.name + " " + self.running_number + " (" + str(len(self.publications)) + " publications)"
    
    def __repr__(self):
        return self.name + " (" + str(len(self.publications)) + " publications. First-ratio: " + str(self.first_ratio)\
               + " SCI-ratio: " + str(self.sci_ratio) + " Nbr firsts in SCI: " + str(self.nbr_first_sci) + ") "

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
        self.knowl_areas = [False] * 14
        self.knowl_area_counters = [0] * 14
        self.knowl_areas = ""

    def add_publication(self, publ):
        if not isinstance(publ, SSSPublication):
            raise TypeError("Error: do not add anything but instances of publication.SSSPublication to the collection")
        if self.nbr_first_sci == -1:
            self.nbr_first_sci = 0
        if self.nbr_publications == -1:
            self.nbr_publications = 0
        self.publications.add(publ)
        self.nbr_publications += 1
        if publ.sci_listed:
            self.nbr_first_sci += 1
        # Add corresponding SWEBOK Knowledge Area
        if publ.knowl_area >= 0:
            self.knowl_area_counters[publ.knowl_area] += 1
        print(self.knowl_area_counters)
    
    def get_nbr_main_confs(self):
        nbr = 0
        for publ in self.publications:
            if publ.major_conf:
                nbr += 1
        return nbr
    
    def get_first_author_titles(self):
        first_author_titles = []
        for publ in self.publications:
            if self.running_number == -1:
                if publ.authors[0] == self.name:
                    first_author_titles.append(publ.title)
            else:
                if publ.authors[0] == str(self.name + " " + self.running_number):
                    first_author_titles.append(publ.title)
        return first_author_titles
        
    def sci_publications_to_string(self):
        result = ""
        for publ in self.publications:
            if self.running_number == -1:
                if publ.sci_listed and publ.authors[0] == self.name:
                    result += str(publ.year) + ": " + publ.title + " (" + str(publ.journal) + ")" + "\n"
            else:
                if publ.sci_listed and publ.authors[0] == str(self.name + " " + self.running_number):
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
                if self.running_number == -1:  # author has no running number
                    if publ.sci_listed and publ.authors[0] == self.name:
                        nbr_first_author += 1
                        self.nbr_sci_publications += 1
                        self.nbr_first_sci += 1
                    elif publ.authors[0] == self.name:
                        nbr_first_author += 1
                    elif publ.sci_listed:
                        self.nbr_sci_publications += 1
                else:  # author has a running number
                    if publ.sci_listed and publ.authors[0] == str(self.name + " " + self.running_number):
                        nbr_first_author += 1
                        self.nbr_sci_publications += 1
                        self.nbr_first_sci += 1
                    elif publ.authors[0] == str(self.name + " " + self.running_number):
                        nbr_first_author += 1
                    elif publ.sci_listed:
                        self.nbr_sci_publications += 1
            except Exception as e:
                print(e)
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

        # SSS Rating = #publications * weighted harmonic mean of sci-ratio (w=2) and 1st-ratio (w=1)
        if self.sci_ratio > 0 and self.first_ratio > 0:
            weight_sci = 2
            weight_first = 1
            weighted_harmonic_mean = (weight_sci+weight_first) / ((weight_sci/self.sci_ratio) + (weight_first/self.first_ratio))
            self.sss_rating = round(self.nbr_publications * weighted_harmonic_mean, 2)
        else:
            self.sss_rating = 0

    def calc_titles(self):
        self.research_interests_string = self.research_interests_to_string()
        self.signature_works = self.sci_publications_to_string()

    def calc_knowl_areas(self):
        if self.knowl_area_counters[0] >= 2:
            self.knowl_areas[0] = True
            self.knowl_areas_string += "RE, "
        if self.knowl_area_counters[1] >= 1:
            self.knowl_areas[1] = True
            self.knowl_areas_string += "Design, "

    def to_string(self):
        return self.name + " (" + str(len(self.publications)) + " publications. SCI-ratio: " + str(round(self.sci_ratio, 2)) + " 1st-ratio: " + str(round(self.first_ratio, 2))  + " Nbr firsts in SCI: " + str(self.nbr_first_sci) + " Nbr main confs: " + str(self.get_nbr_main_confs()) + ")"
    
    def to_csv_line(self):
        return self.name + ";" + str(self.dblp_entries) + ";" + str(len(self.publications)) + ";" + str(self.sci_ratio) + ";" + str(self.first_ratio) + ";" + str(self.nbr_first_sci) + ";" + str(self.get_nbr_main_confs())
    
    def research_interests_to_string(self):
        ''' Return a comma separated string by concatenating research interests. '''
        result = ""
        for term in self.research_interests:
            result += term + ", "
        return result[:-2] # remove two final chars