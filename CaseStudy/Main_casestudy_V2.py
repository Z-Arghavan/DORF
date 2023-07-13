from rdflib import Graph, Namespace, RDF, OWL, RDFS, BNode, URIRef, XSD, Literal
import rdflib.collection as coll
from rdflib.plugins.sparql import prepareQuery


# Define the namespaces

ex = Namespace("http://www.semanticweb.org/arnak/ontologies/2022/7/DOR#")
bot = Namespace("https://w3id.org/bot#")
bpo = Namespace("https://www.projekt-scope.de/ontologies/bpo/#")
dicm = Namespace(
    "https://digitalconstruction.github.io/BuildingMaterials/v/0.3/")

# Create a new RDF graph
g = Graph()


# Bind the prefix
g.bind("", ex)
g.bind("bot", bot)
g.bind("bpo", bpo)
g.bind("dicm", dicm)

########################################################### SHEAR CONNECTOR ASSEMBLY ##
# Create 288 instances of shear connectors
# small slabs have 8 shearonnectors-railchannels pairs and big slabs have 16 shearonnectors-railchannels pairs

# Add the triple to all entities
g.add((ex.ReusePotential_1, RDF.type, ex.ReusePotential))

g.add((ex.RepurposingPotential_1, RDF.type, ex.RepurposingPotential))

g.add((ex.ReManufacturingPotential_1, RDF.type, ex.ReManufacturingPotential))
g.add((ex.ReManufacturingPotential_1,
      ex.hasCircularRequirement, ex.Maintenance_every_10_years))
g.add((ex.Maintenance_every_10_years, RDF.type, ex.Intervention))

g.add((ex.ReusePotential_1, ex.hasCircularRequirement, ex.UnTrainned_1))
g.add((ex.UnTrainned_1, RDF.type, ex.UntrainnedPersonnel))

g.add((ex.ReusePotential_2, ex.hasCircularRequirement, ex.Trainned_1))
g.add((ex.Trainned_1, RDF.type, ex.TrainnedPersonnel))

g.add((ex.RecyclingPotential_1, RDF.type, ex.RecyclingPotential))
g.add((ex.RecyclingPotential_1, ex.hasCircularRequirement, ex.Legal_Req_super))
g.add((ex.Legal_Req_super, RDF.type, ex.CircularPotential))
g.add((ex.Legal_Req_super_1, RDF.type, ex.Legal))
g.add((ex.Legal, RDFS.subClassOf, ex.Legal_Req_super))

g.add((ex.RecyclingPotential_2, RDF.type, ex.RecyclingPotential))

# Create multiple instances of shear connectors
shear_connector_count = 288
Simply_Supported_railplates = []
Continuous_railplates = []

