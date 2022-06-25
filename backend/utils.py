import json

dictionary ={}

# escoge que accion realizar
def action (json_request):
    json_data = json.loads(json_request)

    if json_data['action'] == 'create':
        _add(json_data['data'])
    elif json_data['action'] == 'get':
        return _get(json_data['key'])
    elif json_data['action'] == 'dict':
        return _dic()

# annade nuevos terminos
def _add(data):
    for elem in data:
        t = elem['key']
        value = elem['value']
        dictionary[t] = value

# devuelve el termino t si aparece
def _get(t):
    response = {}

    if t in dictionary:
        response['success'] = True
        response['value'] = dictionary[t]
    else:
        response['success'] = False
        response['value'] = None

    return json.dumps(response)


def _dic():
    return json.dumps(dictionary)