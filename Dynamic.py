"""
Class for building the Graph
"""
import time
import json
import csv
import urllib
import re
import random
import pandas as pd
from rdflib.graph import Graph
from rdflib import RDF,RDFS,Namespace,DCTERMS,URIRef,Literal,BNode
import re
import numpy as np

import readAndSeperate
import readAndSeperate as data


# Take solution i and generate Graph i
def G():
    """
    This function build the Graph using the input Data
    :return: return nothing, write an rdf file to specific directory
    :param: ontology list, headers, data
    """
    solution = data.selected_G()
    G = Graph()
    n_names = []
    n_domain = []
    n_node = []
    namespaces = Namespaces()
    # if Dynamic().a ==  1:
    UN = Namespace('http://www.owl-ontologies.com/Ontology1181490123.owl')
    NM = Namespace('http://nomisma.org/id/')
    CRM = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
    BMO = Namespace('http://collection.britishmuseum.org/id/ontology/')
    G.bind('un', 'http://www.owl-ontologies.com/Ontology1181490123.owl')
    G.bind('nm', 'http://nomisma.org/id/')
    G.bind('crm', 'http://www.cidoc-crm.org/cidoc-crm/')
    G.bind('bmo', 'http://collection.britishmuseum.org/id/ontology/')

    for i in namespaces:
        if i[1] not in n_names:
            n_names.append(i[1])
            n_domain.append(i[2])
        n_node.append(i[1].upper() + "['" + i[0] + "']")

    print("NamespacesNodes", n_node)
    n_node.insert(0, "")

    for j in range(len(n_names)):
        G.bind(n_names[j], n_domain[j])
        exec('' + (n_names[j]).upper().strip() + " = Namespace("'"' + n_domain[j] + '"'")")

    print("Namespaces Names: ", n_names)
    print("Namespaces Link: ", n_domain)
    Content = data.getContent()


    # X_Achse = 0
    Y_Achse = 0
    nodeCounter = 0

    uncertainArray = uncertainArray_()
    ## _________________________________________________________________________________________ 1 ---

    if solution == 1:
        print("Creating Solution 1")
        for con in Content:
            X_Achse = 0
            for inncon in range(1, len(con)):
                if con[inncon] != '':
                    if uncertainArray[X_Achse][Y_Achse] == 0:
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(con[inncon]):
                            G.add((URIRef(con[0]), eval(n_node[inncon]), URIRef(con[inncon])))
                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]),
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))


                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), Literal(con[inncon])))
                        # Bind the Uncertain Condition!!!
                    else:
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(con[inncon]):
                            G.add((URIRef(con[0]), eval(n_node[inncon]), URIRef(con[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), CRM['P140_assigned_attribute_to'], URIRef(con[0])))
                            G.add((BNode('b' + str(nodeCounter)), CRM['P141_assigned'], URIRef(con[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), BMO['PX_Property'], eval(n_node[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), BMO['PX_likelihood'], NM['uncertain_value']))
                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], CRM['E13']))
                            nodeCounter += 1

                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]),
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))
                            G.add((BNode('b' + str(nodeCounter)), CRM['P140_assigned_attribute_to'], URIRef(con[0])))
                            G.add((BNode('b' + str(nodeCounter)), CRM['P141_assigned'],
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))
                            G.add((BNode('b' + str(nodeCounter)), BMO['PX_Property'], eval(n_node[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), BMO['PX_likelihood'], NM['uncertain_value']))
                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], CRM['E13']))
                            nodeCounter += 1
                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), Literal(con[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), CRM['P140_assigned_attribute_to'], URIRef(con[0])))
                            G.add((BNode('b' + str(nodeCounter)), CRM['P141_assigned'], Literal(con[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), BMO['PX_Property'], eval(n_node[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), BMO['PX_likelihood'], NM['uncertain_value']))
                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], CRM['E13']))
                            nodeCounter += 1

                X_Achse += 1
            Y_Achse += 1

            # für jedes con alle inncon hinzufügen
        print("Serializing....")
        G_writer = open('rdf/modelGraphDynamic_G1.'+data.getExportFormat()[0], 'w', encoding='utf-8')
        G_writer.write(G.serialize(format=''+data.getExportFormat()[1]))
        print("G1 ready, ")

        # print(G.serialize())
        ## _________________________________________________________________________________________ 2 ---
    elif solution == 2:
        print("Creating solution 2")

        for con in Content:
            X_Achse = 0
            for inncon in range(1, len(con)):
                if con[inncon] != '':
                    if uncertainArray[X_Achse][Y_Achse] == 0:
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(
                                con[inncon]):
                            G.add((URIRef(con[0]), eval(n_node[inncon]), URIRef(con[inncon])))
                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]),
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))


                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), Literal(con[inncon])))
                        # Bind the Uncertain Condition!!!
                    else:  # UNCERTAIN
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(con[inncon]):

                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), UN['hasUncertainty'], NM['uncertain_value']))
                            G.add((BNode('b' + str(nodeCounter)), RDF['value'], URIRef(con[inncon])))
                            nodeCounter += 1

                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), UN['hasUncertainty'], NM['uncertain_value']))
                            G.add((BNode('b' + str(nodeCounter)), RDF['value'],
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))
                            nodeCounter += 1

                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), UN['hasUncertainty'], NM['uncertain_value']))
                            G.add((BNode('b' + str(nodeCounter)), RDF['value'], Literal(con[inncon])))
                            nodeCounter += 1

                X_Achse += 1
            Y_Achse += 1

            # für jedes con alle inncon hinzufügen
        print("Serializing....")
        G_writer = open('rdf/modelGraphDynamic_G2.'+data.getExportFormat()[0], 'w', encoding='utf-8')
        G_writer.write(G.serialize(format=''+data.getExportFormat()[1]))
        print("G2 ready,")


    # Solution 3-----------------------------------------------------------------------------------------------------
    elif solution == 3:
        print("Creating solution 3")
        C_Counter = 0
        A_Counter = 0
        G.add((URIRef("R1_Reliability_Assessment"), RDFS['subClassOf'], CRM['E16']))
        G.add((URIRef("T1_assessd_the_reliability_of"), RDFS['subPropertyOf'], CRM['P40']))
        G.add((URIRef("T2_assessd_as_reliability"), RDFS['subPropertyOf'], CRM['P39']))
        G.add((URIRef("R2_Reliability"), RDFS['subClassOf'], CRM['E54']))

        for con in Content:
            X_Achse = 0
            for inncon in range(1, len(con)):
                if con[inncon] != '':
                    if uncertainArray[X_Achse][Y_Achse] == 0:
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(
                                con[inncon]):
                            G.add((URIRef(con[0]), eval(n_node[inncon]), URIRef(con[inncon])))
                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]),
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))


                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), Literal(con[inncon])))
                        # Bind the Uncertain Condition!!!
                    else:
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(con[inncon]):

                            G.add((URIRef(con[0]), eval(n_node[inncon]), URIRef(con[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), CRM['P140_assigned_attribute_to'], URIRef(con[0])))
                            G.add((BNode('b' + str(nodeCounter)), CRM['P141_assigned'], URIRef(con[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['Property'], eval(n_node[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], CRM['E13']))
                            G.add((BNode('b' + str(nodeCounter)), CRM['T2_assessd_as_reliability'],
                                   BNode('c' + str(C_Counter))))
                            G.add((BNode('c' + str(C_Counter)), RDF['type'], CRM['R2_Reliability']))
                            G.add((BNode('c' + str(C_Counter)), CRM['P90_has_value'],
                                   Literal(uncertainArray[X_Achse][Y_Achse])))
                            G.add((BNode('A1'), CRM['T1_assessd_the_reliability_of'], BNode('b' + str(nodeCounter))))

                            nodeCounter += 1
                            C_Counter += 1

                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]),
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))
                            G.add((BNode('b' + str(nodeCounter)), CRM['P140_assigned_attribute_to'],
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))
                            G.add((BNode('b' + str(nodeCounter)), CRM['P141_assigned'],
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['Property'], eval(n_node[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], CRM['E13']))
                            G.add((BNode('b' + str(nodeCounter)), CRM['T2_assessd_as_reliability'],
                                   BNode('c' + str(C_Counter))))
                            G.add((BNode('c' + str(C_Counter)), RDF['type'], CRM['R2_Reliability']))
                            G.add((BNode('c' + str(C_Counter)), CRM['P90_has_value'],
                                   Literal(uncertainArray[X_Achse][Y_Achse])))
                            G.add((BNode('A1'), CRM['T1_assessd_the_reliability_of'], BNode('b' + str(nodeCounter))))
                            nodeCounter += 1
                            C_Counter += 1
                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), Literal(con[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), CRM['P140_assigned_attribute_to'], URIRef(con[0])))
                            G.add((BNode('b' + str(nodeCounter)), CRM['P141_assigned'], Literal(con[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['Property'], eval(n_node[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], CRM['E13']))
                            G.add((BNode('b' + str(nodeCounter)), CRM['T2_assessd_as_reliability'],
                                   BNode('c' + str(C_Counter))))
                            G.add((BNode('c' + str(C_Counter)), RDF['type'], CRM['R2_Reliability']))
                            G.add((BNode('c' + str(C_Counter)), CRM['P90_has_value'],
                                   Literal(uncertainArray[X_Achse][Y_Achse])))
                            G.add((BNode('A1'), CRM['T1_assessd_the_reliability_of'], BNode('b' + str(nodeCounter))))
                            nodeCounter += 1
                            C_Counter += 1

                X_Achse += 1
            Y_Achse += 1

            # für jedes con alle inncon hinzufügen
        print("Serializing....")
        G_writer = open('rdf/modelGraphDynamic_G3.'+data.getExportFormat()[0], 'w', encoding='utf-8')
        G_writer.write(G.serialize(format=''+data.getExportFormat()[1]))
        print("G3 ready,")
    # Solution 4 Using CRMinf________________________________________________________________________________________
    elif solution == 4:
        print("Creating solution 4")
        cNodeCounter = 0
        propositionCounter = 0
        CRMinf = Namespace('http://www.ics.forth.gr/isl/CRMinf/')
        G.bind('crminf', 'http://www.ics.forth.gr/isl/CRMinf/')
        for con in Content:
            X_Achse = 0
            for inncon in range(1, len(con)):
                if con[inncon] != '':
                    if uncertainArray[X_Achse][Y_Achse] == 0:
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(
                                con[inncon]):
                            G.add((URIRef(con[0]), eval(n_node[inncon]), URIRef(con[inncon])))
                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]),
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))


                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), Literal(con[inncon])))
                        # Bind the Uncertain Condition!!!
                    else:  # UNCERTAIN
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(con[inncon]):

                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], CRMinf['I5_Inference_Making']))

                            G.add((BNode('b' + str(nodeCounter)), CRMinf['J2_concluded_that'],
                                   BNode('c' + str(cNodeCounter))))
                            G.add((BNode('c' + str(cNodeCounter)), RDF['type'], CRMinf['I2_Belife']))
                            G.add((BNode('c' + str(cNodeCounter)), CRMinf['I4_Proposition_Set'],
                                   Literal("Proposition" + str(propositionCounter))))
                            G.add((BNode('c' + str(cNodeCounter)), CRMinf['J4_that'], URIRef(con[inncon])))
                            G.add((BNode('c' + str(cNodeCounter)), CRMinf['J5_holds_to_be'], Literal("uncertain")))
                            cNodeCounter += 1
                            nodeCounter += 1
                            propositionCounter += 1

                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], CRMinf['I5_Inference_Making']))

                            G.add((BNode('b' + str(nodeCounter)), CRMinf['J2_concluded_that'],
                                   BNode('c' + str(cNodeCounter))))
                            G.add((BNode('c' + str(cNodeCounter)), RDF['type'], CRMinf['I2_Belife']))
                            G.add((BNode('c' + str(cNodeCounter)), CRMinf['I4_Proposition_Set'],
                                   Literal("Proposition" + str(propositionCounter))))
                            G.add((BNode('c' + str(cNodeCounter)), CRMinf['J4_that'],
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))
                            G.add((BNode('c' + str(cNodeCounter)), CRMinf['J5_holds_to_be'], Literal("uncertain")))
                            cNodeCounter += 1
                            nodeCounter += 1
                            propositionCounter += 1

                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], CRMinf['I5_Inference_Making']))

                            G.add((BNode('b' + str(nodeCounter)), CRMinf['J2_concluded_that'],
                                   BNode('c' + str(cNodeCounter))))
                            G.add((BNode('c' + str(cNodeCounter)), RDF['type'], CRMinf['I2_Belife']))
                            G.add((BNode('c' + str(cNodeCounter)), CRMinf['I4_Proposition_Set'],
                                   Literal("Proposition" + str(propositionCounter))))
                            G.add((BNode('c' + str(cNodeCounter)), CRMinf['J4_that'], Literal(con[inncon])))
                            G.add((BNode('c' + str(cNodeCounter)), CRMinf['J5_holds_to_be'], Literal("uncertain")))
                            cNodeCounter += 1
                            nodeCounter += 1
                            propositionCounter += 1

                X_Achse += 1
            Y_Achse += 1

            # für jedes con alle inncon hinzufügen
        print("Serializing....")
        G_writer = open('rdf/modelGraphDynamic_G4.'+data.getExportFormat()[0], 'w', encoding='utf-8')
        G_writer.write(G.serialize(format=''+data.getExportFormat()[1]))
        print("G4 ready,")
