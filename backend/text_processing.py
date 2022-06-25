import re
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from string import punctuation

# preprocesamiento textual

def text_processing (analyze_json):
    data = json.loads(analyze_json)
    if data['action'] == 'process':
        terms = _processing(data['data'])
        return json.dumps({'terms': terms})

# - tokenizacion
# - normalizacion
# - lematizacion
# - eliminacion de stopwords
def _processing(data):

    match = re.search(r'([a-zA-z]+)', data)

    if len(data)==0 or not match:
        return []

    for (pattern, repl) in patterns:
        data = re.sub(pattern, repl, data)

    tokens = word_tokenize(data)
    tokens = [element for element in tokens if (element not in _stopwords and element not in no_words)]

    stems = SnowballStemmer('english') 
    tokens_stem = [stems.stem(token) for token in tokens]

    return tokens_stem


_stopwords = stopwords.words('english')
no_words = list(punctuation)
patterns = [ (r'(\w+)\'re', '\g<1> are'),
            (r'(\w+)\'em', '\g<1> them'),
            (r'[nN]\'t', 'not'),
            (r'[wW]on\'t', 'will not'),
            (r'[cC]an\'t', 'can not'),
            (r'(\w+)\'ll', '\g<1> will'),
            (r'(\w+)n\'t', '\g<1> not'),
            (r'[iI]\'m', 'i am'),
            (r'[aA]in\'t', 'is not'),
            (r'[iI]t\'s', 'it is'),
            (r'(\w+)\'ve', '\g<1> have'),
            (r'(\w+)\'s', '\g<1>'),
            (r'\'m', 'am'),
            (r'\'s', 'is'),
            (r'\'ll', 'will'),
            (r'\'ve', 'have'),
            (r'\'re', 'are')]