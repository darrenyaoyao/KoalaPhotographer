import math


class SDM():
    def __init__(self, database, at=1, ao=0, au=0, smoothing=0.5):
        self.database = database
        self.at = at
        self.ao = ao
        self.au = au
        self.tf_dic = {}
        self.cf_dic = {}
        self.smoothing = smoothing
        self.collection_len = 0
        for key, value in self.database.items():
            self.collection_len += len(value)

    def __call__(self, query, entity):
        return self.FID_value(query, entity)

    def FID_value(self, query, entity):
        score = 0
        for q in query:
            term1 = (1-self.smoothing) * self.tf(q, self.database[entity])\
                / len(self.database[entity])
            term2 = self.smoothing * self.cf(q, self.database)\
                / self.collection_len
            score += self.at * math.log(term1+term2+1)
        return score

    def tf(self, query, document, unordered=False):
        # this function calculates the number of times term query occurs in the document
        num = 0
        if type(query) is list:
            l = len(query)
            for i in range(l, len(document)):
                ws = [w for w in document[:l]]
                if not unordered and query == ws:
                    num += 1
                elif unordered and set(query) == set(ws):
                    num += 1
        else:
            if query in self.tf_dic:
                num = self.tf_dic[query]
            else:
                for w in document:
                    if w == query:
                        num += 1
                self.tf_dic[query] = num
        return num

    def cf(self, query, database, unordered=False):
        # this function calculates the number of times term query occurs in the entire collection
        num_total = 0
        if query in self.cf_dic:
            num_total = self.cf_dic[query]
        else:
            for key, document in database.items():
                num = 0
                if type(query) is list:
                    l = len(query)
                    for i in range(l, len(document)):
                        ws = [w for w in document[:l]]
                        if not unordered and query == ws:
                            num += 1
                        elif unordered and set(query) == set(ws):
                            num += 1
                else:
                    if query in self.tf_dic:
                        num = self.tf_dic[query]
                    else:
                        for w in document:
                            if w == query:
                                num += 1
                        self.tf_dic[query] = num
                num_total += num
            self.cf_dic[query] = num_total
        return num_total