# Solution 5 ___________________________________________________________________________________________________________
    elif solution == 5:
        print("Creating solution 5")
        AMT = Namespace('http://academic-meta-tool.xyz/vocab#')
        G.bind('amt', 'http://academic-meta-tool.xyz/vocab#')
        CRM = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
        G.bind('crm', 'http://www.cidoc-crm.org/cidoc-crm/')

        G.add((URIRef("P62.2_uncertain_depiction"), RDFS['subPropertyOf'], CRM['P62']))
        G.add((URIRef("P138.2_uncertain_authenticity"), RDFS['subPropertyOf'], CRM['P138']))
        G.add((URIRef("P14.2_uncertain_authority"), RDFS['subPropertyOf'], CRM['P14']))
        G.add((URIRef("P102.2_uncertain_name_or_ethnic"), RDFS['subPropertyOf'], CRM['P102']))

        G.add((URIRef("P16.2_uncertain_technic_or_object_used_for_creation"), RDFS['subPropertyOf'], CRM['P16']))
        G.add((URIRef("P67.2_uncertain_type"), RDFS['subPropertyOf'], CRM['P67']))
        G.add((URIRef("P107.2_uncertain_member"), RDFS['subPropertyOf'], CRM['P107']))

        G.add((URIRef("P3.2_uncertain_value"), RDFS['subPropertyOf'], CRM['P3']))
        G.add((URIRef("P130.2_uncertain_symbol_or_feature"), RDFS['subPropertyOf'], CRM['P130']))
        G.add((URIRef("P189.2_uncertain_place"), RDFS['subPropertyOf'], CRM['P189']))

        G.add((URIRef("P137.2_uncertain_material"), RDFS['subPropertyOf'], CRM['P137']))
        G.add((URIRef("P136.2_uncertain_context_or_taxonomy"), RDFS['subPropertyOf'], CRM['P136']))
        G.add((URIRef("P139.2_uncertain_form"), RDFS['subPropertyOf'], CRM['P139']))
        G.add((URIRef("P19.2_uncertain_mode"), RDFS['subPropertyOf'], CRM['P19']))

        headerCompairing = Namespaces()
        import G5_Preset
        for con in Content:
            X_Achse = 0
            for inncon in range(1, len(con)):
                if con[inncon] != '':
                    if uncertainArray[X_Achse][Y_Achse] == 0:
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(
                                con[inncon]):
                            G.add((URIRef(con[0]), eval(n_node[inncon]), URIRef(con[inncon])))
                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]),
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))


                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), Literal(con[inncon])))
                        # Bind the Uncertain Condition!!!
                    else:  # UNCERTAIN

                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(con[inncon]):
                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), AMT['weight'], Literal(uncertainArray[X_Achse][Y_Achse])))
                            G.add((BNode('b' + str(nodeCounter)),
                                   CRM[str(G5_Preset.getLiteral(headerCompairing[X_Achse][0]))], URIRef(con[inncon])))
                            nodeCounter += 1

                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), AMT['weight'], Literal(uncertainArray[X_Achse][Y_Achse])))
                            G.add((BNode('b' + str(nodeCounter)),
                                   CRM[str(G5_Preset.getLiteral(headerCompairing[X_Achse][0]))],
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))
                            nodeCounter += 1

                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), AMT['weight'], Literal(uncertainArray[X_Achse][Y_Achse])))
                            G.add((BNode('b' + str(nodeCounter)),
                                   CRM[str(G5_Preset.getLiteral(headerCompairing[X_Achse][0]))], Literal(con[inncon])))
                            nodeCounter += 1

                X_Achse += 1
            Y_Achse += 1

            # für jedes con alle inncon hinzufügen
        print("Serializing....")
        G_writer = open('rdf/modelGraphDynamic_G5.'+data.getExportFormat()[0], 'w', encoding='utf-8')
        G_writer.write(G.serialize(format=''+data.getExportFormat()[1]))
        print("G5 ready,")


