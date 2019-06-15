class Scholar:  
    def __init__(self, name):
        self.name = name        
        self.publications = set()
        
    def __str__(self):
        return self.name + " (" + str(len(self.publications)) + " publications)"
        
    def add_publication(self, publ):
        self.publications.add(publ)