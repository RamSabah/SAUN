#class for reading Files
import time

import pandas as pd
import json,csv
from pathlib import Path
import os.path

import Dynamic

def doseFileExists(path):
    return os.path.isfile(path)


def getFusekiPort():
    file = open("script/fuseki_data_script.json",'r')
    return json.load((open("script/fuseki_data_script.json",'r')))['port']

def getExportFormat():
    file = open("script/script.json", 'r')
    jsonData = json.load(file)
    if jsonData['exportFormat'] == "on":
        return ['ttl', 'turtle']
    return ['rdf','xml']

def getFilename():
    file = open("script/script.json", 'r')
    jsonData = json.load(file)
    return jsonData['filename']

def getExcelDirectory():
    file = open("script/script.json", 'r')
    dics = json.load(file)
    if 'xlsx' in str(dics['filename']):
        return "download/"+str(dics['filename'])


def convertor():
        path = "excel/"+str(getFilename())
        excelFile = pd.read_excel(r''+path)
        excelFile.to_csv(r'csv/'+str(getFilename()).replace('xlsx','csv'),index=None,header=True,encoding='utf-8')
        print("File converted, Conv1")


def convertor_2():
    path = "readyToRun/" + str(getFilename()).replace('csv','xlsx')
    excelFile = pd.read_excel(r'' + path)
    excelFile.to_csv(r'readyToRun/' + str(getFilename()).replace('xlsx', 'csv'), index=None, header=True, encoding='utf-8')
    print("File converted, Conv2")


def readCSV(direktory):
    try:
        file = open(direktory,'r',encoding='utf-8')
        return file
    except FileNotFoundError: print("Error reading csv file")


def getHeader():
    try:
        if doseFileExists('readyToRun/'+str(getFilename()).replace('xlsx','csv')):
           print(os.path.isfile('readyToRun/'+str(getFilename()).replace('xlsx','csv')))
           file = open("readyToRun/"+str(getFilename()).replace('xlsx','csv'),'r',encoding='utf-8')
           return csv.DictReader(file).fieldnames
    except: print("File not Found")


def getContent():
    try:
       file = open("readyToRun/"+str(getFilename()).replace('xlsx','csv'),'r',encoding='utf-8')
       c_file = csv.reader(file)
       next(c_file)
    except:print("File not found")
    return c_file



def seperateUncertainTable():
    #excelFile = pd.read_excel(r'excel/'+ getFilename())
    #excelFile.to_csv(r'csv/temporer.csv', index=None, header=True, encoding='utf-8')
    fileName_ = getFilename()
    if "xlsx" in str(fileName_):
        fileName_ = str(fileName_).replace('xlsx','csv')
    file = open(r'csv/'+ fileName_, encoding='utf-8')


    # print(csv.DictReader(file).fieldnames)
    headers = csv.DictReader(file).fieldnames

    data = csv.reader(file)
    # print(csv.DictReader(file.read()))
    certain_Headers_ = []
    uncertain_headers = []
    certain_Data = []
    uncertain_data = []
    healp_List = []
    dataHoalder = []
    # print(headers)

    for g in data:
        dataHoalder.append(g)

    for i in range(len(headers)):
        if 'http' in headers[i]:
            for z in dataHoalder:
                healp_List.append(z[i])
            certain_Headers_.append(headers[i])
            certain_Data.append(healp_List)
            healp_List = []

        else:
            for j in dataHoalder:
                healp_List.append(j[i])
            uncertain_headers.append(headers[i])
            uncertain_data.append(healp_List)
            healp_List = []

    certain_Data.insert(0, uncertain_data[0])
    certain_Headers_.insert(0, uncertain_headers[0])

    uncertain_headers.pop(0)
    uncertain_data.pop(0)
    #print(certain_Headers_)
    #print(certain_Data)
    #print("Reached This")

    certain = pd.DataFrame(certain_Data).T
    certain.to_excel(excel_writer="readyToRun/"+str(getFilename()).replace('csv','xlsx'), header=certain_Headers_, index=None, encoding='utf-8')
    uncertain = pd.DataFrame(uncertain_data).T
    uncertain.to_excel(excel_writer="readyToRun/uncertain_array.xlsx", header=uncertain_headers, index=None,
                       encoding='utf-8')
    print("Seperating finished")
    pass


#return current selected Graph
def selected_G():
    file = open("script/script.json",'r')
    jsonData = json.load(file)
    return jsonData['selectedGraph']



def check_excel():
    file = pd.read_excel("readyToRun/uncertain_array.xlsx")
    return file.empty


def runDataPreparation():
    fileExtension = str(getFilename())
    if "xlsx" in fileExtension:
       convertor()

    seperateUncertainTable()
    convertor_2()
    print("Converting Complete")
    pass

if __name__=='__main__':
    print(getFusekiPort())
    #print(getExportFormat())
    #convertor()
    #seperateUncertainTable()
    #convertor_2()
    #runDataPreparation()
    #print(selected_G())