# SOLUTION 11 -----------------------------------------------------------------------------------------------------------------------
    elif solution == 11:
        print("Creating solution 5.2")
        AMT = Namespace('http://academic-meta-tool.xyz/vocab#')
        G.bind('amt', 'http://academic-meta-tool.xyz/vocab#')
        CRM = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
        G.bind('crm', 'http://www.cidoc-crm.org/cidoc-crm/')
        G.bind('local','script/local/')
        LOCAL = Namespace('script/local/')

        headerCompairing = Namespaces()
        import G5_Preset
        for con in Content:
            X_Achse = 0
            for inncon in range(1, len(con)):
                if con[inncon] != '':
                    if uncertainArray[X_Achse][Y_Achse] == 0:
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(
                                con[inncon]):
                            G.add((URIRef(con[0]), eval(n_node[inncon]), URIRef(con[inncon])))
                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]),
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))


                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), Literal(con[inncon])))
                        # Bind the Uncertain Condition!!!
                    else:  # UNCERTAIN

                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(con[inncon]):
                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), AMT['weight'], Literal(uncertainArray[X_Achse][Y_Achse])))
                            G.add((BNode('b' + str(nodeCounter)),
                                   LOCAL[str(G5_Preset.getLiteral(headerCompairing[X_Achse][0]))], URIRef(con[inncon])))
                            nodeCounter += 1

                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), AMT['weight'], Literal(uncertainArray[X_Achse][Y_Achse])))
                            G.add((BNode('b' + str(nodeCounter)),
                                   LOCAL[str(G5_Preset.getLiteral(headerCompairing[X_Achse][0]))],
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))
                            nodeCounter += 1

                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), AMT['weight'], Literal(uncertainArray[X_Achse][Y_Achse])))
                            G.add((BNode('b' + str(nodeCounter)),
                                   LOCAL[str(G5_Preset.getLiteral(headerCompairing[X_Achse][0]))], Literal(con[inncon])))
                            nodeCounter += 1

                X_Achse += 1
            Y_Achse += 1

            # für jedes con alle inncon hinzufügen
        print("Serializing....")
        G_writer = open('rdf/modelGraphDynamic_G6.'+data.getExportFormat()[0], 'w', encoding='utf-8')
        G_writer.write(G.serialize(format=''+data.getExportFormat()[1]))
        print("G5.2 ready,")

