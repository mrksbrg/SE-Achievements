import xml.sax
from sortedcontainers import SortedSet
#import SSSPublication
#import SSSScholar

class ScholarHandler(xml.sax.ContentHandler):
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


    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "article":
            key = attributes["key"]
            #print("Article:", key)
        elif tag == "inproceedings":
            key = attributes["key"]
            #print("inproceedings:", key)

    def endElement(self, tag):
        if self.CurrentData == "article":
            #print("Article:", self.article)
            title = self.article
        elif self.CurrentData == "year":
            #print("Year:", self.year)
            year = self.year
        self.CurrentData = ""

    def characters(self, content):
        if self.CurrentData == "name":
            self.name = content
        elif self.CurrentData == "article":
            self.title = content
        elif self.CurrentData == "year":
            self.year = content

if (__name__ == "__main__"):
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    Handler = ScholarHandler()
    parser.setContentHandler(Handler)

    parser.parse("9384.xml")
    print("Done")