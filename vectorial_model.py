import json
from clustering import clustering
from document_processing import document_processing
from query_expansion import query_expansion
from query_processing import query_processing


class vectorial_model():

    path = ''
    query = ''

    def __init__(self, path, query, umbral):
        self.path = path
        self.query = query
        self.umbral = umbral
    
    def _getResults(self):
        # se pasa el path (en el futuro cualquiera) para el procesamiento de documentos
        json_value = json.dumps({'path': self.path})

        document_processing(json_value)

        # expansion de consulta
        json_value = json.dumps({'query': self.query})
        expanded_query = query_expansion(json_value)

        # procesamiento de consulta y devolucion de resultados
        json_value = json.dumps({'action': 'query', 'query': expanded_query, 'umbral': self.umbral})
        json_result = json.loads(query_processing(json_value))

        return json_result