for i in range(1, shear_connector_count + 1):
    shear_connector_uri = ex.shear_connector + "_" + str(i)
    # Define the instances of : Part
    g.add((shear_connector_uri, RDF.type, bpo.Assembly))
    g.add((shear_connector_uri, ex.hasCircularPotential,
          ex.ReManufacturingPotential_1_))

    # Define the backplate, rail plate, washer, discspring and bolt as sub-parts of each shear connector:
    backplate_count = 1
    railplate_count = 1
    washer_count = 1
    discspring_count = 1
    bolt_count = 1

    backplate_uri = ex.backplate + "_" + str(i)
    railplate_uri = ex.railplate + "_" + str(i)
    washer_uri = ex.washer + "_" + str(i)
    discspring_uri = ex.discspring + "_" + str(i)
    bolt_uri = ex.bolt + "_" + str(i)

    # Define the sub parts of sehar connector as element types:
    g.add((backplate_uri, RDF.type, bpo.Element))
    g.add((railplate_uri, RDF.type, bpo.Element))
    g.add((washer_uri, RDF.type, bpo.Element))
    g.add((discspring_uri, RDF.type, bpo.Element))
    g.add((bolt_uri, RDF.type, bpo.Element))

    # Define relationship between whole and part (inverse relationships: bpo.consistsOf and bpo.isPartOf)
    # Each shear connector is consisted of one backplate, one rail plate, one washer, one discspring and one bolt
    g.add((shear_connector_uri, bpo.consistsOf, backplate_uri))
    g.add((shear_connector_uri, bpo.consistsOf, railplate_uri))
    g.add((shear_connector_uri, bpo.consistsOf, washer_uri))
    g.add((shear_connector_uri, bpo.consistsOf, discspring_uri))
    g.add((shear_connector_uri, bpo.consistsOf, bolt_uri))

    g.add((backplate_uri, bpo.isPartOf, shear_connector_uri))
    g.add((railplate_uri, bpo.isPartOf, shear_connector_uri))
    g.add((washer_uri, bpo.isPartOf, shear_connector_uri))
    g.add((discspring_uri, bpo.isPartOf, shear_connector_uri))
    g.add((bolt_uri, bpo.isPartOf, shear_connector_uri))


    #This part I added in the last step. This is for definign connection type:
    Connection_between_railplate_and_simply_railchannel_uri = ex.Connection_between_railplate_and_simply_railchannel
    ConnectionType_1 = ex.ConnectionType_1

    for j in range(1, backplate_count + 1):
        backplate_ent_uri = ex.backplate_ent + "_" + str(i) + "_" + str(j)
        g.add((backplate_ent_uri, RDF.type, bpo.Entity))
        g.add((backplate_ent_uri, bpo.realisesObject, backplate_uri))
        g.add((shear_connector_uri, bpo.isComposedOfEntity, backplate_ent_uri))
        # Add DOR properties for each backplate_ent_uri
        g.add((backplate_ent_uri, RDF.type, OWL.NamedIndividual))
        g.add((backplate_ent_uri, ex.hasCircularPotential,  ex.ReusePotential_1))
        g.add((backplate_ent_uri, ex.hasTotalReuseCount,
              Literal(3, datatype=XSD.int)))
        g.add((backplate_ent_uri, ex.hasRemainingReuseCount,
              Literal(2, datatype=XSD.int)))
        g.add((backplate_ent_uri, ex.hasCurrentUseCount,
              Literal(1, datatype=XSD.int)))
        g.add((backplate_ent_uri, ex.hasFinalCircularPotential, ex.RecyclingPotential_2))
        # Add DICM and DOR Material
        g.add((backplate_ent_uri, dicm.hasMaterial, ex.SteelSectionSteel_e))
        # Add the RecyclingPotential triples

    for k in range(1, railplate_count + 1):
        railplate_ent_uri = ex.railplate_ent + "_" + str(i) + "_" + str(k)
        g.add((railplate_ent_uri, RDF.type, bpo.Entity))
        g.add((railplate_ent_uri, bpo.realisesObject, railplate_uri))
        g.add((shear_connector_uri, bpo.isComposedOfEntity, railplate_ent_uri))
        # Add DOR properties for each railplate_ent_uri
        g.add((railplate_ent_uri, RDF.type, OWL.NamedIndividual))
        g.add((railplate_ent_uri, ex.hasCircularPotential,  ex.ReusePotential_1))
        g.add((railplate_ent_uri, ex.hasTotalReuseCount,
              Literal(3, datatype=XSD.int)))
        g.add((railplate_ent_uri, ex.hasRemainingReuseCount,
              Literal(2, datatype=XSD.int)))
        g.add((railplate_ent_uri, ex.hasCurrentUseCount,
              Literal(1, datatype=XSD.int)))
        g.add((railplate_ent_uri, ex.hasFinalCircularPotential, ex.RecyclingPotential_1))
        # Add DICM and DOR Material
        g.add((railplate_ent_uri, dicm.hasMaterial, ex.SteelSectionSteel_e))
        # Add the ReusePotential triples
        # Assign railplate entities to shear connectors based on slab type
               

    for l in range(1, washer_count + 1):
        washer_ent_uri = ex.washer_ent + "_" + str(i) + "_" + str(l)
        g.add((washer_ent_uri, RDF.type, bpo.Entity))
        g.add((washer_ent_uri, bpo.realisesObject, washer_uri))
        g.add((shear_connector_uri, bpo.isComposedOfEntity, washer_ent_uri))
        # Add DOR properties for each washer_ent_uri
        g.add((washer_ent_uri, RDF.type, OWL.NamedIndividual))
        g.add((washer_ent_uri, ex.hasCircularPotential,  ex.ReusePotential_1))
        g.add((washer_ent_uri, ex.hasTotalReuseCount, Literal(3, datatype=XSD.int)))
        g.add((washer_ent_uri, ex.hasRemainingReuseCount,
              Literal(2, datatype=XSD.int)))
        g.add((washer_ent_uri, ex.hasCurrentUseCount, Literal(1, datatype=XSD.int)))
        g.add((washer_ent_uri, ex.hasFinalCircularPotential, ex.RecyclingPotential_2))
        # Add DICM and DOR Material
        g.add((washer_ent_uri, dicm.hasMaterial, ex.GalvanaisedSteel_c))

    for m in range(1, discspring_count + 1):
        discspring_ent_uri = ex.discspring_ent + "_" + str(i) + "_" + str(m)
        g.add((discspring_ent_uri, RDF.type, bpo.Entity))
        g.add((discspring_ent_uri, bpo.realisesObject, discspring_uri))
        g.add((shear_connector_uri, bpo.isComposedOfEntity, discspring_ent_uri))
        # Add DOR properties for each discspring_ent_uri
        g.add((discspring_ent_uri, RDF.type, OWL.NamedIndividual))
        g.add((discspring_ent_uri, ex.hasCircularPotential,  ex.ReusePotential_1))
        g.add((discspring_ent_uri, ex.hasTotalReuseCount,
              Literal(3, datatype=XSD.int)))
        g.add((discspring_ent_uri, ex.hasRemainingReuseCount,
              Literal(2, datatype=XSD.int)))
        g.add((discspring_ent_uri, ex.hasCurrentUseCount,
              Literal(1, datatype=XSD.int)))
        g.add((discspring_ent_uri, ex.hasFinalCircularPotential,
              ex.RecyclingPotential_2))
        # Add DICM and DOR Material
        g.add((discspring_ent_uri, dicm.hasMaterial, ex.GalvanaisedSteel_c))

    for n in range(1, bolt_count + 1):
        bolt_ent_uri = ex.bolt_ent + "_" + str(i) + "_" + str(n)
        g.add((bolt_ent_uri, RDF.type, bpo.Entity))
        g.add((bolt_ent_uri, bpo.realisesObject, bolt_uri))
        g.add((shear_connector_uri, bpo.isComposedOfEntity, bolt_ent_uri))
        # Add DOR properties for each bolt_ent_uri
        g.add((bolt_ent_uri, RDF.type, OWL.NamedIndividual))
        g.add((bolt_ent_uri, ex.hasCircularPotential, ex.RecyclingPotential_1))
        g.add((bolt_ent_uri, ex.hasTotalReuseCount, Literal(1, datatype=XSD.int)))
        g.add((bolt_ent_uri, ex.hasRemainingReuseCount,
              Literal(0, datatype=XSD.int)))
        g.add((bolt_ent_uri, ex.hasCurrentUseCount, Literal(1, datatype=XSD.int)))
        g.add((bolt_ent_uri, ex.hasFinalCircularPotential, ex.RecyclingPotential_1))
        # Add DICM and DOR Material
        g.add((bolt_ent_uri, dicm.hasMaterial, ex.GalvanaisedSteel_c))
        # Each instance of bolt entity is connected to its equivalent washer, railpalte,discspring and backplate entity
        g.add((washer_ent_uri, bpo.isConnectedWith, bolt_ent_uri))
        g.add((bolt_ent_uri, bpo.isConnectedWith, washer_ent_uri))
        g.add((bolt_ent_uri, bpo.isConnectedWith, discspring_ent_uri))
        g.add((discspring_ent_uri, bpo.isConnectedWith, bolt_ent_uri))
        g.add((bolt_ent_uri, bpo.isConnectedWith, backplate_ent_uri))
        g.add((backplate_ent_uri, bpo.isConnectedWith, bolt_ent_uri))
        g.add((bolt_ent_uri, bpo.isConnectedWith, railplate_ent_uri))
        g.add((railplate_ent_uri, bpo.isConnectedWith, bolt_ent_uri))

########################################################### CONCRETE SLABS_SIMPLY SUPPORTED MODULE ##

# In the Floor System, we have 6 small slabs and 15 big slabs. small slabs have 8 railchannels and big slabs have 16 railschannels.
# Each railchannel corresponds to one shear connector.
# Each Floor system is supported by 2 primary beams and 7 secondary beams


# Create multiple instances of concrete slabs
Simply_Supported_slab_count = 6
Simply_Supported_slab_railchannel_count = 8


