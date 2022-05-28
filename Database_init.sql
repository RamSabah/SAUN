CREATE DATABASE queries;
USE queries;
CREATE TABLE queries (
graph int,
querynumber int,
description text
);

INSERT INTO queries (graph, querynumber, description) VALUES(1,1,"RDF-Reification-Based Approach by CIDOC CRM");
INSERT INTO queries (graph, querynumber, description) VALUES(2,1,"Additional Resource Directly to the Property-Path, by Dr. Tolle & Dr. Wigg-Wolf.");
INSERT INTO queries (graph, querynumber, description) VALUES(3,1,"Assigning Reliability as a Sub-Class-of E16, by Prof. Niccolucci & Prof. Hermon");
INSERT INTO queries (graph, querynumber, description) VALUES(4,1,"Using Classes/Properties from CRMinf, by Prof. Niccolucci & Prof. Hermon");
INSERT INTO queries (graph, querynumber, description) VALUES(5,1,"Expanding CRM-Properties with the Property Class PC and .2 Properties, by Dr. Doerr.");
INSERT INTO queries (graph, querynumber, description) VALUES(6,1,"RDF-Reification with Extended Date/Time Format Ontology (EDTFO).");
INSERT INTO queries (graph, querynumber, description) VALUES(7,1,"Based on Solution 2 and Extended Date/Time Format Ontology (EDTFO)");
INSERT INTO queries (graph, querynumber, description) VALUES(8,1,"A New Approach Based on Using un:hasUncertainty");
select * from queries;