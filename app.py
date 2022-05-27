from flask import Flask, render_template, request, url_for, redirect, jsonify, send_file, send_from_directory
import json,os, time, subprocess, static_data as std
from subprocess import Popen, PIPE


import Dynamic
import readAndSeperate
app = Flask(__name__)

imageFolder = os.path.join('static', 'images')
graphImage = os.path.join('static/images/')
app.config['UPLOAD_FOLDER'] = imageFolder
app.config['IMAGE'] = graphImage
def getImageList():
    """
    For the Images in the SAUN index Page
    :return: A list of Images
    """
    imageList = os.listdir('static/images/solutions')
    imagelist = ['static/images/solutions/' + image for image in imageList]
    return imagelist

def getGallaryImages():
    """
    For the Gallary images
    :return: A list of images for the Gallary.
    """
    imageList = os.listdir('static/gallary')
    imagelist = ['static/gallary/' + image for image in imageList]
    return imagelist

@app.route('/')
def index():  # put application's code here
    return render_template('index.html',image=getImageList(),g=0)

@app.route('/uploadFile',methods = ['GET','POST'])
def uploadFile():
    """
    This function take the selected solution name and the file to be  converted. And write a script for the Information.
    :return: Redirect the Index Page with the Solution Thumbnails and the generated solution RDF/TTL File
    """
    start = time.time()
    print("Function upload Start ...")
    print(request.form.get('turtle'))

    selectedG = 0
    current_path = ""

    if request.method == 'POST':
        submitt = request.form['uploadFile']
        if request.form['uploadFile'] == "Create_solution":
            selectedG = 1
        if request.form['uploadFile'] == "Generate Solution 1":
            selectedG = 1
        if request.form['uploadFile'] == "Generate Solution 2":
            selectedG = 2
        if request.form['uploadFile'] == "Generate Solution 3":
            selectedG = 3
        if request.form['uploadFile'] == "Generate Solution 4":
            selectedG = 4
        if request.form['uploadFile'] == "Generate Solution 5":
            selectedG = 5
        if request.form['uploadFile'] == "Generate Solution 6":
            selectedG = 6
        if request.form['uploadFile'] == "Generate Solution 7":
            selectedG = 7
        if request.form['uploadFile'] == "Generate Solution 8":
            selectedG = 8
        print("Selected Solution ", selectedG)

        if request.files['file']:
            file = request.files['file']
            print(file.filename)
            filename_ = file.filename
            if "csv" in str(filename_):
                file.save(os.path.join("csv",file.filename))
                current_path+= "csv/"
            elif "xlsx" in str(filename_):
                file.save(os.path.join("excel", file.filename))
                current_path += "excel/"
            else:
                print("Other file uploaded, ")
            # Dictionary Information will be used in other classes
            dic = {"filename":file.filename,"selectedGraph":selectedG, "currentPath":current_path, "exportFormat":request.form.get('turtle')}
            with open("script/script.json",'w') as script:
                json.dump(dic,script)

            readAndSeperate.runDataPreparation()
            Dynamic.G()
            end = time.time() - start
            print("Total run Time for generating solution " + str(selectedG), end)
            f_ = open("rdf/modelGraphDynamic_G"+str(selectedG)+".rdf","r")
            return render_template('index.html', image=getImageList(), file=f_,g=selectedG)
        # Same file still selected, run class Dynamic directly.
        else:
            print("no File foun, redirect last uploaded File.")
            file = open("script/script.json", 'r')
            jsonData = json.load(file)

            dic = {"filename":jsonData['filename'],"selectedGraph":selectedG, "currentPath":jsonData['currentPath'], "exportFormat":jsonData['exportFormat']}
            with open("script/script.json",'w') as script:
                json.dump(dic,script)
            Dynamic.G()
            image = os.path.join(app.config["IMAGE"], "solution_one.jpg")
            end2 = time.time() - start
            print("Total run Time for generating solution " + str(selectedG), end2)
            return render_template('index.html',image=getImageList(),g=selectedG)

@app.route('/local', methods=['GET','POST'])
def local():
    """
    This function for navigating the Menus in the View.
    :return: Redirect the selected HTML page with a specific value.
    """
    if request.method == 'POST':
        if request.form['loadPage'] == "solutions":
            return render_template('index.html',image=getImageList())
        if request.form['loadPage'] == "querys":
            from fuseki import checkFusekiSocket
            # If the Fuseki server is running the Data must be redirectet.
            if checkFusekiSocket():
               import querys
               data = querys.UIQuery()
               #print("Data is ::", data)
               return render_template('queries.html', data=data)
            else:
            # The Fuseki server is off, redirect the templet only
                return render_template('queries.html', message="Fuseki server is offline")
        # for the controll panel the data_script must be read and redirect to the view. By change rewrite the file.
        if request.form['loadPage'] == "fuseki-control":
            data_script = open("script/fuseki_data_script.json", 'r')
            load_data = json.load(data_script)
            return render_template('fuseki_control.html',datasetName=load_data['datasetName'],port=load_data['port'], ip=load_data['ip'])
        if request.form['loadPage'] == "ontology-setup":
           listOfOntologys = std.UIontologyStatic()

           return render_template('ontology.html', list = listOfOntologys)

        if request.form['loadPage'] == "graph":
            import DatabaseManager__
            data = DatabaseManager__.dataReader()
            image = os.path.join(app.config["IMAGE"], "image.png")
            return render_template('graph.html',graphImage=image, data=data)

        if request.form['loadPage'] == "gallary":
            return render_template('gallry.html', images=getGallaryImages())

        else:
            return render_template('index.html',image=getImageList())

    return render_template('local.html')



