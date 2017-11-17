# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 20:03:56 2017

@author: Yao
"""
from operator import itemgetter
from utils.dataloader import DBdocDataloader
from BM25.model import BM25

def main(inputDatabaseFileName, inputQueryFileName):
    # parse data in queries-v2.txt and DBdoc.json
    load = DBdocDataloader(inputDatabaseFileName, inputQueryFileName)
    queries = load.getQueries()
    database = load.getDatabase()
    # initailize BM25 environment
    bm25 = BM25(database)
    with open("result.txt", "w", encoding='UTF-8') as outputFile:
        for queryKey, queryContent in queries.items():
            similities = []
            for entity in database:
                # get simility score of each query and document
                simility = bm25.simility(queryContent, entity)
                # if score > 0 save it otherwise drop it
                if simility > 0:
                    similities.append((entity, simility))
            if len(similities) > 0:
                # max score in current query round
                maxSimility = max(similities, key=itemgetter(1))[1]
                # sort all score in current query round
                similities = sorted(similities, key=itemgetter(1))
                # num of all scores
                similitiesLength = len(similities)
                index = 0
                for simility in similities:
                    # normalize all score to 0~2
                    relevence = simility[1]/maxSimility*2
                    # document entity name
                    entity = simility[0]
                    # document rank
                    rank = similitiesLength-index
                    # write into "result.txt"
                    outputFile.write("%s\tQ0\t<dbpedia:%s>\t%d\t%f\tSTANDARD\n" % (queryKey, entity, rank, relevence))
                    index = index+1

if __name__ == "__main__":
    main(r"DBdoc.json", r"queries-v2.txt")
