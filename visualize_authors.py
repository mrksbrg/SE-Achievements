# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 11:21:15 2019

@author: Markus Borg
"""

import csv
from datetime import date

import numpy as np
from yellowbrick.text import FreqDistVisualizer
from yellowbrick.text import TSNEVisualizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text

class Visualizer:
    def __init__(self, filename):
        self.filename = filename
        self.scholars_dict = {}
        self.scholars_list = []
    
    def parse_csv(self):
        with open(self.filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            
            line_count = 0
            for row in csv_reader:
                self.scholars_dict[row[0]] = row[1]
                self.scholars_list.append(row[1])
                line_count += 1
            print(self.scholars_list)
    
    def visualize(self):
        vectorizer = CountVectorizer(stop_words=text.ENGLISH_STOP_WORDS)
        docs = vectorizer.fit_transform(self.scholars_list)
        features = vectorizer.get_feature_names()
        visualizer = FreqDistVisualizer(features=features)
        visualizer.fit(docs)
        visualizer.poof()
        
        tfidf = TfidfVectorizer(stop_words=text.ENGLISH_STOP_WORDS)
        docs = tfidf.fit_transform(self.scholars_list)
        labels = list(self.scholars_dict.keys())
        tsne = TSNEVisualizer()
        tsne.fit_transform(docs, labels)
        tsne.poof()

#        tfidf  = TfidfVectorizer()
#    
#        docs = tfidf.fit_transform(corpus)
#        labels = corpus.target
#        
#        # Create the visualizer and draw the vectors
#        tsne = TSNEVisualizer()
#        tsne.fit(docs, labels)
#        tsne.poof()
 
vis = Visualizer(str(date.today()) + "_Authors_all_titles.csv")
vis.parse_csv()
vis.visualize()