@app.route('/fuseki', methods=['GET', 'POST'])
def fuseki():
    """
    Function for the control pannel of the fuseki server. To display the data script must be readed. By changing the values rewrite the data_script.
    :return: render the fuseki_control templet. Push Data to the view.
    """
    data_script = open("script/fuseki_data_script.json", 'r')
    load_data = json.load(data_script)
    if request.method == 'POST':
        if request.form['datasetname']:
            load_data['datasetName'] = request.form['datasetname']
        if request.form['port']:
            load_data['port'] = request.form['port']
        if request.form['ip']:
            load_data['ip'] = request.form['ip']
        if request.form['memory']:
            load_data['memory'] = request.form['memory']

    with open("script/fuseki_data_script.json",'w') as script:
        json.dump(load_data,script)
    data_script = open("script/fuseki_data_script.json", 'r')
    load_data = json.load(data_script)
    return render_template('fuseki_control.html', datasetName=load_data['datasetName'],port=load_data['port'], ip=load_data['ip'],memory=load_data['memory'])



@app.route('/query', methods=['GET','POST'])
def query():
    """
    Function for the page query. If request on to run server then upload data.
    :return: render query.html and push query result. else render template only.
    """
    if request.method == 'POST':
       import querys
       currentG = readAndSeperate.selected_G()
       print("Current Graph for Q is ", currentG)
       data = querys.getData(currentG,0)
       return render_template('queries.html', data=data['results']['bindings'])
    else: return render_template('queries.html')

@app.route('/fuseki_status_changer', methods=['GET', 'POST'])
def fuseki_status_changer():
    """
    To avoid conflicts in Fuseki port the fuseki status must be always checked.
    :return: render the queries.html with the query result. Else render the queries with message only.
    """
    from fuseki import fuseki_control, fusekiConnector, checkFusekiSocket
    if request.method == "POST":
        import querys
        fuseki_control()
        fusekiConnector()
        print("Deleay Server for 3 second!")
        time.sleep(3)
        if checkFusekiSocket():
           data = querys.UIQuery()
           return render_template('queries.html', data=data)
    return render_template('queries.html', message="Fuseki Server is off, Switch to run")


@app.route('/graph',methods=['GET','POST'])
def graph():
    """
    For uploading the generated Graph image.
    :return: render index with the images thumbnails.
    """
    if request.method == 'POST':
        return render_template('index.html',image=getImageList())
    pass
@app.route('/graph_image',methods=['GET','POST'])
def showGraph():
    """
    Reading the Graph image.
    :return: render the graph page with the graph image.
    """
    image = os.path.join(app.config["UPLOAD_FOLDER"], "static/images/image.png")
    return render_template("graph.html", graphImage= image)

@app.route('/runQueryOnGraph',methods=['GET','POST'])
def runQueryOnGraph():
    """
    This function use the information in the Database to select the Graph and it's Description. The Graph Creator Function will be run
    :return: in case of success graph generating render the graph page with the new generated graph image und push the information (Data) of each Graph.
    """
    from querys import graphviz_creator
    import DatabaseManager__
    data = DatabaseManager__.dataReader()

    if request.method == 'POST':
        value_holder = request.form['selectedGraph']
        print("value is ::",value_holder)

        for i in range(9):

                if value_holder == "Graph Solution "+str(i)+"":
                   print("Generating Graph ", i)
                   graphviz_creator(i)
                   image = os.path.join(app.config["IMAGE"], "image.png")
                   return render_template('graph.html', graphImage=image, data=data)

        return render_template('graph.html')
    return render_template('graph.html')


@app.route('/status', methods=['GET','POST'])
def status(std,page):

    pass

@app.route('/upload_and_display_image', methods=['GET','POST'])
def upload_and_display_image():
    """
    This function to update the gallary in the Application.
    :return: return the gallary page with all images that have been saved in the Gallary images Directory.
    """
    try:
       if request.method == "POST":
           #if request.form['submit_']:
              file = request.files['upload']
              file.save(os.path.join("static/gallary", file.filename))
       return render_template('gallry.html', images=getGallaryImages())
    except Exception as e:
        print("Error happen...")
        return render_template('gallry.html',image=getGallaryImages())
    pass

@app.route('/download')
def download():
    """
    This function push the generated graph solution to the view.
    :return: nothig, send file as attachment to the View.
    """
    solution = readAndSeperate.selected_G()
    print(solution)
    path = "rdf/modelGraphDynamic_G" + str(solution) + "."+readAndSeperate.getExportFormat()[0]
    return send_file(path, as_attachment=True)


@app.route('/delete_galary_image', methods=['GET','POST'])
def delete_galary_image():
    """
    This function retriev the selected image number and remove it from the image gallary.
    :return: redirect the gallary page with all images.
    """
    if request.method == 'POST':

        if request.form['Delete Image'] == 'Delete Image':
            try:

                imageNumber = request.form['imageIndex']
                print(imageNumber)
                gallaryImages = getGallaryImages()
                imageName = gallaryImages[int(imageNumber)]
                print("image name is :: ", imageName)
                os.remove(str(imageName))
            except Exception as e: print('Error',e)
            return render_template('gallry.html', images=getGallaryImages())
    return render_template('gallry.html', images=getGallaryImages())


    pass

if __name__ == '__main__':
   #subprocess.Popen('installation.bat')
   app.run()
