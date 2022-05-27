
import requests
import random
import json
import socket
import subprocess
import psutil
from subprocess import Popen, PIPE
from SPARQLWrapper import SPARQLWrapper
import profile, memory_profiler


def fuseki_control():
    """
    This function modified fuseki connection data
    :return: return nothing, open the script and edit the Data
    """
    script = open("script/fuseki_data_script.json",'r')
    jsonData = json.load(script)
    port = jsonData['port']
    ip = jsonData['ip']
    dataName = jsonData['dataName']
    current_Solution = 1
    memory = jsonData['memory']

    dic = {"datasetName":jsonData['datasetName'], "ip": ""+ip, "port": port, "dataName": ""+dataName, "memory":memory}
    with open("script/fuseki_data_script.json", 'w') as script:
        json.dump(dic, script)
        print("Fuseki data script updated")

def fusekiConnector():
    """
    Fuseki connector for connecting the server
    :return: False if the Server is running else return True after run the server
    """
    try:
       file = open("script/fuseki_data_script.json",'r')
       jsonData = json.load(file)
       with open("fuseki/fuseki-server.bat","w") as memoryUpdate:
           memoryUpdate.write("java -Xmx"+str(jsonData['memory'])+"200M -jar fuseki-server.jar %*")
       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       if sock.connect_ex((jsonData['ip'],jsonData['port'])) == 0:
           print("Terminating Fuseki Server in progress...")
           local__ = psutil.net_connections('inet')
           for c in local__:
               if c.laddr[1] == jsonData['port']:
                   px_ = c.pid
                   continue
           # Repaird Bug --
           #p = subprocess.Popen('terminate.bat', stdout=PIPE)
           #pid_ = ""
           #pid = p.stdout.read().split()[10]
           #for i in str(pid):
           #    if i.isdigit():
           #        pid_ += i
           #print("Fuseki listining in PID ", pid_)
           px = psutil.Process(int(px_))
           px.kill()
           print("Fuseki Terminated, rerun for start..")
           return False
       else:
           print("Open service Fuseki...")
           string_bilder = "echo 'Running fuseki server'\ncd fuseki\nfuseki-server --update --mem /" + jsonData['datasetName']
           file = open('fuseki_run_script.bat', 'w+')
           file.write(string_bilder)
           file.close()
           print("open Fuseki Port")
           subprocess.Popen('fuseki_run_script.bat')
           host = SPARQLWrapper('http://localhost:'+str(jsonData['port']) + '/' + str(jsonData['datasetName']))
           data = open(""+jsonData['dataName'], 'r', encoding='utf-8').read()
           headers = {'Content-Type': 'application/rdf+xml;charset=utf-8'}
           requests.post('http://localhost:'+str(jsonData['port']) + '/' + str(jsonData['datasetName']), data=data.encode('utf-8'), headers=headers)
           print("Fuseki server running on port ", jsonData['port'])
           print("Dataset",jsonData['datasetName']," has been created and the Data ",jsonData['dataName'], 'uploaded ' )
           return True
    except (psutil.AccessDenied):
        # in some cases cat't access the system. This line of code will run a script to force kill the fuseki server.
          print("Can't accssess process")
          p = subprocess.Popen('terminate.bat', stdout=PIPE)
          pid_ = ""
          pid = p.stdout.read().split()[10]
          for i in str(pid):
             if i.isdigit():
                  pid_ += i
             print("Fuseki listining in PID ", pid_)
          forceKiller = "taskkill /pid " + str(pid_) + " /f"
          fileKiller = open("forcekill.bat","w+")
          fileKiller.write(forceKiller)
          fileKiller.close()
          subprocess.Popen('forcekill.bat')
          #px = psutil.Process(int(px_))
          #px.kill()



def checkFusekiSocket():
    """
    This function check if the fuseki server socet is open. Using the Fuseki_Data_Script file to read the Data.
    :return: True if the Port open, else return False for closed port.
    """
    data_script = open("script/fuseki_data_script.json", 'r')
    load_data = json.load(data_script)
    fusekiSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_fuseki_open = fusekiSocket.connect_ex((load_data['ip'], load_data['port']))
    if is_fuseki_open == 0:
        return True
    else:
        return False
    fusekiSocket.close()



if __name__ == "__main__":
    # Feseki Control rebuld the Parameters of the Servieer
    # Fuseki connector connect run the server and upload the selected Graph
   fuseki_control()

   fusekiConnector()
