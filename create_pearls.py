from owlready2 import *

def clean_string(s):
    return s[9:]
onto_path.append("/home/h93/Piero/Uni/Storytelling/")
onto = get_ontology("ext_mara.owl").load()

# test ontology
ontology_class = list(default_world.sparql("""SELECT ?x WHERE{?x rdf:type owl:Class. } """))

# creo le perle con una prima query sparql mettendoci dentro tutte le domus annotate
canvas = list(default_world.sparql("""SELECT ?x WHERE{?x rdf:type <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#Canvas> } """))

for i in range(len(canvas)):
    query_subject = clean_string(str(canvas[i][0]))
    annotation_contained_into_canvas = list(default_world.
                                       sparql("""SELECT ?annotation WHERE{ 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#""" +query_subject+"""> 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#hasAnnotation>
                                                ?annotation } """))
    canvas[i].append(annotation_contained_into_canvas)
    
for c in canvas:
    print(c)