for o in range(1, Simply_Supported_slab_count + 1):
    Simply_Supported_concrete_slab_uri = ex.Simply_Supported_concrete_slab + \
        "_" + str(o)
    g.add((Simply_Supported_concrete_slab_uri, RDF.type, bpo.Assembly))

    # Define the rebars, rail channels, and casted concrete as sub-parts of each concrete slab:
    Simply_Supported_slab_castedconcrete_count = 1
    Simply_Supported_slab_rebar_count = 25

    for p in range(1, Simply_Supported_slab_rebar_count + 1):
        Simply_Supported_slab_rebar_uri = ex.Simply_Supported_slab_rebar + \
            "_" + str(o)
        Simply_Supported_slab_rebar_ent_uri = ex.Simply_Supported_slab_rebar_ent + \
            "_" + str(o) + "_" + str(p)

        g.add((Simply_Supported_slab_rebar_uri, RDF.type, bpo.Element))
        g.add((Simply_Supported_slab_rebar_ent_uri, RDF.type, bpo.Entity))
        g.add((Simply_Supported_slab_rebar_ent_uri,
              bpo.realisesObject, Simply_Supported_slab_rebar_uri))

        g.add((Simply_Supported_concrete_slab_uri,
              bpo.consistsOf, Simply_Supported_slab_rebar_uri))
        g.add((Simply_Supported_concrete_slab_uri,
              bpo.isComposedOfEntity, Simply_Supported_slab_rebar_ent_uri))
        g.add((Simply_Supported_slab_rebar_uri, bpo.isPartOf,
              Simply_Supported_concrete_slab_uri))

        # Add DOR properties for each rebar_ent_uri
        g.add((Simply_Supported_slab_rebar_ent_uri, RDF.type, OWL.NamedIndividual))
        g.add((Simply_Supported_slab_rebar_ent_uri,
              ex.hasCircularPotential, ex.ReusePotential_2))
        g.add((Simply_Supported_slab_rebar_ent_uri,
              ex.hasTotalReuseCount, Literal(3, datatype=XSD.int)))
        g.add((Simply_Supported_slab_rebar_ent_uri, ex.hasRemainingReuseCount,
              Literal(2, datatype=XSD.int)))
        g.add((Simply_Supported_slab_rebar_ent_uri,
              ex.hasCurrentUseCount, Literal(1, datatype=XSD.int)))
        g.add((Simply_Supported_slab_rebar_ent_uri,
              ex.hasFinalCircularPotential, ex.RecyclingPotential_2))

        # Add DICM and DOR Material
        g.add((Simply_Supported_slab_rebar_ent_uri,
              dicm.hasMaterial, ex.ReinforcementSteel_d))

    for q in range(1, Simply_Supported_slab_railchannel_count + 1):
        Simply_Supported_slab_railchannel_uri = ex.Simply_Supported_slab_railchannel + \
            "_" + str(o)
        Simply_Supported_slab_railchannel_ent_uri = ex.Simply_Supported_slab_railchannel_ent + \
            "_" + str(o) + "_" + str(q)

        g.add((Simply_Supported_slab_railchannel_uri, RDF.type, bpo.Element))
        g.add((Simply_Supported_slab_railchannel_ent_uri, RDF.type, bpo.Entity))
        g.add((Simply_Supported_slab_railchannel_ent_uri,
              bpo.realisesObject, Simply_Supported_slab_railchannel_uri))

        g.add((Simply_Supported_concrete_slab_uri,
              bpo.consistsOf, Simply_Supported_slab_railchannel_uri))
        g.add((Simply_Supported_concrete_slab_uri,
              bpo.isComposedOfEntity, Simply_Supported_slab_railchannel_ent_uri))
        g.add((Simply_Supported_slab_railchannel_uri,
              bpo.isPartOf, Simply_Supported_concrete_slab_uri))

        # Add DOR properties for each railchannel_ent_uri
        g.add((Simply_Supported_slab_railchannel_ent_uri,
              RDF.type, OWL.NamedIndividual))
        g.add((Simply_Supported_slab_railchannel_ent_uri,
              ex.hasCircularPotential, ex.ReusePotential_1))
        g.add((Simply_Supported_slab_railchannel_ent_uri, ex.hasTotalReuseCount,
              Literal(3, datatype=XSD.int)))
        g.add((Simply_Supported_slab_railchannel_ent_uri, ex.hasRemainingReuseCount,
              Literal(2, datatype=XSD.int)))
        g.add((Simply_Supported_slab_railchannel_ent_uri, ex.hasCurrentUseCount,
              Literal(1, datatype=XSD.int)))
        g.add((Simply_Supported_slab_railchannel_ent_uri, ex.hasFinalCircularPotential,
              ex.RecyclingPotential_2))
        # Add the RecyclingPotential triples
        # Add DICM and DOR Material
        g.add((Simply_Supported_slab_railchannel_ent_uri,
              dicm.hasMaterial, ex.SteelSectionSteel_e))
        if (o - 1) * Simply_Supported_slab_railchannel_count + q <= Simply_Supported_slab_count * Simply_Supported_slab_railchannel_count:
            railplate_ent_uri = ex.railplate_ent + "_" + str((o - 1) * Simply_Supported_slab_railchannel_count + q) + "_1"
            g.add((railplate_ent_uri, bpo.isConnectedWith, Simply_Supported_slab_railchannel_ent_uri))
            g.add((Simply_Supported_slab_railchannel_ent_uri, bpo.isConnectedWith, railplate_ent_uri))
            g.add((railplate_ent_uri, bpo.hasOutgoingConnection, Connection_between_railplate_and_simply_railchannel_uri ))
            g.add((Connection_between_railplate_and_simply_railchannel_uri, bpo.connectsInputOf, railplate_ent_uri))
            g.add((Connection_between_railplate_and_simply_railchannel_uri, RDF.type, bpo.ComponentConnection))
            g.add((Connection_between_railplate_and_simply_railchannel_uri, ex.hasConnectionType, ConnectionType_1))
            g.add((ConnectionType_1, RDF.type, ex.ReversibleConnection,))
        

for r in range(1, Simply_Supported_slab_castedconcrete_count + 1):
    Simply_Supported_slab_castedconcrete_uri = ex.Simply_Supported_slab_castedconcrete + \
        "_" + str(o)
    Simply_Supported_slab_castedconcrete_ent_uri = ex.Simply_Supported_slab_castedconcrete_ent + \
        "_" + str(o) + "_" + str(r)

    g.add((Simply_Supported_slab_castedconcrete_uri, RDF.type, bpo.Component))
    g.add((Simply_Supported_slab_castedconcrete_ent_uri, RDF.type, bpo.Entity))
    g.add((Simply_Supported_slab_castedconcrete_ent_uri,
          bpo.realisesObject, Simply_Supported_slab_castedconcrete_uri))

    g.add((Simply_Supported_concrete_slab_uri, bpo.consistsOf,
          Simply_Supported_slab_castedconcrete_uri))
    g.add((Simply_Supported_concrete_slab_uri,
          bpo.isComposedOfEntity, Simply_Supported_slab_castedconcrete_ent_uri))
    g.add((Simply_Supported_slab_castedconcrete_uri,
          bpo.isPartOf, Simply_Supported_concrete_slab_uri))

    # Add DOR properties for each railchannel_ent_uri
    g.add((Simply_Supported_slab_castedconcrete_ent_uri,
          RDF.type, OWL.NamedIndividual))
    g.add((Simply_Supported_slab_castedconcrete_ent_uri,
          ex.hasCircularPotential, ex.ReusePotential_1))
    g.add((Simply_Supported_slab_castedconcrete_ent_uri, ex.hasTotalReuseCount,
          Literal(3, datatype=XSD.int)))
    g.add((Simply_Supported_slab_castedconcrete_ent_uri, ex.hasRemainingReuseCount,
          Literal(2, datatype=XSD.int)))
    g.add((Simply_Supported_slab_castedconcrete_ent_uri, ex.hasCurrentUseCount,
          Literal(1, datatype=XSD.int)))
    g.add((Simply_Supported_slab_castedconcrete_ent_uri, ex.hasFinalCircularPotential,
          ex.RepurposingPotential_1))

    # Add DICM and DOR Material
    g.add((Simply_Supported_slab_castedconcrete_ent_uri,
          dicm.hasMaterial, ex.ready_mix_concret))


########################################################### CONCRETE SLABS_continuous MODULE ##

# In the Floor System, we have 6 small slabs and 15 big slabs. small slabs have 8 railchannels and big slabs have 16 railschannels.
# Each railchannel corresponds to one shear connector.
# Each Floor system is supported by 2 primary beams and 7 secondary beams

