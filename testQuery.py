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
PREFIX edtfo:<https://periodo.github.io/edtf-ontology/edtfo.ttl>'''

# SOLUTION QUERY S1
#_____________________________________________________________________________________________
S1Q1 = PREFIX + '''
  SELECT ?s WHERE { ?s nmo:hasMint nm:comama . 
  FILTER NOT EXISTS{{?b crm:P140_assigned_attribute_to ?s} {?b ?f nm:uncertain_value .}}}
'''

S1Q2 = PREFIX + '''
  SELECT ?s WHERE {?s nmo:hasMint nm:comama. }
'''

S1Q3 = PREFIX + '''
  SELECT ?s ?o WHERE {?s nmo:hasMint ?o. } 
'''

S1Q4 = PREFIX + '''
  SELECT ?s WHERE { 
        ?s nmo:hasMint ?o . 
   FILTER NOT EXISTS{{?b crm:P140_assigned_attribute_to ?s} {?b ?f nm:uncertain_value .}}}
'''

S1Q5 = PREFIX + '''
 SELECT ?s ?p ?o WHERE { ?s ?p ?o . 
        ?b crm:P140_assigned_attribute_to ?s; ?f nm:uncertain_value;  bmo:PX_Property ?p; crm:P141_assigned ?o.} 
'''
# SOLUTION QUERY S2
#_____________________________________________________________________________________________
S2Q1 = PREFIX + '''
 SELECT ?s WHERE {?s nmo:hasMint nm:comama. }  
'''

S2Q2 = PREFIX + '''
 SELECT ?s  WHERE {{?s nmo:hasMint nm:comama.} 
          UNION{?s nmo:hasMint ?b.  ?b ?p nm:comama; un:hasUncertainty nm:uncertain_value}}   
'''

S2Q3 = PREFIX + '''
 SELECT ?s ?o WHERE { {?s nmo:hasMint ?o.}  UNION {?s nmo:hasMint ?b.  ?b ?p ?o.} FILTER(!isBlank(?o)) FILTER NOT EXISTS{?b un:hasUncertainty ?o.}} 
'''

S2Q4___ = PREFIX + '''
 SELECT ?s WHERE {?s nmo:hasMint ?o. FILTER NOT EXISTS{{?s ?p ?b.}{?b un:hasUncertainty ?f}}}    
'''

S2Q4 = PREFIX + '''
SELECT ?s WHERE {?s nmo:hasMint ?o. FILTER(!isBlank (?o))} 
'''

S2Q5 = PREFIX + '''
 SELECT ?s ?o WHERE {?s nmo:hasMint ?b . ?b un:hasUncertainty nm:uncertain_value;  rdf:value ?o . } 
'''

# SOLUTION QUERY S3
#_____________________________________________________________________________________________
S3Q1 = PREFIX + '''
   SELECT ?s WHERE { 
        ?s nmo:hasMint nm:comama.    
         FILTER NOT EXISTS{ ?b crm:T1_assessd_the_reliability_of ?f. 
        ?f crm:P140_assigned_attribute_to ?s; ?p nmo:hasMint.}}
'''

S3Q2 = PREFIX + '''
 SELECT ?s WHERE {  ?s nmo:hasMint nm:comama. }  
'''

S3Q3 = PREFIX + '''
 SELECT ?s ?o WHERE {  ?s nmo:hasMint ?o }  
'''

S3Q4 = PREFIX + '''
 SELECT ?s WHERE { 
        ?s nmo:hasMint ?o.    
         FILTER NOT EXISTS{ ?b crm:T1_assessd_the_reliability_of ?f. 
        ?f crm:P140_assigned_attribute_to ?s; ?p nmo:hasMint.}} 
'''

S3Q5 = PREFIX + '''
 SELECT ?s ?cl WHERE { 
        ?b crm:T2_assessd_as_reliability ?f;    
        crm:P140_assigned_attribute_to ?s; 
        ?p ?x. 
        ?f crm:P90_has_value ?cl. 
        ?s ?x ?o. }
'''
# SOLUTION QUERY S4
#_____________________________________________________________________________________________
S4Q1 = PREFIX + '''
 SELECT ?s WHERE { ?s nmo:hasMint nm:comama. }
'''

S4Q2 = PREFIX + '''
 SELECT ?s  WHERE { 
        {?s nmo:hasMint nm:comama.} 
        UNION{  
        ?s nmo:hasMint ?b. 
        ?b crminf:J2_concluded_that ?f. 
        ?f ?p nm:comama.} }
'''

S4Q3 = PREFIX + '''
SELECT  ?s ?o  WHERE { 
        {?s nmo:hasMint ?o.} 
        UNION{  
        ?s nmo:hasMint ?b. 
        ?b crminf:J2_concluded_that ?f. 
        ?f crminf:J4_that ?o.}
  FILTER(!isBlank(?o))}
'''

S4Q4 = PREFIX + '''
SELECT ?s WHERE {  ?s nmo:hasMint ?o.  FILTER(!isBlank(?o))}
'''

S4Q5 = PREFIX + '''
SELECT ?s ?v WHERE {
 	?s nmo:hasMint ?b . 
    ?b crminf:J2_concluded_that ?f.
 	?f crminf:J4_that ?v;  crminf:J5_holds_to_be "uncertain". }
'''

# SOLUTION QUERY S5
#_____________________________________________________________________________________________
S5Q1 = PREFIX + '''
SELECT ?s WHERE { ?s nmo:hasMint nm:comama.  }
'''

