import os

from boolean_model import boolean_model
from clustering import clustering
from vectorial_model import vectorial_model

# los documentos deben estar en la carpeta docs del directorio del proyecto
path = os.getcwd() + '/docs'

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! INSERTAR CONSULTA AQUI !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
query = 'what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft .'

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! CAMBIAR UMBRAL AQUI (VECTORIAL) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
umbral = 0.1

# !!!!!!!!!!!!!!!!!!!!!!!!!!! NUMERO DE DOCUMENTOS A DEVOLVER (BOOLEANO) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
no_docs = 30


# clustering 
clust_docs, doc_clust = clustering(path, 5)

# modelo vectorial
_vectModel = vectorial_model(path, query, umbral)
vect_jsonResults = _vectModel._getResults()

# modelo booleano
_boolModel = boolean_model(path, query, no_docs)
bool_jsonResults = _boolModel._getResults()



# pintar resultados en consola
print(f"query: {query}")

print("----------------------MODELO VECTORIAL---------------------------------------")
print ("-------------RESULTS------------")
for i, _result in enumerate (vect_jsonResults['results']):
    print(f"{i+1} -- {_result['document']}, value: {_result['value']}")


print("----------------------MODELO BOOLEANO---------------------------------------")
print ("-------------RESULTS------------")
for i, _result in enumerate (bool_jsonResults['results']):
    print(f"{i+1} -- {_result['document']}, value: {_result['value']}")