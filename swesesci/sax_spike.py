import xml.sax
from sortedcontainers import SortedSet
#import SSSPublication
#import SSSScholar

class ScholarHandler(xml.sax.ContentHandler):

    state = -1
    current_pub_title = -1
    current_pub_journal = -1
    current_pub_booktitle = -1
    current_pub_year = -1
    current_pub_authors = []
    current_pub_informal = False

    def __init__(self):
        param1="Markus Borg"
        param2="0"
        param3="RISE"
        #scholar = SSSScholar(param1, param2, param3)

        # all this should be added during parsing
        # self.name = scholar.name
        # self.running_number = scholar.running_number
        # self.affiliation = scholar.affiliation
        # self.research_interests = []
        # self.research_interests_string = ""
        #
        # self.signature_works = []
        # self.sss_contrib = -1
        # self.sss_rating = -1
        #
        # self.dblp_entries = -1
        # self.publications = SortedSet()
        # self.nbr_publications = -1
        # self.first_ratio = -1
        # self.sci_ratio = -1
        # self.nbr_sci_publications = -1
        # self.nbr_first_sci = -1
        #
        # self.publications = SortedSet()

        # temp
        self.name = ""
        self.title = ""
        self.year = ""

    def clear_current_pub(self):
        self.current_pub_title = -1
        self.current_pub_journal = -1
        self.current_pub_booktitle = -1
        self.current_pub_year = -1
        self.current_pub_authors = []
        self.current_pub_informal = False

    def startElement(self, tag, attributes):
        self.state = 0
        #print("Starting element in state: " + str(self.state))
        self.CurrentData = tag
        # Opening person
        if tag == "dblpperson":
            self.state = 1
            author_name = attributes["name"]
            author_id = attributes["pid"]
            print("Author Name (ID):", author_name + " (" + str(author_id) + ")")
        # Opening journal paper
        elif tag == "article":
            self.state = 2
            self.clear_current_pub()
            # filter arXiv preprints
            attribute_list = attributes.getNames()
            if "publtype" in attribute_list and attributes["publtype"] == "informal":
                self.current_pub_informal = True
                print("Skipping an arXiv preprint")
        # Opening conference/workshop paper
        elif tag == "inproceedings":
            self.clear_current_pub()
            self.state = 3
        # Opening co-author
        elif tag == "author":
            self.state = 4
            author_ID = attributes["pid"]
            self.current_pub_authors.append(author_ID)

    def endElement(self, tag):
        # Closing person
        if tag == "dblpperson":
            self.state = 0
        # Closing journal paper
        elif tag == "article" and not self.current_pub_informal:
            #(self, title, journal, booktitle, year, authors)
            print("Journal: (" + str(self.current_pub_year + ") " + str(self.current_pub_title)))
            print("\tCo-authors: " + str(self.current_pub_authors))
            self.state = 0
        # Closing conference/workshop paper
        elif tag == "inproceedings":
            # (self, title, journal, booktitle, year, authors)
            print("Conf/ws paper: (" + str(self.current_pub_year + ") " + str(self.current_pub_title)))
            print("\tCo-authors: " + str(self.current_pub_authors))
            self.state = 0
        # Closing year
        elif tag == "title":
            self.current_pub_title = self.title
        # Closing year
        elif tag == "year":
            self.current_pub_year = self.year
        self.CurrentData = ""

    # Over write the characters method to get the content of an XML element
    def characters(self, content):
        if self.CurrentData == "name":
            self.name = content
        elif self.CurrentData == "article":
            self.article = content
        elif self.CurrentData == "title":
            self.title = content
        elif self.CurrentData == "year":
            self.year = content

if (__name__ == "__main__"):
    parser = xml.sax.make_parser()
    # turn off namespaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    Handler = ScholarHandler()
    parser.setContentHandler(Handler)

    parser.parse("9384.xml")
    print("Done")