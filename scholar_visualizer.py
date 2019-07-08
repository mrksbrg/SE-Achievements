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

from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk

from wordcloud import WordCloud

from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.decomposition import NMF

import matplotlib.pyplot as plt


class ScholarVisualizer:
    def __init__(self, filename_prefix):
        self.filename_prefix = filename_prefix
        self.scholars_dict = {}
        self.scholars_list = []
        self.tailored_stop_words = []
        self.stopped_corpus = None
        #self.stemmed_corpus = None
        
        self.parse_csv()
    
    def parse_csv(self):
        with open(self.filename_prefix + "1_titles_per_author.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            
            line_count = 0
            for row in csv_reader:
                self.scholars_dict[row[0]] = row[1]
                self.scholars_list.append(row[1])
                line_count += 1
    
    def preprocess(self):
        stop_words = set(stopwords.words('english'))

        self.tailored_stop_words = stop_words.union(["software", "engineering", "based", 
                                                          "using", "case", "study", "oriented", 
                                                          "driven", "workshop", "research",
                                                          "übersetzerbau", "zur", "survey",
                                                          "approach", "overview", "summary",
                                                          "use", "multi", "experiment",
                                                          "review", "non", "approaches",
                                                          "controlled", "intensive", "exploratory",
                                                          "studies", "experimental", "evaluation", 
                                                          "experiments", "toward", "s", "1st", 
                                                          "ieee"])
    
    
        corpus = word_tokenize(str(self.scholars_list))
        corpus = [word.lower() for word in corpus]
        
        tokenizer = RegexpTokenizer(r'\w+')
        corpus = tokenizer.tokenize(str(corpus))
    
        stopped_corpus = []
        for word in corpus:
            if word not in self.tailored_stop_words:
                stopped_corpus.append(word)
                        
        self.stopped_corpus = stopped_corpus
        
#        stemmer = PorterStemmer()
#        stemmed_corpus = []
#        for word in stopped_corpus:
#            stemmed_corpus.append(stemmer.stem(word))
#            
#        self.stemmed_corpus = stemmed_corpus
    
    def visualize(self):
        if self.stopped_corpus == None:
            print("Preprocess first")
            return
        
        # Preprocessing
        self.preprocess()
               
        # Print research interests
        word_dist = nltk.FreqDist(self.stopped_corpus)   
        top = word_dist.most_common(5)
        research_interests = ""
        for term in top:
            research_interests += str(term[0]) + ", "
        research_interests = research_interests[:-2] # remove two final chars
        print("### Apparent research interests: " + research_interests)
        
        tf_vec = CountVectorizer(stop_words=self.tailored_stop_words)
        tfidf_vec = TfidfVectorizer(stop_words=self.tailored_stop_words) 
        
        # TF and TFIDF
        tf = tf_vec.fit_transform(self.stopped_corpus)
        tf_feature_names = tf_vec.get_feature_names()
        tfidf = tfidf_vec.fit_transform(self.stopped_corpus)
        tfidf_feature_names = tfidf_vec.get_feature_names()
        
        nbr_topics = 8
        nbr_words = 7

        # LDA
        lda = LDA(n_components=nbr_topics)  
        lda.fit(tf)
        
        # NMF
        #nmf = NMF(n_components=nbr_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)

        print("### LDA topics ###")
        self.display_topics(lda, tf_feature_names, nbr_words)
        #print("\n### NMF topics ###")
        #self.display_topics(nmf, tfidf_feature_names, nbr_words)
    
        # t-SNE
#        docs = tf_vec.fit_transform(self.scholars_list)
#        features = tf_vec.get_feature_names()
#        print(tf_vec.max_features)
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
#        cloud = wordcloud.generate(str(self.stopped_corpus).replace("'",""))
#
#        plt.imshow(cloud, interpolation='bilinear')
#        plt.title("Someone")
#        plt.axis("off")
#        plt.show()
        
    def display_topics(self, model, feature_names, no_top_words):
        for topic_idx, topic in enumerate(model.components_):
            print("Topic %d:" % (topic_idx))
            print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
 
#vis = Visualizer(str(date.today()) + "_Authors_all_titles.csv")
#vis.parse_csv()
#vis.visualize()