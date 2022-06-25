import json
from text_processing import text_processing
from representation import *
from sim import sim

# envia la consulta para su procesamiento y devolucion de resultados
def query_processing(json_request):
	data = json.loads(json_request)
	return query(data['query'],data['umbral'])

# - preprocesamiento textual de la consulta
# - calculo del peso de cada termino en la consulta
# - calculo funcion de similitud para cada documento
# - devolucion de los documentos cuyo valor asociado sea mayor que un umbral predefinido
def query(query, umbral):
	json_process = json.dumps({'action': 'process', 'data': query})
	query_terms = json.loads(text_processing(json_process))['terms']
	query_data = []

	if not query_terms: return json.dumps({'results':[]})

	terms('query', query_terms, query_data)
	idf(query_data, 1)
	w(query_data, 0.5)

	dicc_ranking = sim(query_data, query_terms)

	result= list(zip(dicc_ranking.keys(), dicc_ranking.values()))
	result.sort(key=lambda x: x[1], reverse=True)
	
	return json.dumps({'results':[{'document':dc, 'value':val} for dc, val in result if val >= umbral]})
