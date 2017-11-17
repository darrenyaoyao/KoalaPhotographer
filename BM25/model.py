# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 20:03:56 2017

@author: Yao
"""
import math

class BM25():
    """
    Okapi_BM25:https://en.wikipedia.org/wiki/Okapi_BM25
    """
    def __init__(self, database):
        """
        BM25 model variable

        @documentsTotal: num of documents in DBdoc.json
        @averageDocumentLength: average length of document in index terms in DBdoc.json
        @database: parsed content of DBdoc.json
        @termFrequency: frequency of every index term in DBdoc.json
        @documentFrequency: document frequency of the index term
        @inverseDocumentFrequency: inverse document frequency of every index term. IDF formula: log(([num of documents]-[document frequency of the index term]+0.5)/[num of documents]) 
        @K1: free parameter of BM25 ranking function
        @B: free parameter of BM25 ranking function
        """
        self.documentsTotal = len(database)
        self.averageDocumentLength = float(sum([len(abstract) for _, abstract in database.items()])/self.documentsTotal)
        self.database = database
        self.termFrequency = {}
        self.documentFrequency = {}
        self.inverseDocumentFrequency = {}
        self.K1 = 1.2
        self.B = 0.75
        # initialize all variable
        self.init()

    def init(self):
        """
        initialize all variable
        """
        for entity, abstract in self.database.items():
            self.termFrequency[entity] = {}
            for word in abstract:
                self.termFrequency[entity][word] = self.termFrequency[entity].get(word, 0)+1
            for word in self.termFrequency[entity]:
                self.documentFrequency[word] = self.documentFrequency.get(word, 0)+1
        for word, documentFrequency in self.documentFrequency.items():
            inverseDocumentFrequency = math.log(self.documentsTotal-documentFrequency+0.5)-math.log(documentFrequency+0.5)
            self.inverseDocumentFrequency[word] = inverseDocumentFrequency

    def simility(self, query, entity):
        """
        simility score of BM25

        ranking function: sum of [IDF of index term]*[term frequency of indexe term in the document D]*(K1+1)/([term frequency in the document D]+K1*(1-B+B*[length of the document in index terms]/[average length of document in index terms]))
        @abstractLength: length of the document in index terms
        """
        score = 0.0
        for word in query:
            if word in self.termFrequency[entity]:
                abstractLength = len(self.database[entity])
                score += (self.inverseDocumentFrequency[word]*self.termFrequency[entity][word]*(self.K1+1)/(self.termFrequency[entity][word]+self.K1*(1-self.B+self.B*abstractLength/self.averageDocumentLength)))
        return score