# Create multiple instances of concrete slabs
Continuous_slab_count = 15
Continuous_slab_rebar_count = 25
Continuous_slab_railchannel_count = 16
Continuous_slab_castedconcrete_count = 1

for i in range(1, Continuous_slab_count + 1):
    Continuous_concrete_slab_uri = ex.Continuous_concrete_slab + "_" + str(i)
    g.add((Continuous_concrete_slab_uri, RDF.type, bpo.Assembly))

    # Define the rebars, rail channels, and casted concrete as sub-parts of each concrete slab:

    for j in range(1, Continuous_slab_rebar_count + 1):
        Continuous_slab_rebar_uri = ex.Continuous_slab_rebar + "_" + str(i)
        Continuous_slab_rebar_ent_uri = ex.Continuous_slab_rebar_ent + \
            "_" + str(i) + "_" + str(j)

        g.add((Continuous_slab_rebar_uri, RDF.type, bpo.Element))
        g.add((Continuous_slab_rebar_ent_uri, RDF.type, bpo.Entity))
        g.add((Continuous_slab_rebar_ent_uri,
              bpo.realisesObject, Continuous_slab_rebar_uri))

        g.add((Continuous_concrete_slab_uri,
              bpo.consistsOf, Continuous_slab_rebar_uri))
        g.add((Continuous_concrete_slab_uri, bpo.isComposedOfEntity,
              Continuous_slab_rebar_ent_uri))
        g.add((Continuous_slab_rebar_uri, bpo.isPartOf,
              Continuous_concrete_slab_uri))

        # Add DOR properties for each rebar_ent_uri
        g.add((Continuous_slab_rebar_ent_uri, RDF.type, OWL.NamedIndividual))
        g.add((Continuous_slab_rebar_ent_uri,
              ex.hasCircularPotential, ex.ReusePotential_2))
        g.add((Continuous_slab_rebar_ent_uri,
              ex.hasTotalReuseCount, Literal(3, datatype=XSD.int)))
        g.add((Continuous_slab_rebar_ent_uri, ex.hasRemainingReuseCount,
              Literal(2, datatype=XSD.int)))
        g.add((Continuous_slab_rebar_ent_uri,
              ex.hasCurrentUseCount, Literal(1, datatype=XSD.int)))
        g.add((Continuous_slab_rebar_ent_uri,
              ex.hasFinalCircularPotential, ex.RecyclingPotential_2))

        # Add DICM and DOR Material
        g.add((Continuous_slab_rebar_ent_uri,
              dicm.hasMaterial, ex.ReinforcementSteel_d))

    for k in range(1, Continuous_slab_railchannel_count + 1):
        Continuous_slab_railchannel_uri = ex.Continuous_slab_railchannel + \
            "_" + str(i)
        Continuous_slab_railchannel_ent_uri = ex.Continuous_slab_railchannel_ent + \
            "_" + str(i) + "_" + str(k)

        g.add((Continuous_slab_railchannel_uri, RDF.type, bpo.Element))
        g.add((Continuous_slab_railchannel_ent_uri, RDF.type, bpo.Entity))
        g.add((Continuous_slab_railchannel_ent_uri,
              bpo.realisesObject, Continuous_slab_railchannel_uri))

        g.add((Continuous_concrete_slab_uri, bpo.consistsOf,
              Continuous_slab_railchannel_uri))
        g.add((Continuous_concrete_slab_uri,
              bpo.isComposedOfEntity, Continuous_slab_railchannel_ent_uri))
        g.add((Continuous_slab_railchannel_uri,
              bpo.isPartOf, Continuous_concrete_slab_uri))

        # Add DOR properties for each railchannel_ent_uri
        g.add((Continuous_slab_railchannel_ent_uri, RDF.type, OWL.NamedIndividual))
        g.add((Continuous_slab_railchannel_ent_uri,
              ex.hasCircularPotential, ex.ReusePotential_1))
        g.add((Continuous_slab_railchannel_ent_uri, ex.hasTotalReuseCount,
              Literal(3, datatype=XSD.int)))
        g.add((Continuous_slab_railchannel_ent_uri, ex.hasRemainingReuseCount,
              Literal(2, datatype=XSD.int)))
        g.add((Continuous_slab_railchannel_ent_uri, ex.hasCurrentUseCount,
              Literal(1, datatype=XSD.int)))
        g.add((Continuous_slab_railchannel_ent_uri, ex.hasFinalCircularPotential,
              ex.RecyclingPotential_2))

        # Add DICM and DOR Material
        g.add((Continuous_slab_railchannel_ent_uri,
              dicm.hasMaterial, ex.SteelSectionSteel_e))
        # Connect railplate_ent_uri with Continuous_slab_railchannel_ent_uri
        railplate_ent_uri = ex.railplate_ent + "_" + str((i - 1) * Continuous_slab_railchannel_count + k)
        g.add((railplate_ent_uri, bpo.isConnectedWith, Continuous_slab_railchannel_ent_uri))
        g.add((Continuous_slab_railchannel_ent_uri, bpo.isConnectedWith, railplate_ent_uri))




    for l in range(1, Continuous_slab_castedconcrete_count + 1):
        Continuous_slab_castedconcrete_uri = ex.castedconcrete + "_" + str(i)
        Continuous_slab_castedconcrete_ent_uri = ex.castedconcrete_ent + \
            "_" + str(i) + "_" + str(l)

        g.add((Continuous_slab_castedconcrete_uri, RDF.type, bpo.Component))
        g.add((Continuous_slab_castedconcrete_ent_uri, RDF.type, bpo.Entity))
        g.add((Continuous_slab_castedconcrete_ent_uri,
              bpo.realisesObject, Continuous_slab_castedconcrete_uri))

        g.add((Continuous_concrete_slab_uri, bpo.consistsOf,
              Continuous_slab_castedconcrete_uri))
        g.add((Continuous_concrete_slab_uri,
              bpo.isComposedOfEntity, Continuous_slab_castedconcrete_ent_uri))
        g.add((Continuous_slab_castedconcrete_uri,
              bpo.isPartOf, Continuous_concrete_slab_uri))

        # Add DOR properties for each railchannel_ent_uri
        g.add((Continuous_slab_castedconcrete_ent_uri,
              RDF.type, OWL.NamedIndividual))
        g.add((Continuous_slab_castedconcrete_ent_uri,
              ex.hasCircularPotential, ex.ReusePotential_1))
        g.add((Continuous_slab_castedconcrete_ent_uri, ex.hasTotalReuseCount,
              Literal(3, datatype=XSD.int)))
        g.add((Continuous_slab_castedconcrete_ent_uri, ex.hasRemainingReuseCount,
              Literal(2, datatype=XSD.int)))
        g.add((Continuous_slab_castedconcrete_ent_uri, ex.hasCurrentUseCount,
              Literal(1, datatype=XSD.int)))
        g.add((Continuous_slab_castedconcrete_ent_uri, ex.hasFinalCircularPotential,
              ex.RepurposingPotential_1))

        # Add DICM and DOR Material
        g.add((Continuous_slab_castedconcrete_ent_uri,
              dicm.hasMaterial, ex.ready_mix_concret))

        # Connect railplate_ent_uri with Continuous_slab_railchannel_ent_uri
        railplate_ent_uri = ex.railplate_ent + "_" + str((i - 1) * Continuous_slab_railchannel_count + k)
        g.add((railplate_ent_uri, bpo.isConnectedWith, Continuous_slab_railchannel_ent_uri))
        g.add((Continuous_slab_railchannel_ent_uri, bpo.isConnectedWith, railplate_ent_uri))



