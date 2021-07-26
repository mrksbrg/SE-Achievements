import datetime
from sortedcontainers import SortedSet
from .publication import SSSPublication


class SSSScholar:

    def __init__(self, name, running_number, pid, url, affiliation, dblp_entries):
        # Some redundancy needed for use with Jinja2
        self.name = name
        self.running_number = running_number
        self.pid = pid
        self.url = url
        self.affiliation = affiliation
        self.dblp_entries = dblp_entries
        self.research_interests = []
        self.research_interests_string = ""

        self.signature_works = []
        self.sss_contrib = -1
        self.sss_rating = -1

        self.publications = SortedSet()
        self.nbr_publications = -1
        self.first_ratio = -1
        self.sci_ratio = -1
        self.nbr_sci_publications = -1
        self.nbr_first_sci = -1

        # SWEBOK Knowledge Areas
        self.NBR_AREAS = 22
        self.swebok_counters = [0] * self.NBR_AREAS
        self.swebok_badges = [0] * self.NBR_AREAS
        self.swebok_string = ""
        self.swebok_works = [""] * self.NBR_AREAS
        self.swebok_re_string = ""
        self.swebok_design_string = ""
        self.swebok_constr_string = ""
        self.swebok_test_string = ""
        self.swebok_maint_string = ""
        self.swebok_cm_string = ""
        self.swebok_mgmt_string = ""
        self.swebok_process_string = ""
        self.swebok_models_string = ""
        self.swebok_quality_string = ""
        self.swebok_practice_string = ""
        self.swebok_economics_string = ""
        self.swebok_comp_string = ""
                
    def __str__(self):
        if self.running_number == -1:
            return self.name + " [" + self.pid + "]" + " (" + str(len(self.publications)) + " publications)"
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
        self.swebok_counters = [0] * self.NBR_AREAS
        self.swebok_badges = [0] * self.NBR_AREAS
        self.swebok_string = ""
        self.swebok_works = [""] * self.NBR_AREAS
        self.swebok_re_string = ""
        self.swebok_design_string = ""
        self.swebok_constr_string = ""
        self.swebok_test_string = ""
        self.swebok_maint_string = ""
        self.swebok_cm_string = ""
        self.swebok_mgmt_string = ""
        self.swebok_process_string = ""
        self.swebok_models_string = ""
        self.swebok_quality_string = ""
        self.swebok_practice_string = ""
        self.swebok_economics_string = ""
        self.swebok_comp_string = ""

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
        first_author = False
        if self.running_number == -1:
            if publ.authors[0][0] == self.name or publ.authors[0][0] == str(self.name + " 0001"):
                #print("First author name without running number matches: " + publ.title)
                first_author = True
        else:
            if publ.authors[0][0] == str(self.name + " " + self.running_number):
                #print("First author name with running number (" + self.running_number + "): " + publ.title)
                first_author = True
        if first_author and publ.knowl_area >= 0:
            self.swebok_counters[publ.knowl_area] += 1
            if publ.booktitle != -1:
                # conference publication
                tmp_work = str(publ.year) + ": " + publ.title + " (" + publ.booktitle + ") "
                self.swebok_works[publ.knowl_area] += tmp_work
                self.add_to_swebok_string(tmp_work, publ.knowl_area)
            else:
                # journal publication
                tmp_work = str(publ.year) + ": " + publ.title + " (" + publ.journal + ") "
                self.swebok_works[publ.knowl_area] += tmp_work
                self.add_to_swebok_string(tmp_work, publ.knowl_area)

    # add to the string that Jinja uses
    def add_to_swebok_string(self, str, knowl_area_id):
        if knowl_area_id == 0:
            self.swebok_re_string += str
        elif knowl_area_id == 1:
            self.swebok_design_string += str
        elif knowl_area_id == 2:
            self.swebok_constr_string += str
        elif knowl_area_id == 3:
            self.swebok_test_string += str
        elif knowl_area_id == 4:
            self.swebok_maint_string += str
        elif knowl_area_id == 5:
            self.swebok_cm_string += str
        elif knowl_area_id == 6:
            self.swebok_mgmt_string += str
        elif knowl_area_id == 7:
            self.swebok_process_string += str
        elif knowl_area_id == 8:
            self.swebok_models_string += str
        elif knowl_area_id == 9:
            self.swebok_quality_string += str
        elif knowl_area_id == 10:
            self.swebok_practice_string += str
        elif knowl_area_id == 11:
            self.swebok_economics_string += str
        elif knowl_area_id == 12:
            self.swebok_comp_string += str

    def get_nbr_ICSE(self):
        nbr = 0
        for publ in self.publications:
            if publ.major_conf:
                nbr += 1
        return nbr
    
    def get_first_author_titles(self):
        first_author_titles = []
        for publ in self.publications:
            if self.running_number == -1:
                if publ.authors[0][0] == self.name:
                    first_author_titles.append(publ.title)
            else:
                if publ.authors[0][0] == str(self.name + " " + self.running_number):
                    first_author_titles.append(publ.title)
        return first_author_titles

    def get_recent_titles(self):
        '''
        :return: Return a list of the recent (5 years) titles
        '''
        recent_publications = ""
        now = datetime.datetime.now()
        for p in self.publications:
            if int(p.year) >= int(now.year) - 5:
                recent_publications += p.title + " "
        return recent_publications

    def sci_publications_to_string(self):
        result = ""
        for publ in self.publications:
            if self.running_number == -1:
                if publ.sci_listed and publ.authors[0][0] == self.name:
                    result += str(publ.year) + ": " + publ.title + " (" + str(publ.journal) + ")" + "\n"
            else:
                if publ.sci_listed and publ.authors[0][0] == str(self.name + " " + self.running_number):
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
                    if publ.sci_listed and publ.authors[0][0] == self.name:
                        nbr_first_author += 1
                        self.nbr_sci_publications += 1
                        self.nbr_first_sci += 1
                    elif publ.authors[0][0] == self.name:
                        nbr_first_author += 1
                    elif publ.sci_listed:
                        self.nbr_sci_publications += 1
                else:  # author has a running number
                    if publ.sci_listed and publ.authors[0][0] == str(self.name + " " + self.running_number):
                        nbr_first_author += 1
                        self.nbr_sci_publications += 1
                        self.nbr_first_sci += 1
                    elif publ.authors[0][0] == str(self.name + " " + self.running_number):
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

    def badge_grader(self, number):
        # 1 = Bronze, 3 = Silver, 5 = Gold, 10 = Platinum
        level = 0
        if number >= 1:
            level = 1
            if number >= 3:
                level = 2
                if number >= 5:
                    level = 3
                    if number >= 10:
                        level = 4
        return level

    def unlock_achievements(self):
        # Inspiration "Once is chance, twice is coincidence, three times is a pattern"
        if self.swebok_counters[0] >= 1:
            self.swebok_badges[0] = self.badge_grader(self.swebok_counters[0])
            self.swebok_string += str(self.swebok_badges[0]) + "-RE, "
        if self.swebok_counters[1] >= 1:
            self.swebok_badges[1] = self.badge_grader(self.swebok_counters[1])
            self.swebok_string += str(self.swebok_badges[1]) + "-Design, "
        if self.swebok_counters[2] >= 1:
            self.swebok_badges[2] = self.badge_grader(self.swebok_counters[2])
            self.swebok_string += str(self.swebok_badges[2]) + "-Constr, "
        if self.swebok_counters[3] >= 1:
            self.swebok_badges[3] = self.badge_grader(self.swebok_counters[3])
            self.swebok_string += str(self.swebok_badges[3]) + "-Test, "
        if self.swebok_counters[4] >= 1:
            self.swebok_badges[4] = self.badge_grader(self.swebok_counters[4])
            self.swebok_string += str(self.swebok_badges[4]) + "-Maint, "
        if self.swebok_counters[5] >= 1:
            self.swebok_badges[5] = self.badge_grader(self.swebok_counters[5])
            self.swebok_string += str(self.swebok_badges[5]) + "-CM, "
        if self.swebok_counters[6] >= 1:
            self.swebok_badges[6] = self.badge_grader(self.swebok_counters[6])
            self.swebok_string += str(self.swebok_badges[6]) + "-Mgmt, "
        if self.swebok_counters[7] >= 1:
            self.swebok_badges[7] = self.badge_grader(self.swebok_counters[7])
            self.swebok_string += str(self.swebok_badges[7]) + "-Process, "
        if self.swebok_counters[8] >= 1:
            self.swebok_badges[8] = self.badge_grader(self.swebok_counters[8])
            self.swebok_string += str(self.swebok_badges[8]) + "-Models, "
        if self.swebok_counters[9] >= 1:
            self.swebok_badges[9] = self.badge_grader(self.swebok_counters[9])
            self.swebok_string += str(self.swebok_badges[9]) + "-Quality, "
        if self.swebok_counters[10] >= 1:
            self.swebok_badges[10] = self.badge_grader(self.swebok_counters[10])
            self.swebok_string += str(self.swebok_badges[10]) + "-Practice, "
        if self.swebok_counters[11] >= 1:
            self.swebok_badges[11] = self.badge_grader(self.swebok_counters[11])
            self.swebok_string += str(self.swebok_badges[11]) + "-Economics, "
        if self.swebok_counters[12] >= 1:
            self.swebok_badges[12] = self.badge_grader(self.swebok_counters[12])
            self.swebok_string += str(self.swebok_badges[12]) + "-Computing, "
        if self.swebok_counters[13] >= 1:
            self.swebok_badges[13] = self.badge_grader(self.swebok_counters[13])
            self.swebok_string += str(self.swebok_badges[13]) + "-Maths, "
        if self.swebok_counters[14] >= 1:
            self.swebok_badges[14] = self.badge_grader(self.swebok_counters[14])
            self.swebok_string += str(self.swebok_badges[14]) + "-Eng, "
        if self.swebok_counters[15] >= 1:
            self.swebok_badges[15] = self.badge_grader(self.swebok_counters[15])
            self.swebok_string += str(self.swebok_badges[15]) + "-ICSE, "
        if self.swebok_counters[16] >= 1:
            self.swebok_badges[16] = self.badge_grader(self.swebok_counters[16])
            self.swebok_string += str(self.swebok_badges[16]) + "-Prestige, "
        if self.swebok_counters[17] >= 1:
            self.swebok_badges[17] = self.badge_grader(self.swebok_counters[17])
            self.swebok_string += str(self.swebok_badges[17]) + "-Emp, "
        if self.swebok_counters[18] >= 1:
            self.swebok_badges[18] = self.badge_grader(self.swebok_counters[18])
            self.swebok_string += str(self.swebok_badges[18]) + "-IS, "
        if self.swebok_counters[19] >= 1:
            self.swebok_badges[19] = self.badge_grader(self.swebok_counters[19])
            self.swebok_string += str(self.swebok_badges[19]) + "-HCI, "
        if self.swebok_counters[20] >= 1:
            self.swebok_badges[20] = self.badge_grader(self.swebok_counters[20])
            self.swebok_string += str(self.swebok_badges[20]) + "-Assure, "
        if self.swebok_counters[21] >= 1:
            self.swebok_badges[21] = self.badge_grader(self.swebok_counters[21])
            self.swebok_string += str(self.swebok_badges[21]) + "-Web, "

    def to_string(self):
        return self.name + " [" + self.pid + "] (" + str(len(self.publications)) + " publications. SCI-ratio: " + str(round(self.sci_ratio, 2)) + " 1st-ratio: " + str(round(self.first_ratio, 2)) + " Nbr firsts in SCI: " + str(self.nbr_first_sci) + " Nbr first ICSE: " + str(self.get_nbr_ICSE()) + ")"
    
    def to_csv_line(self):
        return self.name + ";" + str(self.dblp_entries) + ";" + str(len(self.publications)) + ";" + str(self.sci_ratio) + ";" + str(self.first_ratio) + ";" + str(self.nbr_first_sci) + ";" + str(self.get_nbr_ICSE())
    
    def research_interests_to_string(self):
        ''' Return a comma separated string by concatenating research interests. '''
        result = ""
        for term in self.research_interests:
            result += term + ", "
        return result[:-2] # remove two final chars