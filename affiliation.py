class SSSAffiliation:

    def __init__(self, name):
        self.name = name
        self.nbr_scholars = 0
        self.total_sss_contrib = 0
        self.top_terms = []
        self.top_terms_string = ""
        self.nbr_topics = 0
        self.topics = []
        self.topics_string = ""

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.total_sss_contrib < other.total_sss_contrib

    def add_term(self, term):
        self.top_terms.append(term)

    def add_topics(self, topics):
        self.topics = topics

    def calc_topics(self):
        self.topics_string = self.topics_to_string()

    def topics_to_string(self):
        ''' Return a comma separated string by concatenating topics. '''
        result = ""
        counter = 1
        for terms in self.topics:
            result += "Topic " + str(counter) + ": " + str(terms) + ";\n"
            counter += 1
        return result[:-2] # remove two final chars
