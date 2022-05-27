
# Old Fusiki code PID Terminator
def fusekiConnector():
    """
    Fuseki connector for connecting the server
    :return: False if the Server is running else return True after run the server
    """
    file = open("script/fuseki_data_script.json",'r')
    jsonData = json.load(file)
    print("Socket Starting")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex((jsonData['ip'],jsonData['port'])) == 0:
        print("Terminating Fuseki Server in Process...")
        p = subprocess.Popen('terminate.bat', stdout=PIPE)
        out, err = p.communicate()
        print("Fuseki listening PID - ", str(out)[172:177]) # to be edit MUST
        LISTENING = str(out)[172:177] #                       to be edit MUST
        substring = ""
        for i in LISTENING:
            if i == "\\" or i == "\\\\":
                pass
            else:
                substring += i
        digit = ""
        for j in substring:
            if j.isdigit():
                digit+=j
        if digit == '':
            print("Fuseki PID not Found, server can't be Terminated!")
        px = psutil.Process(int(digit))
        px.kill()
        print("Fuseki Terminated, rerun for start..")
        return False
    else:
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


#New Function of Fuseki server

file = open("script/fuseki_data_script.json", 'r')
jsonData = json.load(file)
print("Socket Starting")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if sock.connect_ex((jsonData['ip'], jsonData['port'])) == 0:
    print("Terminating Fuseki Server in Process...")
    p = subprocess.Popen('terminate.bat', stdout=PIPE)
    pid_ = ""
    pid = p.stdout.read().split()[10]
    for i in str(pid):
        if i.isdigit():
            pid_+= i

    pid_ = int(pid_)
    print(pid_)

   # print("PID ", p.stdout.read().split()[10])
    #print("PID ", p.stdout.read().decode().splitlines()[2])

    out, err = p.communicate()
    print("Fuseki listening PID - ", str(out)[172:177])  # to be edit MUST
    print(out)
    LISTENING = str(out)[172:177]  # to be edit MUST
    substring = ""
