
from operator import mod
from flask import Flask, request, render_template,jsonify, redirect,url_for
import webbrowser

import os
import json
from boolean_model import boolean_model
from clustering import clustering
from vectorial_model import vectorial_model


# VARIABLES
_host = 'localhost'
_port = 3001

global _model, _collection
global clust_docs, doc_clust


# APP
app = Flask(__name__)


def initModel(model, collection):

    global clust_docs, doc_clust

    # los documentos deben estar en la carpeta docs del directorio del proyecto
    path = os.getcwd() + '/static/docs/' + collection

    # !!!!!!!!!!!!!!!!!!!!!!!!!!! NUMERO DE DOCUMENTOS A DEVOLVER (BOOLEANO) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    no_docs = 25

    # clustering 
    clust_docs, doc_clust, empty_collection = clustering(path)

    if model == 'vectorial':
        # modelo vectorial
        return vectorial_model(path),empty_collection
    
    elif model == 'booleano':
        # modelo booleano
        return boolean_model(path),empty_collection 
    else: 
        return '',empty_collection

def getDocsDir():
    base_dir = path = os.getcwd() + '/static/docs/'
    with os.scandir(base_dir) as files:
        subdirectories = [file.name for file in files if file.is_dir()]
        return subdirectories



def jsonResult(query):
    
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! CAMBIAR UMBRAL AQUI (VECTORIAL) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    umbral = 0.11
   
    json_result = _model._getResults(query, umbral)
    
    return json_result


# ROUTES
@app.route('/', methods=["GET"])
def home():

    return render_template('home.html', subdirectories=getDocsDir()) 


@app.route('/index', methods=["GET", "POST"])
def index():
    global _collection
    global _model
    
    
    if request.method == 'POST':
        model = request.form['model']
        collection = request.form['collection']

        
        _model,empty_collection = initModel(model, collection)

        if empty_collection:
            return render_template("error.html", msg="Selected collection is empty")
        _collection = collection

        
        return render_template('index.html')

    else:
        return render_template('index.html')


@app.route('/search', methods=["POST"])
def search():
    global clust_docs, doc_clust
    global _model
    global _collection

    query = request.form['query']
    results = jsonResult(query)['results']

    docs = []
    for i in range(0, len(results)): 
        docs.append(results[i]['document'])
    
    return render_template('search.html', docs=docs, collection=_collection, query=query, clust_docs=clust_docs, doc_clust=doc_clust)




@app.route('/cluster', methods=["POST"])
def cluster():
    topic = request.form['topic']
    docs_topic = clust_docs[topic]
    return render_template('clusters.html', topic=topic, docs=docs_topic, collection=_collection)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("pagina_no_encontrada.html"), 404


if __name__ == '__main__':
    webbrowser.open(f'http://{_host}:{_port}', new=2)

    # el debug en true es para poder recargar los cambios
    app.run(host=_host, port=_port, debug=False)