# SOLUTION 6  -----------------------------------------------------------------------------------------------------------------------
    elif solution == 6:
        print("Creating Solution 7")

        EDTFO = Namespace('https://periodo.github.io/edtf-ontology/edtfo.ttl')
        G.bind('edtfo', 'https://periodo.github.io/edtf-ontology/edtfo.ttl')

        for con in Content:
            X_Achse = 0
            for inncon in range(1, len(con)):
                if con[inncon] != '':
                    if uncertainArray[X_Achse][Y_Achse] == 0:
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(con[inncon]):
                            G.add((URIRef(con[0]), eval(n_node[inncon]), URIRef(con[inncon])))
                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]),
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))


                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), Literal(con[inncon])))
                        # Bind the Uncertain Condition!!!
                    else:
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(con[inncon]):
                            G.add((URIRef(con[0]), eval(n_node[inncon]), URIRef(con[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['subject'], URIRef(con[0])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['object'], URIRef(con[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['Property'], eval(n_node[inncon])))

                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], EDTFO['UncertainStatement']))
                            nodeCounter += 1

                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]),
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['subject'], URIRef(con[0])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['object'],
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['Property'], eval(n_node[inncon])))

                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], EDTFO['UncertainStatement']))
                            nodeCounter += 1
                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), Literal(con[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['subject'], URIRef(con[0])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['object'], Literal(con[inncon])))
                            G.add((BNode('b' + str(nodeCounter)), RDF['Property'], eval(n_node[inncon])))

                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], EDTFO['UncertainStatement']))
                            nodeCounter += 1

                X_Achse += 1
            Y_Achse += 1

            # für jedes con alle inncon hinzufügen
        print("Serializing....")
        G_writer = open('rdf/modelGraphDynamic_G6.'+data.getExportFormat()[0], 'w', encoding='utf-8')
        G_writer.write(G.serialize(format=''+data.getExportFormat()[1]))
        print("G6 ready, ")
