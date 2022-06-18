from nltk.corpus import stopwords
from string import punctuation
from nltk import wordpunct_tokenize
import json
from nltk.corpus import wordnet


# expansion de consulta usando sus sinonimos
def query_expansion(json_request):
    data = json.loads(json_request)
    return data['query'] + " " + query_synonyms(data['query'])
    

# por cada termino de la consulta, esta se expande con algunos sinonimos
def query_synonyms(data):
    _stopwords = stopwords.words('english')
    symbols = list(punctuation)
    tokens = [item for item in wordpunct_tokenize(data) if (item not in _stopwords + symbols)]

    words = []
    synonyms = []
    for token in tokens:
        for syn in wordnet.synsets(token):
            for lm in syn.lemmas():
                synonyms.append(lm.name())

        synonyms = (set(synonyms))
        words.extend(list(synonyms)[:5])
        synonyms = []

    return " ".join(words)