S5Q2 = PREFIX + '''
    SELECT ?s  WHERE { 
        {?s nmo:hasMint nm:comama.} 
        UNION{  
        ?s nmo:hasMint ?b. 
        ?b crm:P189.2_uncertain_place nm:comama.}}
'''

S5Q3 = PREFIX + '''
    SELECT ?s ?o WHERE { 
        {?s nmo:hasMint ?o.} 
        UNION{  
        ?s nmo:hasMint ?b. 
        ?b crm:P189.2_uncertain_place ?o.}
    FILTER (!isBlank(?o))}
'''

S5Q4 = PREFIX + '''
SELECT ?s WHERE { ?s nmo:hasMint ?o. FILTER(!isBlank (?o))}
'''

S5Q5 = PREFIX + '''
SELECT ?s ?ul WHERE {
 	?s nmo:hasMint ?b. 
    ?b crm:P189.2_uncertain_place nm:comama; amt:weight ?ul .}
'''


# SOLUTION QUERY S6
#_______________________________________________________________________________________________________________________

S6Q1 = PREFIX + '''
  SELECT ?s WHERE { ?s nmo:hasMint nm:comama . 
  FILTER NOT EXISTS{{?b rdf:subject ?s} {?b rdf:object nm:comama .} {?b rdf:Property nmo:hasMint.} {?b rdf:type edtfo:UncertainStatement.}}}

'''

S6Q2 = PREFIX + '''
SELECT ?s WHERE {?s nmo:hasMint nm:comama. } 
'''

S6Q3 = PREFIX + '''
SELECT ?s ?o WHERE {?s nmo:hasMint ?o. } 
'''

S6Q4 = PREFIX + '''
  SELECT ?s WHERE { 
            ?s nmo:hasMint ?o . 
            FILTER NOT EXISTS{{?b rdf:subject ?s} {?b rdf:object nm:comama .} {?b rdf:Property nmo:hasMint.} {?b rdf:type edtfo:UncertainStatement.}}}
'''

S6Q5 = PREFIX + '''
SELECT ?s ?p ?o WHERE { ?s ?p ?o . 
           ?b rdf:subject ?s; rdf:type edtfo:UncertainStatement;  rdf:Property ?p; rdf:object ?o.} 
'''


# SOLUTION QUERY S7
#______________________________________________________________________________________________

S7Q1 = PREFIX + '''
SELECT ?s WHERE {?s nmo:hasMint nm:comama. } 
'''

S7Q2 = PREFIX + '''
SELECT ?s  WHERE {
    {?s nmo:hasMint nm:comama.} 
UNION
    {?s nmo:hasMint ?b.  
     ?b ?p nm:comama; rdf:type edtfo:ApproximateStatement.}} 

'''

S7Q3 = PREFIX + '''
SELECT ?s ?o WHERE { {?s nmo:hasMint ?o.}  UNION {?s nmo:hasMint ?b.  ?b rdf:value ?o.} FILTER(!isBlank(?o))}
'''

S7Q4 = PREFIX + '''
SELECT ?s WHERE {?s nmo:hasMint ?o. FILTER(!isBlank(?o))} 
'''

S7Q5 = PREFIX + '''
SELECT ?s ?o WHERE {?s nmo:hasMint ?b . ?b rdf:type edtfo:UncertainStatement;  rdf:value ?o . }
'''
# SOLUTION QUERY S8
#______________________________________________________________________________________________
S8Q1 = PREFIX + '''
SELECT ?s WHERE {?s nmo:hasMint nm:comama. FILTER(!isBlank (?s))} 
'''

S8Q2 = PREFIX + '''
SELECT ?s  WHERE {{?s nmo:hasMint nm:comama.} 
          UNION{?s un:hasUncertainty ?b.  ?b nmo:hasMint nm:comama.}}  
'''

S8Q3 = PREFIX + '''
SELECT ?s ?o WHERE { {?s nmo:hasMint ?o.}  UNION {?s un:hasUncertainty ?b.  ?b nmo:hasMint ?o.} }  
'''

S8Q4 = PREFIX + '''
SELECT ?s WHERE {?s nmo:hasMint ?o. FILTER(!isBlank (?s))} 
'''

S8Q5 = PREFIX + '''
SELECT ?s ?o WHERE {?s un:hasUncertainty ?b . ?b nmo:hasMint ?o . }
'''

# SOLUTION QUERY RANDOM
#__________________________________________________________________________________________
S0Q0 = PREFIX + '''
SELECT ?s ?p ?o  WHERE { ?s ?p ?o}
'''

S1Q0 = PREFIX + '''
SELECT ?s ?p ?o  WHERE { ?s ?p ?o}
'''

S2Q0 = PREFIX + '''
SELECT ?s ?p ?o  WHERE { ?s ?p ?o}
'''

S3Q0 = PREFIX + '''
SELECT ?s ?p ?o  WHERE { ?s ?p ?o}
'''

S4Q0 = PREFIX + '''
SELECT ?s ?p ?o  WHERE { ?s ?p ?o}
'''
S5Q0 = PREFIX + '''
SELECT ?s ?p ?o  WHERE { ?s ?p ?o}
'''
S6Q0 = PREFIX + '''
SELECT ?s ?p ?o  WHERE { ?s ?p ?o}
'''
S7Q0 = PREFIX + '''
SELECT ?s ?p ?o  WHERE { ?s ?p ?o}
'''
S8Q0 = PREFIX + '''
SELECT ?s ?p ?o  WHERE { ?s ?p ?o}
'''
S9Q0 = PREFIX + '''
SELECT ?s ?p ?o  WHERE { ?s ?p ?o}
'''




