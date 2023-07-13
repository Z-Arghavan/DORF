from rdflib import Graph, Namespace, RDF, OWL, RDFS, BNode, URIRef, XSD, Literal
import rdflib.collection as coll
from rdflib.plugins.sparql import prepareQuery


#This query finds all the (1) Non reusable entities, and (2) potentially reusable entities 

query_4 = prepareQuery(
    """
    PREFIX ex: <http://www.semanticweb.org/arnak/ontologies/2022/7/DOR#>
    PREFIX bpo: <http://example.org/bpo#>
    PREFIX dicm: <http://example.org/dicm#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT (COUNT(?entity_zero) AS ?count_zero) (COUNT(?entity_nonzero) AS ?count_nonzero)
    WHERE {
        {
            SELECT ?entity_zero
            WHERE {
                ?entity_zero ex:hasRemainingReuseCount "0"^^xsd:int .
            }
        }
        UNION
        {
            SELECT ?entity_nonzero
            WHERE {
                ?entity_nonzero ex:hasRemainingReuseCount ?count .
                FILTER (?count != "0"^^xsd:int)
            }
        }
    }
    """,
    initNs={"ex": ex, "bpo": bpo, "dicm": dicm}
)

# Execute the query
results = g.query(query_4)

# Extract the count values from the results
for row in results:
    count_nonReusables = row["count_zero"]
    count_reusables = row["count_nonzero"]
    print("Count of entities with hasRemainingReuseCount = 0, which are  Not Reusable:", count_nonReusables)
    print("Count of entities with hasRemainingReuseCount != 0:,  which are Potentially Reusable:", count_reusables)