########################################################### PRIMARY BEAM ##


# Create multiple instances of primary beams
primary_beam_count = 2
for i in range(1, primary_beam_count + 1):
    primary_beam_uri = ex.primary_beam + "_" + str(i)
    g.add((primary_beam_uri, RDF.type, bpo.component))

    # Define the primary_beam as a single Element
    primary_beam_ent_count = 1
    primary_beam_uri = ex.primary_beam + "_" + str(i)

    # Define the sub parts of primary_beam as element types:
    g.add((primary_beam_uri, RDF.type, bpo.Element))

    for j in range(1, primary_beam_ent_count + 1):
        primary_beam_ent_uri = ex.primary_beam_ent + \
            "_" + str(i) + "_" + str(j)
        g.add((primary_beam_ent_uri, RDF.type, bpo.Entity))
        g.add((primary_beam_ent_uri, bpo.realisesObject, primary_beam_uri))
        # Add DOR properties for each primary_beam_ent_uri
        g.add((primary_beam_ent_uri, RDF.type, OWL.NamedIndividual))
        g.add((primary_beam_ent_uri, ex.hasCircularPotential, ex.ReusePotential_1))
        g.add((primary_beam_ent_uri, ex.hasTotalReuseCount,
              Literal(3, datatype=XSD.int)))
        g.add((primary_beam_ent_uri, ex.hasRemainingReuseCount,
              Literal(2, datatype=XSD.int)))
        g.add((primary_beam_ent_uri, ex.hasCurrentUseCount,
              Literal(1, datatype=XSD.int)))
        g.add((primary_beam_ent_uri, ex.hasFinalCircularPotential,
              ex.RecyclingPotential_2))
        # Add DICM and DOR Material
        g.add((primary_beam_ent_uri, dicm.hasMaterial, ex.Steel_a))


########################################################### SECONDARY BEAM ##


# Create multiple instances of secondary beam
secondary_beam_count = 7
for i in range(1, secondary_beam_count + 1):
    secondary_beam_uri = ex.secondary_beam + "_" + str(i)
    g.add((secondary_beam_uri, RDF.type, bpo.component))

    # Define the secondary_beam as a single Element
    secondary_beam_ent_count = 1
    secondary_beam_uri = ex.secondary_beam + "_" + str(i)

    # Define the sub parts of secondary_beam as element types:
    g.add((secondary_beam_uri, RDF.type, bpo.Element))

    for j in range(1, secondary_beam_ent_count + 1):
        secondary_beam_ent_uri = ex.secondary_beam_ent + \
            "_" + str(i) + "_" + str(j)
        g.add((secondary_beam_ent_uri, RDF.type, bpo.Entity))
        g.add((secondary_beam_ent_uri, bpo.realisesObject, secondary_beam_uri))
        # Add DOR properties for each primary_beam_ent_uri
        g.add((secondary_beam_ent_uri, RDF.type, OWL.NamedIndividual))
        g.add((secondary_beam_ent_uri, ex.hasCircularPotential, ex.ReusePotential_1))
        g.add((secondary_beam_ent_uri, ex.hasTotalReuseCount,
              Literal(3, datatype=XSD.int)))
        g.add((secondary_beam_ent_uri, ex.hasRemainingReuseCount,
              Literal(2, datatype=XSD.int)))
        g.add((secondary_beam_ent_uri, ex.hasCurrentUseCount,
              Literal(1, datatype=XSD.int)))
        g.add((secondary_beam_ent_uri,
              ex.hasFinalCircularPotential, ex.RecyclingPotential_2))
        # Add DICM and DOR Material
        g.add((secondary_beam_ent_uri, dicm.hasMaterial, ex.Steel_b))
        # Add connection between primary beam and secondary beam
        for k in range(1, primary_beam_count + 1):
            primary_beam_ent_uri = ex.primary_beam_ent + "_" + str(k) + "_1"
            g.add((secondary_beam_ent_uri, bpo.isConnectedWith, primary_beam_ent_uri))
            g.add((primary_beam_ent_uri, bpo.isConnectedWith, secondary_beam_ent_uri))

# Define and Link PrimaryBeam and SecondaryBeam to Steel MATERIAL, one material is sourced from recycled steel and the other is not.
# Structural_steel: https://oekobaudat.de/OEKOBAU.DAT/datasetdetail/process.xhtml?uuid=d4ca0d80-54a4-44b6-9fda-2cbbf82ea0d4&version=20.21.060&stock=OBD_2021_II&lang=en


# STEEL MATERIAL
# Create first blank node
bn2 = BNode()
bn4 = BNode()
g.add((bn2, RDF.type, OWL.Class))
g.add((bn4, RDF.type, OWL.Class))

# create intersectionOf 'RecyclableMaterial' and 'SecondaryRawMaterial'
coll.Collection(g, bn2, [ex.RecyclableMaterial, ex.SecondaryRawMaterial])
coll.Collection(g, bn4, [ex.RecyclableMaterial, ex.PrimaryRawMaterial])


bn1 = BNode()
bn3 = BNode()
g.add((bn1, RDF.type, OWL.Class))
g.add((bn1, OWL.intersectionOf, bn2))

g.add((bn3, RDF.type, OWL.Class))
g.add((bn3, OWL.intersectionOf, bn4))

# Define individuals
g.add((ex.Steel_b, RDF.type, dicm.Material))
g.add((ex.Steel_b, ex.hasSourceType, bn3))
g.add((ex.Steel_b, ex.hasWasteCode, Literal(170405, datatype=XSD.int)))


g.add((ex.Steel_a, RDF.type, dicm.Material))
g.add((ex.Steel_a, ex.hasSourceType, bn1))
g.add((ex.Steel_a, ex.hasWasteCode, Literal(170405, datatype=XSD.int)))


# aa = BNode()
# g.add((aa, RDF.type, OWL.Class))
# coll.Collection(g, aa, [ex.B, ex.C])
# bn1 = BNode()
# g.add((bn1, RDF.type, OWL.Class))
# g.add((bn1, OWL.intersectionOf, aa))
# https://stackoverflow.com/questions/76198709/rdflib-owl-restriction-with-intersection-in-pretty-xml-format


# Concrete Material used in LCA study: https://oekobaudat.de/OEKOBAU.DAT/datasetdetail/process.xhtml?uuid=923e1c71-f172-4902-a5f5-c4a1e8a773bc&version=20.21.060&stock=OBD_2021_II&lang=en
# CONCRETE MATERILA
# Create first blank node
bn6 = BNode()
g.add((bn6, RDF.type, OWL.Class))

# create intersectionOf 'NONRecyclableMaterial' and 'NONRenewableMaterial'
coll.Collection(g, bn6, [ex.NonRecyclableMaterial, ex.NonRenewableMaterial])

bn5 = BNode()
g.add((bn5, RDF.type, OWL.Class))
g.add((bn5, OWL.intersectionOf, bn6))


