import subprocess

from SPARQLWrapper import SPARQLWrapper, JSON
import json, time, memory_profiler, testQuery as BQ, pandas as pd
import socket, fuseki
from subprocess import Popen
import readAndSeperate as data
import testQuery

PREFIX = '''PREFIX nm: <http://nomisma.org/id/>
PREFIX nmo: <http://nomisma.org/ontology#>
PREFIX void: <http://rdfs.org/ns/void#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bio: <http://purl.org/vocab/bio/0.1/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX dcmitype: <http://purl.org/dc/dcmitype/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX org: <http://www.w3.org/ns/org#>
PREFIX osgeo: <http://data.ordnancesurvey.co.uk/ontology/geometry/>
PREFIX rdac: <http://www.rdaregistry.info/Elements/c/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX spatial: <http://jena.apache.org/spatial#> 
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dcterm: <http://purl.org/dc/terms/> 
PREFIX un: <http://www.owl-ontologies.com/Ontology1181490123.owl>
PREFIX bmo: <http://collection.britishmuseum.org/id/ontology/>
PREFIX amt: <http://academic-meta-tool.xyz/vocab#> 
PREFIX loc: <http://localhost:3030>
PREFIX crminf:<http://www.ics.forth.gr/isl/CRMinf/>
PREFIX edtfo:< https://periodo.github.io/edtf-ontology/edtfo.ttl>'''


def generic_query():
    return PREFIX + '''SELECT ?s WHERE {?s nmo:hasMint nm:comama. } '''

def S2Q1():
    return PREFIX + '''SELECT ?s WHERE {?s nmo:hasMint nm:comama. } '''

def queryRetrival(S,Q):
    return eval("BQ.S"+str(S) + "Q"+str(Q))




@memory_profiler.profile()
def manualTest(s,q):

    file = open("script/fuseki_data_script.json",'r')
    jsonData = json.load(file)
    print("Connectd to ",'http://localhost:'+str(jsonData['port']) + '/' + jsonData['datasetName'])
    host = SPARQLWrapper('http://localhost:'+str(jsonData['port'])+'/'+jsonData['datasetName'])
    host.setQuery(queryRetrival(s,q))
    host.setReturnFormat(JSON)
    print("Download data...")
    data = host.query().convert()

    headers = []
    string_line = ""
    for header in data['head']['vars']:
        headers.append(header)

    """ for i in headers:
        string_line = string_line + "'" + str(i) + ": ', result['" + str(i) + "']['value']" + ","
    print(string_line)

    string_line[:-1]
    for result in data['results']['bindings']:
        print(eval(string_line))"""


#@memory_profiler.profile()
def getData(S,Q):

    file = open("script/fuseki_data_script.json",'r')
    jsonData = json.load(file)
    print("Connectd to ",'http://localhost:'+str(jsonData['port']) + '/' + jsonData['datasetName'])
    host = SPARQLWrapper('http://localhost:'+str(jsonData['port'])+'/'+jsonData['datasetName'])
    host.setQuery(queryRetrival(S,Q))
    host.setReturnFormat(JSON)
    print("Download data...")
    queryResult = host.query().convert()
    #print(data)

    headers = []
    string_line = ""
    for header in queryResult['head']['vars']:
        headers.append(header)

    for i in headers:
        string_line = string_line + "'" + str(i) + ": ', result['" + str(i) + "']['value']" + ","
    #print(string_line)

    string_line[:-1]
    resultList = []
    '''for result in data['results']['bindings']:
        print(eval(string_line))
        resultList.append(eval(string_line))'''

    '''for result in data['results']['bindings']:
        print(result)'''
    return queryResult


