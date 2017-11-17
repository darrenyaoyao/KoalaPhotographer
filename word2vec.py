#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import json
import nltk
import sys
from gensim import corpora
from collections import defaultdict

#open the database file
fileName = sys.argv[1]
with codecs.open(fileName, 'rb', encoding='utf-8') as db:
    db_json = json.load(db)
    documents = []
    entities = []
    #load json file and store into document list
    for line in db_json:
        entities.append(line['entity'])
        if line['abstract'] != None:
            documents.append(line['abstract'][1:-1])
        else:
            documents.append("")

    
    # remove common words and tokenize each document
    stoplist = set('for a of the and to in . , ( )'.split())
    for document in documents:
        sent_list = []
        for sentence in nltk.sent_tokenize(document):
            sent_list.append(' '.join(nltk.word_tokenize(sentence)).lower())
        document=' '.join(sent_list)

    texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

    # remove words that appear only once
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    
    texts = [[token for token in text if frequency[token] > 1] for text in texts]
    
    dictionary = corpora.Dictionary(texts)
    # store the dictionary
    dictionary.save('database.dict')
    print(dictionary)

    corpus = [dictionary.doc2bow(text) for text in texts]
    # store for later use
    corpora.MmCorpus.serialize('database.mm', corpus)
    print(corpus)