# Define individuals
# Define Ready_Mix_C2025 as a dicm:Material
g.add((ex.ready_mix_concret, RDF.type, dicm.Material))
g.add((ex.ready_mix_concret, ex.hasSourceType, bn5))
# Assign waste code to Ready_Mix_C2025
g.add((ex.ready_mix_concret, ex.hasWasteCode, Literal(170101, datatype=XSD.int)))


# Note for Shear Connection Materials

# There are two groups of parts for bolt material.
# One is produced and recycled at each life cycle: 0.49 (bolt+nut)
# One is reused each life cycle (like steel or concrete slabs): 0.217 (disc springs and washers)
# According to that they should have two different impact calculation paths but you did it already.
# It means only that bolt+nut we have to reproduce each cycle and springs+washers we will reuse always.


# STEEL MATERIAL
# Create first blank node
bn8 = BNode()
g.add((bn8, RDF.type, OWL.Class))

# create intersectionOf 'RecyclableMaterial' and 'SecondaryRawMaterial'
coll.Collection(g, bn8, [ex.RecyclableMaterial, ex.PrimaryRawMaterial])
bn7 = BNode()
g.add((bn7, RDF.type, OWL.Class))
g.add((bn7, OWL.intersectionOf, bn8))

# Bolt material: Galvanized steel screws: https://oekobaudat.de/OEKOBAU.DAT/datasetdetail/process.xhtml?uuid=f9caaa66-88c9-4a65-8718-a15aec11fd8b&version=20.21.060&stock=OBD_2021_II&lang=en
g.add((ex.GalvanaisedSteel_c, RDF.type, dicm.Material))
g.add((ex.GalvanaisedSteel_c, ex.hasSourceType, bn7))
g.add((ex.GalvanaisedSteel_c, ex.hasWasteCode, Literal(170405, datatype=XSD.int)))

# Rebar material: Reinforcement steel wire; wire: https://oekobaudat.de/OEKOBAU.DAT/datasetdetail/process.xhtml?uuid=e9ae96ee-ba8d-420d-9725-7c8abd06e082&version=20.19.120&stock=OBD_2021_II&lang=en
g.add((ex.ReinforcementSteel_d, RDF.type, dicm.Material))
g.add((ex.ReinforcementSteel_d, ex.hasSourceType, bn7))
g.add((ex.ReinforcementSteel_d, ex.hasWasteCode, Literal(170405, datatype=XSD.int)))


# Steel Section: Structural Steel: https://oekobaudat.de/OEKOBAU.DAT/datasetdetail/process.xhtml?uuid=5cb2c568-76fe-4803-8b46-0084e79800c8&version=00.14.000&stock=OBD_2021_II&lang=en
g.add((ex.SteelSectionSteel_e, RDF.type, dicm.Material))
g.add((ex.SteelSectionSteel_e, ex.hasSourceType, bn7))
g.add((ex.SteelSectionSteel_e, ex.hasWasteCode, Literal(170405, datatype=XSD.int)))


########################################################### DOR ONTOLOGY ##


# ___________________________________________________________ OBJECT PROPERTY

g.add((ex.auditsFor, RDF.type, OWL.ObjectProperty))
g.add((ex.auditsFor, RDFS.domain, ex.PreDeconstructionAuditor))
g.add((ex.auditsFor, RDFS.range, ex.CircularPotential))

g.add((ex.designsFor, RDF.type, OWL.ObjectProperty))
g.add((ex.designsFor, RDFS.domain, ex.Designer))
g.add((ex.designsFor, RDFS.range, ex.CircularPotential))

g.add((ex.producesFor, RDF.type, OWL.ObjectProperty))
g.add((ex.producesFor, RDFS.domain, ex.Manufacturer))
g.add((ex.producesFor, RDFS.range, ex.CircularPotential))

g.add((ex.recertifiesFor, RDF.type, OWL.ObjectProperty))
g.add((ex.recertifiesFor, RDFS.domain, ex.MaterialBankAgent))
g.add((ex.recertifiesFor, RDFS.range, ex.CircularPotential))

g.add((ex.connectionTo, RDF.type, OWL.ObjectProperty))
g.add((ex.connectionTo, OWL.inverseOf, ex.hasConnection))
g.add((ex.connectionTo, RDFS.range, bpo.Product))


union_of_values = [
    ex.FunctionalLayer,
    bot.Building,
    bpo.Component,
    bpo.Entity
]

union_class = ex.UnionClass
for class_value in union_of_values:
    g.add((union_class, OWL.unionOf, class_value))


g.add((ex.hasFinalCircularPotential, RDF.type, OWL.ObjectProperty))
g.add((ex.hasFinalCircularPotential, RDFS.domain, union_class))
g.add((ex.hasFinalCircularPotential, RDFS.range, ex.CircularPotential))

g.add((ex.hasCircularRequirement, RDF.type, OWL.ObjectProperty))
g.add((ex.hasCircularRequirement, RDFS.domain, ex.CircularPotential))
g.add((ex.hasCircularRequirement, RDFS.range, ex.CircularRequirement))


g.add((ex.hasCircularPotential, RDF.type, OWL.ObjectProperty))
g.add((ex.hasCircularPotential, RDFS.domain, union_class))
g.add((ex.hasCircularPotential, RDFS.range, ex.CircularPotential))


g.add((ex.hasConnectionType, RDF.type, OWL.ObjectProperty))
g.add((ex.hasConnectionType, RDF.type, OWL.FunctionalProperty))
g.add((ex.hasConnectionType, RDFS.domain, bpo.ComponentConnection))
g.add((ex.hasConnectionType, RDFS.range, ex.ConnectionType))


g.add((ex.hasFunctionalLayer, RDF.type, OWL.ObjectProperty))
g.add((ex.hasFunctionalLayer, RDFS.domain, bot.Building))
g.add((ex.hasFunctionalLayer, RDFS.range, ex.FunctionalLayer))


g.add((ex.hasRecommendedInspection, RDF.type, OWL.ObjectProperty))
g.add((ex.hasRecommendedInspection, RDFS.domain, bpo.Component))


g.add((ex.hasRecommendedInspectionMethod, RDF.type, OWL.ObjectProperty))
g.add((ex.hasRecommendedInspectionMethod,
      RDFS.subPropertyOf, ex.hasRecommendedInspection))
g.add((ex.hasRecommendedInspectionMethod, RDFS.domain, bpo.Component))
g.add((ex.hasRecommendedInspectionMethod, RDFS.range, ex.InspectionMethod))


g.add((ex.hasRecommendedInspectionMode, RDF.type, OWL.ObjectProperty))
g.add((ex.hasRecommendedInspectionMode,
      RDFS.subPropertyOf, ex.hasRecommendedInspection))
g.add((ex.hasRecommendedInspectionMode, RDFS.domain, bpo.Component))
g.add((ex.hasRecommendedInspectionMode, RDFS.range, ex.InspectionMode))


g.add((ex.hasRequiredInspection, RDF.type, OWL.ObjectProperty))
g.add((ex.hasRequiredInspection, RDFS.domain, bpo.Component))


