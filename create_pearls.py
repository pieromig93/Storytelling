from owlready2 import *
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from IPython.display import HTML
import rdflib

onto_path.append("/home/h93/Piero/Uni/Storytelling/")
onto = get_ontology("ext_mara.owl").load()

# test ontology
# metto in una lista tutte le classi e gli individui dell'ontologia
class_list = list(onto.classes())
individuals_list = list(onto.individuals())

starting_canvas = 'ext_Mara.https://cosme.unicampania.it/rasta/norba/8-VIABILITA-Strade-antiche/index.json/canvas/4'
canvas = [starting_canvas]

def remove_prefix(s):
    return str(s).split(".",1)[1]

def clean_list(list):
    return_list = []
    for element in list:
        return_list.append(element[0])

    return return_list

def get_all_canvas():
    canvas = list(default_world.
                                       sparql("""SELECT ?canvas WHERE{ 
                                                ?canvas
                                                rdf:type 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#Canvas>
                                                } """))
    canvas = clean_list(canvas)
    return canvas    

def hasAnnotation(canvas):
    canvas = remove_prefix(canvas)
    annotation_contained_into_canvas = list(default_world.
                                       sparql("""SELECT ?annotation WHERE{ 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#""" +canvas+"""> 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#hasAnnotation>
                                                ?annotation } """))
    annotation_contained_into_canvas = clean_list(annotation_contained_into_canvas)
    return annotation_contained_into_canvas
    
def hasDetail(annotation):
    annotation = remove_prefix(annotation)
    detail_of_annotation = list(default_world.
                                    sparql("""SELECT ?detail WHERE{ 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#""" +annotation+"""> 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#hasDetail>
                                                ?detail } """))
    detail_of_annotation = clean_list(detail_of_annotation)
    return detail_of_annotation[0]

def isContainedIntoAnnotation(detail):
    detail = remove_prefix(detail)
    annotation_of_detail = list(default_world.
                                    sparql("""SELECT ?an WHERE{ 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#""" +detail+"""> 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#isContainedIntoAnnotation>
                                                ?an } """))
    annotation_of_detail = clean_list(annotation_of_detail)
    return annotation_of_detail

def isInCanavs(annotation):
    annotation = remove_prefix(annotation)
    canvas_of_annotation = list(default_world.
                                    sparql("""SELECT ?can WHERE{ 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#""" +annotation+"""> 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#isInCanvas>
                                                ?can } """))
    canvas_of_annotation = clean_list(canvas_of_annotation)
    return canvas_of_annotation

def get_super_class(detail):
    detail = remove_prefix(detail)
    super_class = list(default_world.
                                    sparql("""SELECT ?class WHERE{ 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#""" +detail+"""> 
                                                rdf:type
                                                ?class
                                                filter(?class != owl:Class)
                                                filter(?class != owl:NamedIndividual)
                                                } """))
    super_class = clean_list(super_class)
    return super_class[0]

def create_graph_from_canvas(canvas, G):
    for c in canvas:
        annotations = hasAnnotation(c)
        for an in annotations:    
            detail = hasDetail(an)
            for d in detail:
                annotations_of_detail = isContainedIntoAnnotation(d)
                for an in annotations_of_detail:
                    canvas_of_annotation = isInCanavs(an)
                    for i in canvas_of_annotation:
                        G.add_node(str(i)[50:])
                        G.add_edge(str(c),str(i)[50:])
    
    net=Network(filter_menu=True, layout='dot', directed=True, select_menu=True)
    net.from_nx(G)
    net.save_graph("./canvas_graph.html")
    HTML(filename="./canvas_graph.html")

def clustering(canvas_list):
    clustering_dict = {}
    clustering_list = []
    for canvas in canvas_list:    
        clustering_list.append(canvas)
        annotations_list = hasAnnotation(canvas)
        for annotation in annotations_list:
            detail = hasDetail(annotation)
            mother_class = str(get_super_class(detail))
            if clustering_dict.get(mother_class) == None:
                # non presente nel dizionario
                clustering_dict[mother_class] = 1
            else:
                # incremento quella già presente
                clustering_dict[mother_class] = clustering_dict[mother_class]+1
            
        clustering_list.append(clustering_dict)
        clustering_dict = {}
    return clustering_list

def get_mara_distances():
    
    nif = rdflib.Namespace('http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#')
    g = rdflib.Graph()
    g.parse ('/home/h93/Piero/Uni/Storytelling/ext_mara.owl', format='application/rdf+xml')
    
    # creo un grafo networkx
    onto_graph = nx.MultiDiGraph()
    
    # itero tra le triple
    for s, p, o in g:
        onto_graph.add_edge(str(s), str(o), key=str(p))

    fout = open("/home/h93/Piero/Uni/Storytelling/mara_distances.csv", "w")

    for c in get_all_canvas():
        for e in get_all_canvas():
            if c != e:
                try:
                    p = nx.shortest_path(onto_graph, nif+remove_prefix(c), nif+remove_prefix(e))    
                    print(str(p[0])[106:]+", "+str(p[len(p)-1])[106:]+", "+str(len(p)), file= fout)
                    print(str(p), file= fout)
                except:
                    continue

if __name__ == "__main__":
    print("Starting...")
    fout = open("/home/h93/Piero/Uni/Storytelling/clu_info.txt", "w")
    print(clustering(get_all_canvas()), file=fout)