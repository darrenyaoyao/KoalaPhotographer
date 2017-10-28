#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 20:03:56 2017

@author: Yao
"""

import math
from util import dataloader

"""
Okapi_BM25:https://en.wikipedia.org/wiki/Okapi_BM25
"""

class BM25():
    def __init__(self, database):
        self.documentsTotal = len(database)
        self.averageDocumentLength = float(sum([len(abstract) for _,abstract in database.items()])/self.documentsTotal)
        self.database = database
        self.termFrequency = {}
        self.inverseDocumentFrequency = {}
        self.documentFrequency = {}
        self.K1 = 1.2
        self.B = 0.8
        self.init()
        
    def init(self):
        for entity,abstract in self.database.items():
            self.termFrequency[entity] = {}
            for word in abstract:
                self.termFrequency[entity][word] = self.termFrequency[entity].get(word, 0)+1
            for word in self.termFrequency[entity]:
                self.documentFrequency[word] = self.documentFrequency.get(word, 0)+1
        for word, documentFrequency in self.documentFrequency.items():
            inverseDocumentFrequency = math.log(self.documentsTotal-documentFrequency+0.5)-math.log(documentFrequency+0.5)
            self.inverseDocumentFrequency[word] = inverseDocumentFrequency

    def simility(self, query, entity):
        score = 0.0
        for word in query:
            if word in self.termFrequency[entity]:
                abstractLength = len(self.database[entity])
                score += (self.inverseDocumentFrequency[word]*self.termFrequency[entity][word]*(self.K1+1)/(self.termFrequency[entity][word]+self.K1*(1-self.B+self.B*abstractLength/self.averageDocumentLength)))
        return score
        
def main(inputDatabaseFileName, inputQueryFileName):
    load = dataloader.init(inputDatabaseFileName, inputQueryFileName)
    queries = load.getQueries()
    database = load.getDatabase()
    bm25 = BM25(database)
    with open("result.txt", "w") as outputFile:
        for queryKey, queryContent in queries.items():
            similities = {}
            for entity in database:
                simility = bm25.simility(queryContent, entity)
                if simility > 0:
                    similities[entity] = simility
            if len(similities)>0:
                maxSimility = max(similities.values())
                for entity in similities:
                    relevence = similities[entity]/maxSimility*2
                    outputFile.write("%s Q0\t<dbpedia:%s>\t%f\n" % (queryKey, entity, relevence))

if __name__ == "__main__":
    main(r"DBdoc.json", r"queries-v2.txt")