# SOLUTION 7____________________________________________________________________________________________________________

    elif solution == 7:
        print("Creating solution 8")

        EDTFO = Namespace('https://periodo.github.io/edtf-ontology/edtfo.ttl')
        G.bind('edtfo', 'https://periodo.github.io/edtf-ontology/edtfo.ttl')

        for con in Content:
            X_Achse = 0
            for inncon in range(1, len(con)):
                if con[inncon] != '':
                    if uncertainArray[X_Achse][Y_Achse] == 0:
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(
                                con[inncon]):
                            G.add((URIRef(con[0]), eval(n_node[inncon]), URIRef(con[inncon])))
                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]),
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))


                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), Literal(con[inncon])))
                        # Bind the Uncertain Condition!!!
                    else:  # UNCERTAIN
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(con[inncon]):

                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], EDTFO['UncertainStatement']))
                            G.add((BNode('b' + str(nodeCounter)), RDF['value'], URIRef(con[inncon])))
                            nodeCounter += 1

                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], EDTFO['UncertainStatement']))
                            G.add((BNode('b' + str(nodeCounter)), RDF['value'],
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))
                            nodeCounter += 1

                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), RDF['type'], EDTFO['UncertainStatement']))
                            G.add((BNode('b' + str(nodeCounter)), RDF['value'], Literal(con[inncon])))
                            nodeCounter += 1

                X_Achse += 1
            Y_Achse += 1

            # für jedes con alle inncon hinzufügen
        print("Serializing....")
        G_writer = open('rdf/modelGraphDynamic_G7.'+data.getExportFormat()[0], 'w', encoding='utf-8')
        G_writer.write(G.serialize(format=''+data.getExportFormat()[1]))
        print("G7 ready,")

