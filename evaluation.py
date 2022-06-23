from decimal import DivisionByZero
import glob
import os

from boolean_model import boolean_model
from vectorial_model import vectorial_model

def evaluation(path, queries, model, result_file):

    _model = model(path)

    # cambiar umbral y numero de documentos aqui
    limit = 30 if model is boolean_model else 0.1

    _precision = 0
    _recall = 0
    _fMeasure = 0
    _f1Measure = 0
    _rPrecision = 0
    _fallout = 0

    count = 1
    for query in queries:
        rr = []
        rel = []
        r10 = []
        rr10 = []

        if query != '\n':
            json_result = _model._getResults(query, limit)

            for pair in json_result['results']:
                if(len(r10) < 10):
                    r10.append(pair["document"])
                    
                for j in result_file:
                    b =''
                    t = 1
                    for i in j:
                        if i ==' ':
                            break
                        b+=i
                        t+=1
                    if (str(count) == str(b)):
                        a =''
                        for i in j[t:]:
                            if i ==' ':
                                break
                            a+=i
                        rel.append(a)
                        if (pair["document"] == (str(a) + ".txt")):
                            if (len(r10) < 10):
                                rr10.append(a)
                            rr.append(a)
            if len(json_result['results']) >= 1:
                
                count += 1
                _precision += precision(len(rr),len(json_result['results']))
                _recall += recall(len(rr),len(rel)/len(json_result['results']))
                _fMeasure += measure_f(len(rr),len(json_result['results']),len(rel)/len(json_result['results']),0)
                _f1Measure += measure_f1(len(rr),len(json_result['results']),len(rel)/len(json_result['results']))
                _rPrecision += r_precision(len(rr10),10)
                _fallout += fallout(len(json_result['results']),len(rel)/len(json_result['results']),len(rr),len(glob.glob(os.path.join(path, "*.txt"), recursive=True)))
            
        

    print('Precision Average: ' + str(_precision/(count-1)))
    print('Recall Average: ' + str(_recall/(count-1)))
    print('F (beta = 0) Average: ' + str(_fMeasure/(count-1)))
    print('F1 Average: ' + str(_f1Measure/(count-1)))
    print('R-precision Average: ' + str(_rPrecision/(count-1)))
    print('Fallout Average: ' + str(_fallout/(count-1)))





def precision(RR, REC):
    try:
        return RR/REC
    except (ZeroDivisionError):
        return 0


def recall (RR, REL):
    try:
        return RR/REL
    except (ZeroDivisionError):
        return 0


def measure_f (RR, REC, REL, beta):
    P = precision(RR, REC)
    R = recall(RR, REL)
    if(((beta**2)*P) + R) != 0:
        return ((1+ beta**2)*P*R) / (((beta**2)*P) + R)
    return 0
       

def measure_f1 (RR, REC, REL):
    P = precision(RR, REC)
    R = recall(RR, REL)
    if (P + R) != 0:
        return 2*P*R / (P + R)
    return 0


def r_precision (RR, R):
    return RR / R if R != 0 else 0


def fallout (REC, REL, RR, TOTAL):
    return (REC-RR)/(TOTAL - REL) if (TOTAL - REL) != 0 else 0


def main():


    path_cran = os.getcwd() + '/collections/prueba_cran/cran'
    path_med = os.getcwd() + '/collections/prueba_med/med'

    queries_cran = open(os.getcwd() + '/collections/prueba_cran/cranquery.txt','r')
    queries_med = open(os.getcwd() + '/collections/prueba_med/medquery.txt','r')

    resultFile_cran = open(os.getcwd() + '/collections/prueba_cran/cranqrel.txt','r')
    resultFile_med = open(os.getcwd() + '/collections/prueba_med/medqrel.txt','r')




    print("=========================== PRUEBA DE CRANFIELD ============================================")
    print("--------------------------- Modelo Booleano --------------------------------------------")
    evaluation(path_cran, queries_cran, boolean_model, resultFile_cran)
    print('\n\n')

    print("--------------------------- Modelo Vectorial --------------------------------------------")
    evaluation(path_cran, queries_cran, vectorial_model, resultFile_cran)
    print("===============================================================================================\n\n")


    print("=========================== PRUEBA DE MEDLINE =================================================")
    print("--------------------------- Modelo Booleano -----------------------------------------------")
    evaluation(path_med, queries_med, boolean_model, resultFile_med)
    print('\n\n')

    print("--------------------------- Modelo Vectorial --------------------------------------------")
    evaluation(path_med, queries_med, vectorial_model, resultFile_med)

main()