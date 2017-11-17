from utils.dataloader import DBdocDataloader
from SDM.model import SDM
from tqdm import tqdm
import math

dataloader = DBdocDataloader('DBdoc.json', 'queries-v2.txt')
model = SDM(dataloader.getDatabase())
queries = dataloader.getQueries()
database = dataloader.getDatabase()
min_score = math.log(1)
max_score = 0

results = {}

print(len(queries))
print(len(database))

q_list = []

training_data = []
for _, q in queries.items():
    if q in q_list:
        print(q)
        print("Double")
    else:
        q_list.append(q)
    for entity, _ in database.items():
        training_data.append((q, entity))

for data in tqdm(training_data):
        query = data[0]
        entity = data[1]
        score = model(query, entity)
        if score > max_score:
            max_score = score
        if score > min_score:
            q = ', '.join(query)
            if q in results:
                results[q].append((query, entity, score-min_score))
            else:
                results[q] = [(query, entity, score-min_score)]


def get_key(element):
    return element[2]


def get_query_id(query, queries):
    for k, v in queries.items():
        if v == query:
            return k


for query in results:
    results[query] = sorted(results[query], key=get_key)
    results[query] = [(get_query_id(r[0], queries), r[1], r[2]*2/max_score) for r in results[query]]

with open('result.txt', 'w') as f:
    for q in results:
        for index, element in enumerate(results[q]):
            f.write(element[0]+'\t'+'Q0'+'\t'+'<dbpedia:'+element[1]+'>'+'\t' +
                    str(len(results[q])-index)+'\t'+str(element[2])[:6]+'\tSTANDARD\n')