#SOLUTION 8_____________________________________________________________________________________________________________

    elif solution == 8:
        print("Creating solution 9")

        #EDTFO = Namespace('https://periodo.github.io/edtf-ontology/edtfo.ttl') Not in use
        #G.bind('edtfo', 'https://periodo.github.io/edtf-ontology/edtfo.ttl') Not in use

        for con in Content:
            X_Achse = 0
            for inncon in range(1, len(con)):
                if con[inncon] != '':
                    if uncertainArray[X_Achse][Y_Achse] == 0:
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(
                                con[inncon]):
                            G.add((URIRef(con[0]), eval(n_node[inncon]), URIRef(con[inncon])))
                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), eval(n_node[inncon]),
                                   Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))


                        else:
                            G.add((URIRef(con[0]), eval(n_node[inncon]), Literal(con[inncon])))
                        # Bind the Uncertain Condition!!!
                    else:  # UNCERTAIN
                        if ('http:' in con[inncon] or 'https' in con[inncon]) and "XMLSchema" not in str(con[inncon]):

                            G.add((URIRef(con[0]), UN['hasUncertainty'], BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)),eval(n_node[inncon]), URIRef(con[inncon])))
                            nodeCounter += 1

                        elif 'XMLSchema' in con[inncon]:
                            G.add((URIRef(con[0]), UN['hasUncertainty'], BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), eval(n_node[inncon]),  Literal(valueLinkSeperator(con[inncon])[0],
                                           datatype=valueLinkSeperator(con[inncon])[1])))
                            nodeCounter += 1

                        else:
                            G.add((URIRef(con[0]), UN['hasUncertainty'], BNode('b' + str(nodeCounter))))
                            G.add((BNode('b' + str(nodeCounter)), eval(n_node[inncon]),Literal(con[inncon])))
                            nodeCounter += 1

                X_Achse += 1
            Y_Achse += 1

            # für jedes con alle inncon hinzufügen
        print("Serializing....")
        G_writer = open('rdf/modelGraphDynamic_G8.'+data.getExportFormat()[0], 'w', encoding='utf-8')
        G_writer.write(G.serialize(format=''+data.getExportFormat()[1]))
        print("G8 ready,")

    else:
        print("No solution selected!")


