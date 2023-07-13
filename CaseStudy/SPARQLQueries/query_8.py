query_8 = prepareQuery(
    """
    PREFIX : <http://www.semanticweb.org/arnak/ontologies/2022/7/DOR#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix ex: <http://www.semanticweb.org/arnak/ontologies/2022/7/DOR#>
    
    SELECT DISTINCT ?entity ?Potential1
    WHERE {
        ?entity ex:hasCircularPotential ?CircularPotential .
        ?CircularPotential ex:hasCircularRequirement ?LegalRequirement .
        ex:Legal rdfs:subClassOf ?LegalRequirement .
    }
    """,
    initNs={"ex": ex, "rdfs": RDFS, "bpo": bpo}
)

# Execute the query
results = g.query(query_8)

## if len(results) > 0:
# Display the results
# for result in results:
# print(result)
# else:
# print("No results")

# Iterate over the results

for row in results:
    entity = row["entity"]
    LegalRequirement = row["LegalRequirement"]
    print(entity)
    print(LegalRequirement)