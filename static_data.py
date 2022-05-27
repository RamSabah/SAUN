
#Define List of Ontology
# For adding new Ontology use a tuple ([identification_1, identification_2, ...], ontology) and check the periority.

list_of_ontology = [(["foaf"],'foaf'),
                    (["dc/terms","dcterms"],'dcterms'),
                    (["22-rdf-syntax"],'rdf'),
                    (["doap"],'doap'),
                    (["nomisma","ontology"],'nmo'),
                    (["nomisma","id"],'nm'),
                    (["rdfs","void"],'void'),
                    (["rdfs","sioc","services"],'svcs'),
                    (["rdfs"],'rdfs'),
                    (["edm"],'edm'),(["oa#"],'oa'),
                    (["skos"],'skos'),
                    (["hasUncertainty"],'un'),
                    (["rdf-schema"],'rdfs')]

#link = "http://nomisma.org/ontology#hasMaterial"
def UIontologyStatic():
    return list_of_ontology

    pass
def getOntology(link):
    validator = False
    for i in list_of_ontology:
        for j in i[0]:
            if j in link:
                validator = True
        if validator:
           return i[1]
    return "notinclude"

#print(getOntology())

"""list_of_ontology = [(["foaf"], 'foaf'), (["dc/terms", "dcterms"], 'dcterms'), (["22-rdf-syntax"], 'rdf'),
                    (["doap"], 'doap'), (["nomisma", "ontology"], 'nmo'), (["nomisma", "id"], 'nm'),
                    (["rdfs", "void"], 'void'), (["rdfs", "sioc", "services"], 'svcs'), (["rdfs"], 'rdfs'),
                    (["edm"], 'edm'), (["oa#"], 'oa'), (["skos"], 'skos'), (["hasUncertainty"], 'un')]"""


def prefixMerg(link):
    """

    :param link: input link of the headers
    :return: list of tow element[ Prefix, Property]
    """
    if 'http' not in link:return link
    prefix = getOntology(link)
    reversLink = link[::-1]
    property = ""
    for i in reversLink:
       if i != '/' and i != '#':
           property+=i
       else: return prefix+':'+property[::-1]

# Ontology detect ## Desabled
'''def getOntology(link):
    if ('foaf' in link):
        return 'foaf'
    if 'dc/terms' in link:
        return 'dcterms'
    if 'dcterms' in link:
        return 'dcterms'
    if '22-rdf-syntax' in link:
        return 'rdf'
    if 'doap' in link:
        return 'doap'
    if 'nomisma' in link and 'ontology' in link:
        return 'nmo'
    if 'nomisma' in link and 'id' in link:
        return 'nm'
    if 'rdfs' in link and 'void' in link:
        return 'void'
    if 'rdfs' in link and 'sioc' in link and 'services' in link:
        return 'svcs'
    if 'rdfs' in link:
        return 'rdfs'
    if 'edm' in link:
        return 'edm'
    if 'oa#' in link:
        return 'oa'
    if 'skos' in link:
        return 'skos'
    if 'hasUncertainty' in link:
        return 'un'
    else:
        return "notInclude"'''