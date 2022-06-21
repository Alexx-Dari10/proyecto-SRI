from decimal import DivisionByZero
import glob
import json
import os
from document_processing import document_processing
from query_expansion import query_expansion
from query_processing import query_processing

def main():
    path = os.getcwd() + '/collections/prueba_cran'
    #path = os.getcwd() + '/collections/prueba_med'

    json_value = json.dumps({'path': path})
    document_processing(json_value)

    queries = open(os.getcwd() + '/collections/prueba_cran/cranquery.txt','r')

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
            json_value = json.dumps({'query': query})
            expanded_query = query_expansion(json_value)
            json_value = json.dumps({'action': 'query', 'query': expanded_query, 'umbral': 0.1})
            json_result = json.loads(query_processing(json_value))

            for pair in json_result['results']:
                if(len(r10) < 10):
                    r10.append(pair["document"])
                    
                file2 = open(os.getcwd() + '/collections/prueba_cran/cranqrel.txt','r')
                for j in file2:
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
        print("No documents recovered")


def recall (RR, REL):
    try:
        return RR/REL
    except (ZeroDivisionError):
        print("No documents recovered")


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
    return RR / R


def fallout (REC, REL, RR, TOTAL):
    return (REC-RR)/(TOTAL - REL) if (TOTAL - REL) != 0 else 0

main()