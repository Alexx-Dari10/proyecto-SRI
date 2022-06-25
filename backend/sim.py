import json
import math
from .utils import action

# calculo funcion de similitud, devuelve un ranking de los documentos
def sim(query_data, query_terms):
	docs = valid_docs (query_terms)
	dicc_ranking = {}

	_djq = djq(query_data, docs)
	_dj = dj()
	_q = q(query_data)['query']
	for doc in docs.keys():
		if doc not in dicc_ranking:
			dicc_ranking[doc] = (_djq[doc] / (_dj[doc]['w']*_q))
	return dicc_ranking

# documentos en los que aparecen terminos de la consulta
def valid_docs(query_terms):
	docs = {}
	for term in query_terms:
		json_respons = json.loads(action(json.dumps({'action':'get', 'key':term})))
		if json_respons['success']:
			term_value = json_respons['value']
			for doc in term_value['documents'].keys():
				if doc not in docs:
					docs[doc] = {'terms': {term: 0}, 'weights': [term_value['documents'][doc]['weight']]}
				else:
					docs[doc]['terms'][term] = len(docs[doc]['weights'])
					docs[doc]['weights'].append(term_value['documents'][doc]['weight'])

	return docs


# __________________________________________________
# calculo auxiliar de la funcion de similitud 

def dj():
	docs = {}
	json_respons = json.loads(action(json.dumps({'action':'dict'})))
	for item in json_respons.keys():
		result = json_respons[item]
		for document in result['documents']:
			if document not in docs:
				docs[document] = {'w': (result['documents'][document]['weight'])**2}
			else:
				docs[document]['w'] += (result['documents'][document]['weight'])**2

	for item in docs:
		docs[item]['w'] = math.sqrt(docs[item]['w'])

	return docs

def q(query_data):
	query_w = {}
	for item in query_data:
		if 'query' not in query_w:
			query_w['query'] = (item['value']['documents']['query']['weight'])**2
		else:
			query_w['query'] += (item['value']['documents']['query']['weight'])**2
	query_w['query'] = math.sqrt(query_w['query'])
	return query_w

def djq(query_data, docs):
	dicc_ranking = {}
	for doc in docs.keys():
		for tm_query in query_data:
			if tm_query['key'] in docs[doc]['terms'].keys():

				weight_query = tm_query['value']['documents']['query']['weight']
				index_weight_data = docs[doc]['terms'][tm_query['key']]
				weight_data = docs[doc]['weights'][index_weight_data]
				if doc not in dicc_ranking:
					dicc_ranking[doc] = (weight_query * weight_data)
				else:
					dicc_ranking[doc] += weight_query * weight_data
					
	return dicc_ranking