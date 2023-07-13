from rdflib import Graph, Namespace, RDF, OWL, RDFS, BNode, URIRef, XSD, Literal
import rdflib.collection as coll
from rdflib.plugins.sparql import prepareQuery

#This query shows what components are associate with the waste code 170101. 

query_5 = prepareQuery(
    """
    SELECT ?component
    WHERE {
      ?component rdf:type bpo:Component .
      ?entity rdf:type bpo:Entity .
      ?entity bpo:realisesObject ?component .
      ?entity dicm:hasMaterial ?material .
      ?material ex:hasWasteCode "170101"^^xsd:int .
    }
    """,
    initNs={"rdf": RDF, "bpo": bpo, "dicm": dicm, "ex": ex}
)

# Execute the query
results = g.query(query_5)

# Iterate over the results
for row in results:
    component = row["component"]
    print(component)