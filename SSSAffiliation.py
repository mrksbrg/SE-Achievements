class SSSAffiliation:

    def __init__(self, name):
        self.name = name
        self.topics = []

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

