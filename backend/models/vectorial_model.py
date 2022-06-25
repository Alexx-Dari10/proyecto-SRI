import json
from ..documents.document_processing import document_processing
from ..query.query_expansion import query_expansion
from ..query.query_processing import query_processing


class vectorial_model():

    path = ''

    def __init__(self, path):
        self.path = path

        # se pasa el path (en el futuro cualquiera) para el procesamiento de documentos
        json_value = json.dumps({'path': self.path})
        document_processing(json_value)
    

    def _getResults(self, query, umbral):

        # expansion de consulta
        json_value = json.dumps({'query': query})
        expanded_query = query_expansion(json_value)

        # procesamiento de consulta y devolucion de resultados
        json_value = json.dumps({'action': 'query', 'query': expanded_query, 'umbral': umbral})
        json_result = json.loads(query_processing(json_value))

        return json_result