g.add((ex.hasRequiredInspectionMethod, RDF.type, OWL.ObjectProperty))
g.add((ex.hasRequiredInspectionMethod, RDFS.subPropertyOf, ex.hasRequiredInspection))
g.add((ex.hasRequiredInspectionMethod, RDFS.domain, bpo.Component))
g.add((ex.hasRequiredInspectionMethod, RDFS.range, ex.InspectionMethod))


g.add((ex.hasRequiredInspectionMode, RDF.type, OWL.ObjectProperty))
g.add((ex.hasRequiredInspectionMode, RDFS.subPropertyOf, ex.hasRequiredInspection))
g.add((ex.hasRequiredInspectionMode, RDFS.domain, bpo.Component))
g.add((ex.hasRequiredInspectionMode, RDFS.range, ex.InspectionMode))


g.add((ex.hasSourceType, RDF.type, OWL.ObjectProperty))
g.add((ex.hasSourceType, RDFS.domain, ex.CircularPotential))
g.add((ex.hasSourceType, RDFS.range, ex.MaterialSourceType))


# ___________________________________________________________ CLASSES

g.add((ex.assembly, RDF.type, RDFS.Class))
g.add((ex.assembly, RDFS.subClassOf, ex.Building))

g.add((ex.Building, RDF.type, RDFS.Class))


g.add((ex.element, RDF.type, RDFS.Class))
g.add((ex.element, RDFS.subClassOf, ex.Component))


# g.add((ex.InstallationType, RDF.type, RDFS.Class))


# Actor
g.add((ex.actor, RDF.type, RDFS.Class))

g.add((ex.PreDeconstructionAuditor, RDF.type, RDFS.Class))
g.add((ex.PreDeconstructionAuditor, RDFS.subClassOf, ex.actor))

g.add((ex.Manufacturer, RDF.type, RDFS.Class))
g.add((ex.Manufacturer, RDFS.subClassOf, ex.actor))

g.add((ex.MaterialBankAgent, RDF.type, RDFS.Class))
g.add((ex.MaterialBankAgent, RDFS.subClassOf, ex.actor))

g.add((ex.WasteAuditor, RDF.type, RDFS.Class))
g.add((ex.WasteAuditor, RDFS.subClassOf, ex.actor))

g.add((ex.Designer, RDF.type, RDFS.Class))
g.add((ex.Designer, RDFS.subClassOf, ex.actor))


# Material Source Type
g.add((ex.MaterialSourceType, RDF.type, RDFS.Class))

g.add((ex.PrimaryRawMaterial, RDF.type, RDFS.Class))
g.add((ex.PrimaryRawMaterial, RDFS.subClassOf, ex.MaterialSourceType))

g.add((ex.SecondaryRawMaterial, RDF.type, RDFS.Class))
g.add((ex.SecondaryRawMaterial, RDFS.subClassOf, ex.MaterialSourceType))

g.add((ex.RecyclableMaterial, RDF.type, RDFS.Class))
g.add((ex.RecyclableMaterial, RDFS.subClassOf, ex.MaterialSourceType))

g.add((ex.NonRenewableMaterial, RDF.type, RDFS.Class))
g.add((ex.NonRenewableMaterial, RDFS.subClassOf, ex.MaterialSourceType))

g.add((ex.RenewableMaterial, RDF.type, RDFS.Class))
g.add((ex.RenewableMaterial, RDFS.subClassOf, ex.MaterialSourceType))

g.add((ex.NonHazardousMaterial, RDF.type, RDFS.Class))
g.add((ex.NonHazardousMaterial, RDFS.subClassOf, ex.MaterialSourceType))

g.add((ex.HazardousMaterial, RDF.type, RDFS.Class))
g.add((ex.HazardousMaterial, RDFS.subClassOf, ex.MaterialSourceType))


# Circular Potential

g.add((ex.CircularPotential, RDF.type, RDFS.Class))
g.add((ex.CircularRequirement, RDF.type, RDFS.Class))

g.add((ex.ReusePotential, RDF.type, RDFS.Class))
g.add((ex.ReusePotential, RDFS.subClassOf, ex.CircularPotential))

g.add((ex.RemanufacturingPotential, RDF.type, RDFS.Class))
g.add((ex.RemanufacturingPotential, RDFS.subClassOf, ex.CircularPotential))

g.add((ex.RecyclingPotential, RDF.type, RDFS.Class))
g.add((ex.RecyclingPotential, RDFS.subClassOf, ex.CircularPotential))

g.add((ex.RepurposingPotential, RDF.type, RDFS.Class))
g.add((ex.RepurposingPotential, RDFS.subClassOf, ex.CircularPotential))

g.add((ex.DiscardPotential, RDF.type, RDFS.Class))
g.add((ex.DiscardPotential, RDFS.subClassOf, ex.CircularPotential))


# Circular Requirment

g.add((ex.Personnel, RDF.type, RDFS.Class))
g.add((ex.Personnel, RDFS.subClassOf, ex.CircularRequirement))

g.add((ex.TrainnedPersonnel, RDF.type, RDFS.Class))
g.add((ex.TrainnedPersonnel, RDFS.subClassOf, ex.Personnel))

g.add((ex.UntrainnedPersonnel, RDF.type, RDFS.Class))
g.add((ex.UntrainnedPersonnel, RDFS.subClassOf, ex.Personnel))

g.add((ex.SiteDependency, RDF.type, RDFS.Class))
g.add((ex.SiteDependency, RDFS.subClassOf, ex.CircularRequirement))

g.add((ex.OnSite, RDF.type, RDFS.Class))
g.add((ex.OnSite, RDFS.subClassOf, ex.SiteDependency))

g.add((ex.OffSite, RDF.type, RDFS.Class))
g.add((ex.OffSite, RDFS.subClassOf, ex.SiteDependency))


g.add((ex.Certification, RDF.type, RDFS.Class))
g.add((ex.Certification, RDFS.subClassOf, ex.CircularRequirement))

g.add((ex.Inspection, RDF.type, RDFS.Class))

g.add((ex.InspectionMode, RDF.type, RDFS.Class))
g.add((ex.InspectionMode, RDFS.subClassOf, ex.Inspection))

g.add((ex.InspectionType, RDF.type, RDFS.Class))
g.add((ex.InspectionType, RDFS.subClassOf, ex.Inspection))

g.add((ex.Intervention, RDF.type, RDFS.Class))
g.add((ex.Intervention, RDFS.subClassOf, ex.CircularRequirement))

g.add((ex.Logistics, RDF.type, RDFS.Class))
g.add((ex.Logistics, RDFS.subClassOf, ex.CircularRequirement))

g.add((ex.Exposure, RDF.type, RDFS.Class))
g.add((ex.Exposure, RDFS.subClassOf, ex.CircularRequirement))

g.add((ex.Legal, RDF.type, RDFS.Class))
g.add((ex.Legal, RDFS.subClassOf, ex.CircularRequirement))

g.add((ex.CircularRequirement, RDF.type, RDFS.Class))

# Connection Type

g.add((ex.ConnectionType, RDF.type, RDFS.Class))

g.add((ex.ChemicalConnection, RDF.type, RDFS.Class))
g.add((ex.ChemicalConnection, RDFS.subClassOf, ex.ConnectionType))

