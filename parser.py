# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 17:24:44 2017

@author: Markus
"""

class Author:  
    def __init__(self, name):
        self.name = name        
        self.pubList = list()
        
    def __str__(self):
        return self.name + " (" + str(len(self.pubList)) + " publications)"
        
    def addPublication(self, pubKey):
        self.pubList.append(pubKey)
     
class Publication:    
    def __init__(self, title, authorList, year, type):
        self.title = title        
        self.authorList = authorList
        self.year = year
        self.type = type
        
    def __str__(self):
        temp = ''
        for a in self.authorList:
            temp += a + ", ";     
        return self.title + " BY " + temp + "(" + str(self.year) + ")"
    
def addPublicationToAuthor (name, pubKey):
    if name in authors:
        authors[name].addPublication(pubKey)
    else:
        tempAuthor = Author(name)
        tempAuthor.addPublication(pubKey)
        authors[name] = tempAuthor    
        
import xml.etree.cElementTree as etree

authors = {}
publications = {}
tempAuthorList = list()

for event, elem in etree.iterparse('dblp_test.xml'): # default is only 'end' events

    if elem.tag == 'title':
        title = elem.text
    elif elem.tag == 'year':
        pubYear = elem.text
    elif elem.tag == 'author':
        tempAuthor = elem.text
        tempAuthorList.append(tempAuthor)
        temp = ''
      
    elif elem.tag == 'article':
        pubKey = elem.get("key")
        pub = Publication(title, tempAuthorList, pubYear, "TEMP")
        publications[pubKey] = pub
        
        # add a publication ref to all co-authors
        for a in tempAuthorList:
            addPublicationToAuthor(a, pubKey)

        tempAuthorList = list() # clear the temp list

print ("All " + str(len(authors)) + " authors:")
for a in authors:
    print (authors[a])
    
print ('\nAll ' + str(len(publications)) + ' publications:')
for i in publications:
    print (publications[i])
