import math
import pandas 
import nltk
import re
import os
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def clustering(path):
    titles = []
    content = []
    
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for filename in files:
                with open(os.path.join(root,filename), encoding='utf8', errors='ignore') as f:
                    titles.append(filename)
                    content.append(f.read())   

    tfidf_vector = TfidfVectorizer(max_df=0.8, max_features=200000000, min_df=0.2, stop_words='english',use_idf=True,tokenizer=tokenize_stemmer,ngram_range=(1,3))
    tfidf_matrix = tfidf_vector.fit_transform(content)

 # metodo del codo
    i = -1
    inertia = []
    for num_clusters in range(1,len(titles)):
        kmeans = KMeans(n_clusters=num_clusters)
        kmeans.fit(tfidf_matrix)
        _sum = 0
        for d in kmeans.transform(tfidf_matrix):
            _sum += min(d)**2
        
        inertia.append(_sum)
        
        if len(inertia) > 1:
            if math.fabs(inertia[i+1] - inertia[i]) < 15:
                break        
        
        i+=1
        
    # analisis y devolucion de resultados
    clusters = kmeans.labels_.tolist()

    docs =  {    
            'title' : titles, 
            'text' : content,
            'cluster': None
            }
    frame = pandas.DataFrame(docs,index=[clusters],columns=['title','cluster'])
    frame['cluster'].value_counts()

    doc_clust = {}
    clust_docs = {}

    for i in range(num_clusters):
        doc_list = []
        
        _cluster = "Cluster" + str(i+1)
             
        for title in frame.loc[i]['title'].values.tolist():
            doc_list.append(title)
            doc_clust[title] = _cluster
        
        clust_docs[_cluster] = doc_list
        
    
    return clust_docs, doc_clust
    
    
def tokenize_stemmer(text):
    stemmer = SnowballStemmer("english")
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]',token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems