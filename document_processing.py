import json
import glob
import os
from text_processing import text_processing
from representation import *
from utils import action

# envia el path al metodo que procesa los documentos
def document_processing(json_request):
    data = json.loads(json_request)
    documents(data['path'])


#  - realiza preprocesamiento textual de cada documento
#  - calcula el peso ( w ) de cada termino en el documento
def documents(path):
	data = []
    
	documents = glob.glob(os.path.join(path + "/**", "*.txt"), recursive=True)
	docs_text = [(doc_path, read(doc_path)) for doc_path in documents]
	
	for i in range(len(docs_text)):
		json_process = json.dumps({'action':'process', 'data':docs_text[i][1]})
		_terms = json.loads(text_processing(json_process))['terms']

		docs_text[i] = (docs_text[i][0], _terms)
	
	for doc in docs_text:
		_terms = doc[1]
		doc_name = os.path.basename(doc[0])
		terms(doc_name, _terms, data)
        
	idf(data, len(documents))
	w(data,0)
	
	json_process = json.dumps({'action':'create', 'data':data})
	action(json_process)


def read(txt_path):
	with open(txt_path, "r", encoding="utf8", errors="ignore") as f:
		document = f.read()
		f.close()
		return document