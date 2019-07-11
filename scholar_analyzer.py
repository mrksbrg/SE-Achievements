# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 11:21:15 2019

@author: Markus Borg
"""

import csv

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk

from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.decomposition import NMF

class ScholarAnalyzer:

    def __init__(self, filename_prefix, swese_scholars):
        self.filename_prefix = filename_prefix
        self.swese_scholars = swese_scholars
        self.se_scholars = None
        self.scholars_dict = {}
        self.affiliations_dict = {}
        self.tailored_stop_words = []
        self.scholars_stopped_corpus = {}
        self.affiliations_stopped_corpus = {}

        self._nbr_swese_scholar = -1
        self._nbr_affiliations = -1
        self.parse_csv()    
        self.preprocess_titles()
    
    def parse_csv(self):
        with open(self.filename_prefix + "1_titles_per_author.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                self.scholars_dict[row[0]] = row[1]
        self._nbr_swese_scholar = len(self.scholars_dict)


        with open(self.filename_prefix + "1_titles_per_affiliation.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                self.affiliations_dict[row[0]] = row[1]

        self._nbr_affiliations = len(self.affiliations_dict)

    def preprocess_titles(self):
        ''' Create a dict with scholars as key and a list representing the corpus of title terms after stop word removal. '''
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
                                                          "ieee", "conference", "articles", 
                                                          "international", "cited", "towards",
                                                          "problems", "via"])

        # Preprocessing of authors' titles
        for scholar, corpus in self.scholars_dict.items():    
            self.scholars_stopped_corpus[scholar] = []
            
            corpus = word_tokenize(str(self.scholars_dict[scholar]))
            corpus = [word.lower() for word in corpus]
            
            tokenizer = RegexpTokenizer(r'\w+')
            corpus = tokenizer.tokenize(str(corpus))
        
            for word in corpus:
                if word not in self.tailored_stop_words:
                    self.scholars_stopped_corpus[scholar].append(word)

        # Preprocessing of affiliation' titles
        for affiliation, corpus in self.affiliations_dict.items():
            self.affiliations_stopped_corpus[affiliation] = []

            corpus = word_tokenize(str(self.affiliations_dict[affiliation]))
            corpus = [word.lower() for word in corpus]

            tokenizer = RegexpTokenizer(r'\w+')
            corpus = tokenizer.tokenize(str(corpus))

            for word in corpus:
                if word not in self.tailored_stop_words:
                    self.affiliations_stopped_corpus[affiliation].append(word)
            
#            stemmer = PorterStemmer()
#            stemmed_corpus = []
#            for word in stopped_corpus:
#                stemmed_corpus.append(stemmer.stem(word))
#                
#            self.stemmed_corpus = stemmed_corpus

    def write_results(self):
        tmp = open(self.filename_prefix + "2_analyzer_interests.csv", "w+")
        for scholar in self.swese_scholars:
            tmp.write(scholar.name + ";" + scholar.research_interests_to_string() + "\n")
        tmp.close()
    
    def analyze_individual_research_interests(self):
        ''' Extract apparent research interests from all scholars based on first-authored publications '''
        self.preprocess_titles()
        print("\n####### Apparent individual research interests #######")

        for scholar, corpus in self.scholars_dict.items():
            # Find the current scholar in the master list
            curr = next((x for x in self.swese_scholars if scholar == x.name), None)
            word_dist = nltk.FreqDist(self.scholars_stopped_corpus[scholar])
            top = word_dist.most_common(10)
            research_interests = ""
            for term in top:
                research_interests += str(term[0]) + ", "
                curr.append_research_interest(str(term[0]))
            research_interests = research_interests[:-2] # remove two final chars
            print(scholar + ": " + research_interests)

        print("\n####### Apparent research interests of the affiliations #######")

        for affiliation, corpus in self.affiliations_dict.items():
            # Find the current affiliation in the master list
            word_dist = nltk.FreqDist(self.affiliations_stopped_corpus[affiliation])
            top = word_dist.most_common(10)
            research_interests = ""
            for term in top:
                research_interests += str(term[0]) + ", "
            research_interests = research_interests[:-2]  # remove two final chars
            print(affiliation + ": " + research_interests)

    def analyze_affiliation_topics(self):
        if self._nbr_affiliations > 1:
            tf_vec = CountVectorizer(stop_words=self.tailored_stop_words)
            #tfidf_vec = TfidfVectorizer(stop_words=self.tailored_stop_words)

            # TF and TFIDF
            tf = tf_vec.fit_transform(self.affiliations_dict)
            tf_feature_names = tf_vec.get_feature_names()
            #tfidf = tfidf_vec.fit_transform(self.affiliations_stopped_corpus)
            #tfidf_feature_names = tfidf_vec.get_feature_names()

            nbr_topics = 8
            nbr_words = 7

            # LDA
            lda = LDA(n_components=nbr_topics)
            lda.fit(tf)

            # NMF
            #nmf = NMF(n_components=nbr_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)

            print("\n### LDA topics ###")
            self.display_topics(lda, tf_feature_names, nbr_words)
            #print("\n### NMF topics ###")
            #self.display_topics(nmf, tfidf_feature_names, nbr_words)
        else:
            print("Only one affiliation, skipping topic analysis.")
       
    def display_topics(self, model, feature_names, no_top_words):
        for topic_idx, topic in enumerate(model.components_):
            print("Topic %d:" % (topic_idx))
            print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
 