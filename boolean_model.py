import glob
import json
import os

from document_processing import read
from query_expansion import query_expansion
from text_processing import text_processing


class boolean_model:

    path = []
    query = ''

    all_terms = set()
    docs_terms = {}

    docs_vectors = {}

    def __init__(self, path, query, number_ofDocs):
        self.path = path
        self.query = query
        self.number_ofDocs = number_ofDocs

    def start(self):
        self.process_docs()
        self.docs_boolRepresentation()

        processed_query = self.process_query()
        q_vector = self.query_vector(processed_query)

        _dict = self.sim(q_vector)
        results = list(zip(_dict.keys(), _dict.values()))
        results.sort(key=lambda x: x[1], reverse=True)

        return json.dumps({'results':[{'document':dc, 'value':val} for dc, val in results[:self.number_ofDocs]]})


    def get_terms(self): return list(self.all_terms)
    
    def process_docs(self):
        documents = glob.glob(os.path.join(self.path + "/**", "*.txt"), recursive=True)
        docs_text = [(doc_path, read(doc_path)) for doc_path in documents]
        
        for i in range(len(docs_text)):
            json_process = json.dumps({'action':'process', 'data': docs_text[i][1]})
            _terms = json.loads(text_processing(json_process))['terms']

            doc_name = os.path.basename(docs_text[i][0])
            self.docs_terms[doc_name] = _terms
            self.all_terms.update(_terms)
        
        self.all_terms = self.get_terms()
    

    def docs_boolRepresentation(self):
        bool_vector = []

        for i in (self.docs_terms):
            for j in self.all_terms:
    
                if j in self.docs_terms[i]:
                    bool_vector.append(1)
                else:
                    bool_vector.append(0)
    
            copy = bool_vector.copy()
            self.docs_vectors.update({i: copy})
    
            bool_vector.clear()
    

    def process_query(self):
        json_value = json.dumps({'query': self.query})
        expanded_query = query_expansion(json_value)

        json_process = json.dumps({'action': 'process', 'data': expanded_query})
        return json.loads(text_processing(json_process))['terms']
    

    def query_vector(self, query):
        qvect = []
    
        for i in self.all_terms:
    
            if i in query:
                qvect.append(1)
            else:
                qvect.append(0)
    
        return qvect
    

    def sim(self, q_vect):

        dictionary = {}
        count = 0
    
        term_Len = len(self.all_terms)
    
        for i in self.docs_vectors:
    
            for t in range(term_Len):
                if(q_vect[t] == self.docs_vectors[i][t] and q_vect[t]):
                    count += 1

            if count > 0:
                dictionary.update({i: count})

            count = 0
        
        return dictionary





path = os.getcwd() + '/docs'
query = 'what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft .'

a = boolean_model(path, query, 30)
docs = a.start()
docs