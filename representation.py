from nltk import FreqDist
import math

def terms(doc, terms, data):
	freq = FreqDist(terms)
	max_freq = max(freq.values()if len(freq) > 0 else [0])

	for term in freq.keys():
		ntf = freq[term] / max_freq
		new_doc = {'tf': ntf,
				   'weight': 0}
		in_data = False
		for term_data in data:
			if term == term_data['key']:

				term_data['value']['documents'][doc] = new_doc
				in_data = True
				break

		if not in_data:
			data.append({'key': term,
						 'value': {'idf':0,
									'documents': {doc:new_doc}}})

def idf(data, N):
	for term in data:
		term['value']['idf'] = math.log10((N / len(term['value']['documents'])) + 1)

def w(data,a):
	for term in data:
		for doc in term['value']['documents'].keys():
			document = (doc,term['value']['documents'][doc])
			term['value']['documents'][doc]['weight'] = (a + (1 - a)* document[1]['tf']) * term['value']['idf']