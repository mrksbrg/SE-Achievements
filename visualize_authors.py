# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 11:21:15 2019

@author: Markus Borg
"""

import csv
from datetime import date
from yellowbrick.text import TSNEVisualizer
from sklearn.feature_extraction.text import TfidfVectorizer

def __init__(self, filename):
    self.filename = filename
    self.scholars = {}

def parse_csv(self):
    with open(str(date.today()) + "_Authors_all_titles.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        
        line_count = 0
        for row in csv_reader:
            self.scholars[row[0]] = row[1]
            print(f'\t{row[0]} works in the {row[1]} department.')
            line_count += 1
        print(f'Processed {line_count} lines.')

def visualize(input):
    corpus = input
    tfidf  = TfidfVectorizer()

    docs = tfidf.fit_transform(corpus.data)
    labels = corpus.target
    
    # Create the visualizer and draw the vectors
    tsne = TSNEVisualizer()
    tsne.fit(docs, labels)
    tsne.poof()
 

parse_csv()