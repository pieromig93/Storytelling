"""
    Una volta costruita l'ontologia si necessita della costruzione del grafo utilizzando le stringhe 
    di perle. Questo avviene molto semplicemente: se prendiamo per esempio le domus di Pompei (o Norba) la perla potrebbe essere proprio la domus ed i 
    contenuti appartenenti alla stessa domus vengono inseriti all'interno della perla. Ci basiamo su un'ontologia, e quindi, una struttura in rdf che
    necessita di essere parserizzata.
"""

def clean_string(s):
    return s[7:]


from owlready2 import *

# importo ontologia 
onto_path.append("/home/h93/Piero/Uni/Storytelling/file/ontology")
onto = get_ontology("http://www.semanticweb.org/h93/ontologies/2023/3/pompei")
onto.load()

# test query sparql
ontology_class = default_world.sparql("""SELECT ?x WHERE{?x rdf:type owl:Class. } """)
ontology_individual = default_world.sparql("""SELECT ?x WHERE{?x rdf:type owl:NamedIndividual. } """)

# creo le perle con una prima query sparql mettendoci dentro tutte le domus annotate
pearls = list(default_world.sparql("""SELECT ?x WHERE{?x rdf:type <http://www.semanticweb.org/h93/ontologies/2023/3/pompei#Domus> } """))

for i in range(len(pearls)):
    
    # aggiungo alle perle i contenuti specifici per ognuna
    canvas_contained_into_pearl = []
    linked_to_pearl = []
    query_subject = clean_string(str(pearls[i][0]))

    # devo costruire la stringa per la query sparql cosicché possa aggiungere al vettore delle perle i contenuti relativi alla domus
    canvas_contained_into_pearl = list(default_world.
                                       sparql("""SELECT ?canvas WHERE{ 
                                                <http://www.semanticweb.org/h93/ontologies/2023/3/pompei#""" +query_subject+"""> 
                                                <http://www.semanticweb.org/h93/ontologies/2023/3/pompei#contain>
                                                ?canvas } """))
    
    linked_to_pearl = list(default_world.
                                       sparql("""SELECT ?domus WHERE{ 
                                                <http://www.semanticweb.org/h93/ontologies/2023/3/pompei#""" +query_subject+"""> 
                                                <http://www.semanticweb.org/h93/ontologies/2023/3/pompei#isAdiacentTo>
                                                ?domus } """))
    pearls[i].append(canvas_contained_into_pearl)
    pearls[i].append(linked_to_pearl)

for pearl in pearls:
    print(pearl)

# dalle perle appena create dobbiamo creare il grafo.