def dynmaicTest():
    """
    This function run a test for all the queries in the class testQuery for all 8 Solutions.
    :return: Write the result of the test for each solution in the benchmark directory.
    """
    sum =0
    timeList = []
    sum_list = []
    all_list = []
    median_list = []
    connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    check_socket = connect_socket.connect_ex(("localhost",3030))
    # Updating the server
    for s in range(1,9):
        time.sleep(3)
        file = open("script/fuseki_data_script.json")
        jsonData = json.load(file)
        jsonData['dataName'] = "rdf/modelGraphDynamic_G"+str(s)+".rdf"
        dic = {"datasetName": jsonData['datasetName'], "ip": jsonData['ip'], "port": jsonData['port'], "dataName": jsonData['dataName'], "memory":jsonData['memory']}
        with open("script/fuseki_data_script.json", 'w') as script:
            json.dump(dic, script)

        if check_socket == 0:
           print("Server running")
        else:
            print("Port is closed")
            fuseki.fusekiConnector()
            time.sleep(5)
        for q in range(1,6):
            for loop in range(1,6):
                print("Running Solution ", s , " Query ", q , " for the", loop , " time.")
                time.sleep(2)
                start = time.time()
                getData(s,q)
                end = time.time() - start
                sum += end
                timeList.append(round(end,2))
            all_list.append(timeList)
            sum_list.append(round(sum / 5,2))
            median_list.append(sorted(timeList)[2])
            sum = 0
            timeList = []
            print("median", median_list)
        print(all_list)
        dataframe = pd.DataFrame([all_list, sum_list,median_list]).T
        dataframe.to_excel(excel_writer="benchmark/S"+str(s)+"_Result.xlsx",header=["Time per Run for S"+str(s), "Average Time", "Median"], index=True)
        sum_list = []
        all_list = []
        median_list = []
        fuseki.fusekiConnector()
        time.sleep(5)
    pass
#@memory_profiler.profile()
def graphviz_creator(graph):
    """

    :param graph:
    :return:
    """
    print("Selected GGG",graph)
    from static_data import prefixMerg
    connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    check_socket = connect_socket.connect_ex(("localhost",data.getFusekiPort()))
    file = open("script/fuseki_data_script.json")
    jsonData = json.load(file)
    jsonData['dataName'] = "rdf/modelGraphDynamic_G" + str(graph) + ".rdf"
    dic = {"datasetName": jsonData['datasetName'], "ip": jsonData['ip'], "port": jsonData['port'],
           "dataName": jsonData['dataName'],"memory":jsonData['memory']}
    with open("script/fuseki_data_script.json", 'w') as script:
        json.dump(dic, script)

    if check_socket == 0:
        print("Server running")
        fuseki.fusekiConnector()
        time.sleep(5)
        fuseki.fusekiConnector()
        time.sleep(5)
    else:
        print("Port is closed")
        fuseki.fusekiConnector()
        time.sleep(5)



    queryResult = getData(graph,0)
    headers = []
    string_line = ""
    for header in queryResult['head']['vars']:
        headers.append(header)
    #print(headers)
    for i in headers:
        string_line = string_line + "'" + str(i) + ": ', result['" + str(i) + "']['value']" + ","
    # print(string_line)

    string_line[:-1]
    resultList = []
    headerList = ['s', 'p','o']
    #print('o'==headerList[-1])
    sub_sec = ""
    gBuild = "" +"digraph G { \nlabel="+'"''Solution Graph'+""+'"'+";\n"
    for result in queryResult['results']['bindings']:
        print(result['s']['value'], "  ", result['p']['value'], "  ", result['o']['value'])
        gBuild+= '"'+ prefixMerg(result['s']['value']) +'" -> "' + prefixMerg(result['o']['value']) +'" [label="' + prefixMerg(result['p']['value'])+'"];\n'
    gBuild+="}"
    #print(gBuild)
    #print(gBuild)
    file = open("graph/graph.dot",'w', encoding="utf-8")
    file.write(gBuild)
    file.close()
    Popen('graphiz_generate_script.bat')
    time.sleep(3)

    '''for result in data['results']['bindings']:
        print(result)'''
# TO BE DYNAMIC -----
    pass


def UIQuery():
    data = getData(0,0)
    resultArray = []
    for i in data['results']['bindings']:
        resultArray.append([i['s']['value'],i['p']['value'],i['o']['value']])
    print(resultArray)
    return resultArray


if __name__ == "__main__":
    #UIQuery()
    #graphviz_creator(1)
    #fuseki.fusekiConnector()
    dynmaicTest()
    #start = time.time()
    #(8,5)
    #end = time.time() - start
    #print("Deploy Time is: ", end)
    #print(" Run time ==", round(time.time() - start,3))
    #egtData(1,1)
    pass
