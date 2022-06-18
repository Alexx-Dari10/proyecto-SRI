import os
import json
from document_processing import document_processing
from query_processing import query_processing
from query_expansion import query_expansion

# los documentos deben estar en la carpeta docs del directorio del proyecto
path = os.getcwd() + '/docs'

# se pasa el path (en el futuro cualquiera) para el procesamiento de documentos
json_value = json.dumps({'path': path})
document_processing(json_value)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! INSERTAR CONSULTA AQUI !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
query = 'what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft .'


# expansion de consulta
json_value = json.dumps({'query': query})
expanded_query = query_expansion(json_value)


# procesamiento de consulta y devolucion de resultados
# !!!!!!!!!!!!!!!!!! CAMBIAR UMBRAL AQUI !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
json_value = json.dumps({'action': 'query', 'query': expanded_query, 'umbral': 0.1})
json_result = json.loads(query_processing(json_value))


# pintar resultados en consola
print(f"query: {query}")
print ("-------------RESULTS------------")
for i, _result in enumerate (json_result['results']):
    print(f"{i+1} -- {_result['document']}, value: {_result['value']}")