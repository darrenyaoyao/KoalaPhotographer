import sys
import re
import nltk
import json
import codecs
import operator
from gensim import corpora, models, similarities

#load the dictionary and corpus
dictionary = corpora.Dictionary.load('database.dict')
corpus = corpora.MmCorpus('database.mm')

# define a multi-dimensional LSI space
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=400)
# transform corpus to LSI space and index it
index = similarities.MatrixSimilarity(lsi[corpus])
index.save('database.index')
index = similarities.MatrixSimilarity.load('database.index')

# read the document entities
entities = []
with codecs.open('../Project1_data/DBdoc.json', 'rb', encoding='utf-8') as db:
    db_json = json.load(db)
    for line in db_json:
        entities.append(line['entity'].encode('utf-8'))

inputQueryFileName = sys.argv[1]
with open(inputQueryFileName) as completeQueries:
    for queryLine in completeQueries:
        query = re.split(r"\t",queryLine)
        # tokenize the query
        queryKey, queryContent = query[0], ' '.join(nltk.word_tokenize(query[1])).lower()

        vec_bow = dictionary.doc2bow(queryContent.lower().split()) 
        # convert the query to LSI space
        vec_lsi = lsi[vec_bow]
        # perform a similarity query against the corpus
        sims = index[vec_lsi]

        # sort the result by score
        sims = sorted(enumerate(sims), key=lambda item: item[1])

        # for those score<0, set to zero
        result_sims = [] 
        for sim in sims:
            if sim[1] >= 0:
                result_sims.append(sim)
            else:
                result_sims.append(tuple([sim[0],0]))
                
        maxRank = len(result_sims)
        maxScore = result_sims[maxRank-1][1]
        minScore = 0
        rangeScore = maxScore-minScore

        rank = maxRank
        for sim in result_sims:
            # scale the score from 0-2
            score = (sim[1]-minScore)/rangeScore*2
            # print the result
            resultLine = ('%s\t%s\t<dbpedia:%s>\t%d\t%f\t%s') % (queryKey, 'Q0', entities[sim[0]], rank, score, 'STANDARD')
            print resultLine
            rank -= 1


