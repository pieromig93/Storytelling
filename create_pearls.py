from owlready2 import *
import json

def remove_prefix(s):
    return s[9:]
onto_path.append("/home/h93/Piero/Uni/Storytelling/")
onto = get_ontology("ext_mara.owl").load()

# test ontology
ontology_class = list(default_world.sparql("""SELECT ?x WHERE{?x rdf:type owl:Class. } """))

# creo le perle con una prima query sparql mettendoci dentro tutte le domus annotate
canvas = list(default_world.sparql("""SELECT ?x WHERE{?x rdf:type <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#Canvas> } """))

for i in range(len(canvas)):
    query_subject = remove_prefix(str(canvas[i][0]))
    annotation_contained_into_canvas = list(default_world.
                                       sparql("""SELECT ?annotation WHERE{ 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#""" +query_subject+"""> 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#hasAnnotation>
                                                ?annotation } """))
    clean_list = []
    for an in annotation_contained_into_canvas:
        clean_list.append(an[0])
    canvas[i].append(clean_list)

# in c[0] abbiamo tutti i canvas mentre in c[1] abbiamo la lista delle annotazioni
annotation_detail_dict = {}
for c in canvas:
    for i in range(len(c[1])):
        query_subject = remove_prefix(str(c[1][i]))
        detail_of_annotation = list(default_world.
                                    sparql("""SELECT ?detail WHERE{ 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#""" +query_subject+"""> 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#hasDetail>
                                                ?detail } """))
        
        annotation_detail_dict[query_subject] = remove_prefix(str(detail_of_annotation[0][0]))

print(annotation_detail_dict)