g.add((ex.GravitationalConnection, RDF.type, RDFS.Class))
g.add((ex.GravitationalConnection, RDFS.subClassOf, ex.ConnectionType))

g.add((ex.MechanicalConnection, RDF.type, RDFS.Class))
g.add((ex.MechanicalConnection, RDFS.subClassOf, ex.ConnectionType))

g.add((ex.IndirectConnection, RDF.type, RDFS.Class))
g.add((ex.IndirectConnection, RDFS.subClassOf, ex.ConnectionType))

g.add((ex.DirectConnection, RDF.type, RDFS.Class))
g.add((ex.DirectConnection, RDFS.subClassOf, ex.ConnectionType))

g.add((ex.Irreversible_connection, RDF.type, RDFS.Class))
g.add((ex.Irreversible_connection, RDFS.subClassOf, ex.ConnectionType))

g.add((ex.ReversibleConnection, RDF.type, RDFS.Class))
g.add((ex.ReversibleConnection, RDFS.subClassOf, ex.ConnectionType))


# Functional Layer

g.add((ex.FunctionalLayer, RDF.type, RDFS.Class))

g.add((ex.SpacePlan, RDF.type, RDFS.Class))
g.add((ex.SpacePlan, RDFS.subClassOf, ex.FunctionalLayer))

g.add((ex.Structure, RDF.type, RDFS.Class))
g.add((ex.Structure, RDFS.subClassOf, ex.FunctionalLayer))

g.add((ex.Facade, RDF.type, RDFS.Class))
g.add((ex.Facade, RDFS.subClassOf, ex.FunctionalLayer))


# BPO
g.add((ex.Product, RDF.type, RDFS.Class))
g.add((ex.Product, RDFS.subClassOf, ex.Component))

# _________________________________________DATA PROPERTY
# Defining union of classes for FunctionalLayer AND Component AND Building

union_of_values_3 = [
    ex.FunctionalLayer,
    bot.Building,
    bpo.Component,
    bpo.Entity
]

union_class_3 = ex.UnionClass_3
for class_value_3 in union_of_values_3:
    g.add((union_class_3, OWL.unionOf, class_value_3))


# Data property: hasCircularPotentialIndicator
g.add((ex.hasCircularPotentialIndicator, RDF.type, OWL.DatatypeProperty))
g.add((ex.hasCircularPotentialIndicator, RDF.type, OWL.FunctionalProperty))
g.add((ex.hasCircularPotentialIndicator, RDFS.domain, union_class_3))
g.add((ex.hasCircularPotentialIndicator, RDFS.range, XSD.string))

# Data property: hasConstructionDate
g.add((ex.hasConstructionDate, RDF.type, OWL.DatatypeProperty))
g.add((ex.hasConstructionDate, RDFS.domain, bot.Building))
g.add((ex.hasConstructionDate, RDFS.range, XSD.dateTime))


# Data property: hasDecommissioningDate
g.add((ex.hasDecommissioningDate, RDF.type, OWL.DatatypeProperty))
g.add((ex.hasDecommissioningDate, RDFS.domain, bot.Building))
g.add((ex.hasDecommissioningDate, RDFS.range, XSD.dateTime))


# Data property: hasDesignLife
g.add((ex.hasDesignLife, RDF.type, OWL.DatatypeProperty))
g.add((ex.hasDesignLife, RDFS.domain, union_class_3))
g.add((ex.hasDesignLife, RDFS.range, XSD.nonNegativeInteger))


# Data property: hasEconomicLife
g.add((ex.hasEconomicLife, RDF.type, OWL.DatatypeProperty))
g.add((ex.hasEconomicLife, RDFS.domain, union_class_3))
g.add((ex.hasEconomicLife, RDFS.range, XSD.nonNegativeInteger))

# Data property: hasServiceLife
g.add((ex.hasServiceLife, RDF.type, OWL.DatatypeProperty))
g.add((ex.hasServiceLife, RDFS.domain, union_class_3))
g.add((ex.hasServiceLife, RDFS.range, XSD.nonNegativeInteger))


# Data property: hasWasteCode
g.add((ex.hasWasteCode, RDF.type, OWL.DatatypeProperty))
g.add((ex.hasWasteCode, RDF.type, OWL.FunctionalProperty))
g.add((ex.hasWasteCode, RDFS.domain, dicm.Material))
g.add((ex.hasWasteCode, RDFS.range, XSD.string))

# Data property: hasCurrentUseCount
g.add((ex.hasCurrentUseCount, RDF.type, OWL.DatatypeProperty))
g.add((ex.hasCurrentUseCount, RDF.type, OWL.FunctionalProperty))
g.add((ex.hasCurrentUseCount, RDFS.domain, union_class_3))
g.add((ex.hasCurrentUseCount, RDFS.range, XSD.nonNegativeInteger))


# Data property: hasRemainingReuseCount
g.add((ex.hasRemainingReuseCount, RDF.type, OWL.DatatypeProperty))
g.add((ex.hasRemainingReuseCount, RDF.type, OWL.FunctionalProperty))
g.add((ex.hasRemainingReuseCount, RDFS.domain, union_class_3))
g.add((ex.hasRemainingReuseCount, RDFS.range, XSD.nonNegativeInteger))


# Data property: hasTotalReuseCount
g.add((ex.hasTotalReuseCount, RDF.type, OWL.DatatypeProperty))
g.add((ex.hasTotalReuseCount, RDF.type, OWL.FunctionalProperty))
g.add((ex.hasTotalReuseCount, RDFS.domain, union_class_3))
g.add((ex.hasTotalReuseCount, RDFS.range, XSD.nonNegativeInteger))


########################################################### Extending BOT ##
# Create a Site
g.add((URIRef("Site_1"), RDF.type, bot.Site))
g.add((URIRef("Site_1"), bot.conatinsZone, URIRef("Building_1")))


# Create a Building
g.add((URIRef("Building_1"), RDF.type, bot.Building))


# Create Stories
g.add((URIRef("Building_1"), bot.hasStorey, URIRef("Storey_1")))
g.add((URIRef("Building_1"), bot.hasStorey, URIRef("Storey_2")))
g.add(((URIRef("Storey_1"), RDF.type, bot.Storey)))
g.add(((URIRef("Storey_2"), RDF.type, bot.Storey)))


# Create Spaces
g.add((URIRef("Storey_1"), bot.hasSpace, URIRef("Space_a")))
g.add((URIRef("Storey_1"), bot.hasSpace, URIRef("Space_b")))

g.add((URIRef("Storey_2"), bot.hasSpace, URIRef("Space_c")))
g.add((URIRef("Storey_2"), bot.hasSpace, URIRef("Space_d")))


g.add((URIRef("Space_a"), RDF.type, bot.Space))
g.add((URIRef("Space_b"), RDF.type, bot.Space))
g.add((URIRef("Space_c"), RDF.type, bot.Space))
g.add((URIRef("Space_d"), RDF.type, bot.Space))


########################################################### SAVE ##


# Serialize the graph to Turtle format and save
output_file = "Main_casestudy_V8.ttl"
g.serialize(destination=output_file, format="turtle")

print("Graph saved as", output_file)


