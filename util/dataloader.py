#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 20:17:01 2017

@author: Auk
"""
import re
import json


class init():
    def __init__(self, inputDatabaseFileName, inputQueryFileName):
        self.queries = {}
        self.database = {}
        self.rawDatabase = {}
        with open(inputQueryFileName) as completeQueries:
            for queryLine in completeQueries:
                query = re.split(r"\t",queryLine)
                queryKey, queryContent = query[0], query[1].split()
                self.queries[queryKey] = queryContent
        with open(inputDatabaseFileName) as databaseFile:
            self.rawDatabase = json.load(databaseFile)
            for dataLine in self.rawDatabase:
                dataAbstract = dataLine["abstract"].split() if isinstance(dataLine["abstract"],str) else []
                self.database[dataLine["entity"]] = dataAbstract
                
    def getDatabase(self):
        return self.database
    
    def getQueries(self):
        return self.queries
    
    def getRawDatabase(self):
        return self.rawDatabase