# Check content only. Not in use :!
def Content(self):
    contents = data.getContent()
    print(contents)
    for i in contents:
        print(i[1])


# seperate link from numbers e.g. 8.0^^http://www.w3.org/2001/XMLSchema#double
def valueLinkSeperator(input):
    list = []

    try:
        if "string" in input:
            return input.split("^^")

        splitetdInput = input.split((re.search("(?P<url>https?://[^\s]+)", input).group("url")))
        list = []
        for i in splitetdInput:
            newstr = ''.join((ch if ch in '0123456789.' else ' ') for ch in i)
            listOfNumbers = [float(i) for i in newstr.split()]
            for j in listOfNumbers:
                if isinstance(j, float):
                    list.append(j)

        list.append(re.search("(?P<url>https?://[^\s]+)", input).group("url"))
    except:
        splitetdInput = input.split((re.search("(?P<url>https?://[^\s]+)", input)))
        list = []
        for i in splitetdInput:
            newstr = ''.join((ch if ch in '0123456789.' else ' ') for ch in i)
            listOfNumbers = [float(i) for i in newstr.split()]
            for j in listOfNumbers:
                if isinstance(j, float):
                    list.append(j)

        list.append(re.search("(?P<url>https?://[^\s]+)", input))
    print("ValueList::   ", list)

    return list


# get namespaces
def Namespaces():  # -- Return Namespace and Ontologpy
    """
    This function is for bilding the Namespaces of the input file. It use the headers and the getOntology function to bild the namespaces.
    :return: Return list of the Namespaces
    """
    print("Building Namespaces...")

    columnsList = []
    singleColumn = ""
    namespaces = data.getHeader()
    #print("Namespaces ",namespaces)
    for namespace in namespaces[1:]:
        for i in namespace[::-1]:
            if i != '/' and i != '#':
                singleColumn += i
            else:
                break
        columnsList.append(
            [singleColumn[::-1], getOntology(namespace), namespace.replace(singleColumn[::-1], '')])
        singleColumn = ""

    print('Columnlist ', columnsList)
    return columnsList


