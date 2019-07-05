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
from nltk.stem.porter import PorterStemmer

from wordcloud import WordCloud

from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.decomposition import NMF

import matplotlib.pyplot as plt


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
            #print(self.scholars_list)
                
    def display_topics(self, model, feature_names, no_top_words):
        for topic_idx, topic in enumerate(model.components_):
            print("Topic %d:" % (topic_idx))
            print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
    
    def visualize(self):
        
        # Preprocessing
        extra_stop_words = text.ENGLISH_STOP_WORDS.union(["software", "engineering", "based", 
                                                          "using", "case", "study", "oriented", 
                                                          "driven", "workshop", "research",
                                                          "übersetzerbau", "zur", "survey",
                                                          "approach", "overview", "summary",
                                                          "use", "multi", "experiment",
                                                          "review", "non", "approaches",
                                                          "controlled"])
        tf_vec = CountVectorizer(stop_words=text.ENGLISH_STOP_WORDS.union(extra_stop_words))
        tfidf_vec = TfidfVectorizer(stop_words=text.ENGLISH_STOP_WORDS.union(extra_stop_words))     
        stemmer = PorterStemmer()
        stemmed_corpus = []
        for word in self.scholars_list:
            stemmed_corpus.append(stemmer.stem(word))
            
        tf = tf_vec.fit_transform(stemmed_corpus)
        tf_feature_names = tf_vec.get_feature_names()
        tfidf = tfidf_vec.fit_transform(stemmed_corpus)
        tfidf_feature_names = tfidf_vec.get_feature_names()
        
        nbr_topics = 8
        nbr_words = 7

        # LDA
        lda = LDA(n_components=nbr_topics)  
        lda.fit(tf)
        
        # NMF
        nmf = NMF(n_components=nbr_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)

        print("### LDA topics ###")
        self.display_topics(lda, tf_feature_names, nbr_words)
        print("\n### NMF topics ###")
        self.display_topics(nmf, tfidf_feature_names, nbr_words)
    
        # t-SNE
#        docs = vectorizer.fit_transform(self.scholars_list)
#        features = vectorizer.get_feature_names()
#        visualizer = FreqDistVisualizer(features=features)
#        visualizer.fit(docs)
#        visualizer.poof()      
#        
#        docs = tfidf.fit_transform(stemmed_corpus)        
#        labels = list(self.scholars_dict.keys())
#        tsne = TSNEVisualizer()
#        tsne.fit_transform(tfidf, labels)
#        tsne.poof()
        
        # Wordcloud
#        wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
#        cloud = wordcloud.generate(stemmed_corpus[1])
#
#        plt.imshow(cloud, interpolation='bilinear')
#        plt.title("Someone")
#        plt.axis("off")
#        plt.show()
 
vis = Visualizer(str(date.today()) + "_Authors_all_titles.csv")
vis.parse_csv()
vis.visualize()