# random uncertain array
def uncertainArray_():
    """
    This function for rebulding the Uncertain Array. The uncertain array must be parrellel in width and depth to the Data Array.
    Using the (*) and non(http) for identifying an uncertain column. If there is no uncertain colum the function bild an uncertain array
    with certain entries.
    :return: Uncertain array
    """
    print("Generating uncertain array ...\n")
    check_uncertain_array = readAndSeperate.check_excel()
    if check_uncertain_array:
        headerLength = len(data.getHeader())
        contentLength = data.getContent()
        counter = 0
        for i in contentLength:
            counter += 1
        # print("pass3")
        #print(counter)
        MArray = [[1 for x in range(headerLength)] for y in range(counter)]
        # print(MArray[1])
        for i in range(int(counter / 2)):
            aNumber = random.randint(0, counter - 1)
            bNumber = random.randint(0, headerLength - 1)
            MArray[aNumber][bNumber] = 0

        for j in range(len(MArray)):
            MArray[j][0] = 0
            MArray[j][1] = 0
        # print("UncertainArray Counter: ", counter)
        # Flip MArray
        Marray_2 = []
        MArray_Healper = []
        for a in range(len(MArray[0])):
            for b in range(len(MArray)):
                MArray_Healper.append(MArray[b][a])
            Marray_2.append(MArray_Healper)
            MArray_Healper = []
        print(MArray)
        return Marray_2
    else:
        ## Uncertain Array is 0, TODO_
        df = pd.read_excel(r'readyToRun/uncertain_array.xlsx')
        dataHeaders = Namespaces()
        contendLength = data.getContent()
        counter = 0
        for o in contendLength:
            counter += 1
        uncertainHeaders = []
        orginalDataHeaders = []
        columnsData_healper = []
        columndData = []
        Marray = []
        for x in dataHeaders:
            orginalDataHeaders.append(x[0])

        for i in df:
            uncertainHeaders.append(i.split('*')[0])

        for g in orginalDataHeaders:
            if g in uncertainHeaders:
                pass

        values_ = df.values
        #print(len(values_[0]))
        for x in range(len(values_[0])):
            for y in range(len(values_)):
                columnsData_healper.append(values_[y][x])
            columndData.append(columnsData_healper)
            columnsData_healper = []

        for a in orginalDataHeaders:
            if a in uncertainHeaders:
                index = uncertainHeaders.index(str(a))
                Marray.append(columndData[index])
            else:
                for k in range(counter):
                    columnsData_healper.append(0)
                Marray.append(columnsData_healper)
                columnsData_healper = []
        #print("Temporer MArray-,", Marray)
        for xx in range(len(Marray)):
            for x_ in range(len(Marray[0])):
                if np.isnan(Marray[xx][x_]):
                    Marray[xx][x_] = 0
                if Marray[xx][x_] == 1.0:
                    Marray[xx][x_] = 1

        #print("uncertain array ready", Marray)
        return Marray


# Ontology detect
#_Testet_uncomplet---
def getOntology(link):
    """
    This function use the list_of_ontology to find the ontology of the link.
    :param link: link is a URI that begin with the key word http.
    #############################################################
    # if you have a notinclude PREFIX by generated file, add    #
    # the Prefix manually in the list_of_ontolgy.               #
    #############################################################
    :return: If the link defind, return the ontology, else notinclude.
    """
    import static_data
    list_of_ontology = static_data.list_of_ontology
    validator = False
    for i in list_of_ontology:
        for j in i[0]:
            if j in link:
                validator = True
            else:break
        if validator:
           return i[1]
    return "notinclude"




# Entry___________________________________________________________________________________________________________
# Interface
def getFileName(self):
    file = open("recivedFiles/script.json", 'r')
    return (json.load(file)['filename'])


# Fuseki
def datasetName(self):
    return "dataG"


# Interface
def HTMLReciver(self):
    file = open("recivedFiles/script.json", 'r')
    dics = json.load(file)
    if 'xlsx' in str(dics['filename']):
        pass


# Benchmark
def dataName(self, g=0):
    return "csv/modelGraphDynamic_G5.rdf"


# Benchmark
def query(self):
    #object = model2Bechmark.QUERY
    # return object().G1_Certain_Uncertain_CostomG()  # G1_Certain_Uncertain_CostomG(), Return collection272 Certain and Uncertain
    # return object().Art_Of_D_G1_ae_Certain_and_Uncertain_Query() # Return hasMaterial = nm:ae certain and uncertain
    # return object().genericQueryLimited()  # Return hasMaterial = nm:ae certain and uncertain
    return object().genericQuery()  # G1_uncertain_only


# Interface
def getFilename(self):
    file = open("recivedFiles/script.json", 'r')
    dics = json.load(file)
    return str(dics['filename'])



if __name__=='__main__':
    G()
    pass
