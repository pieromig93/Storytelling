import json, os, Levenshtein
from owlready2 import *

def normalize_list(l):
    norm_list = []
    for element in l:
        norm_list.append(str(element).lower().replace("_","").split(".")[1])
    return norm_list

# directory dove ci sono tutti i manifest .json
files = os.listdir("/home/h93/Piero/Uni/Storytelling/file/files prof/manifests")

# directory dell'ontologia
onto_path.append("/home/h93/Piero/Uni/Storytelling/file/files prof/mara ontology")
onto = get_ontology("mara.owl").load()

# metto in una lista tutte le classi e gli individui dell'ontologia
class_list = list(onto.classes())
individuals_list = list(onto.individuals())

# normalizzo tutta la lista degli individui e delle classi per ottimizzare la ricerca degli elementi
normalized_list_individuals = normalize_list(individuals_list)
normalized_class_list = normalize_list(class_list)


# cerco l'individuo più vicino all'annotazione letta
def get_nearest_individual(s1):
    
    s = s1.lower().replace("_","")[5:]
    max_sim = 0
    max_individuo = None
    for ind in normalized_list_individuals:
        sim = 1 - (Levenshtein.distance(ind, s)/ max(len(s), len(ind)))
        if sim > max_sim:
            max_sim = sim
            max_individuo = ind

    if max_sim >0.72:
        index = normalized_list_individuals.index(max_individuo)
        ind_name = str(individuals_list[index])[5:]
        ind = onto.search_one(iri= f"*{ind_name}")
        # print("STRING: "+s+" IND: "+ind.name)

    else: 
        # print(s)
        # vuol dire che non ho trovato corrispondenza con un individuo già presente nell'ontologia
        # bisogna creare un nuovo individuo
        # verificare che il nome sia diverso da quello di una classe
        if s in normalized_class_list:
            print(s)
        # creare l'individuo come figlio della classe più alta nella gerarchia delle classi
        # append(s) in normalized_list
        # sort di normalized list
        ind = None

    return ind


# per ogni file della directory devo leggerlo e popolare l'ontologia
for file in files:
    
    annotation_file = open("/home/h93/Piero/Uni/Storytelling/file/files prof/manifests/"+str(file), "r")
    data = json.load(annotation_file)
    
    # print(data['id'])
    norba = onto.search_one(iri = "*Norba")
    manifest = onto.Manifest(str(data['id']))
    manifest.isPartOf.append(norba)

    #prendo tutti i canvas del manifest    
    for input in data['items']:

        # print(input['id'])
        canvas = onto.Canvas(str(input['id']))
        canvas.hasManifest.append(manifest)
        canvas.isPartOf.append(norba)

        try:    
            for annotation in input['annotations']['items']:
                # print(str(annotation['id'])+" ----> "+str(annotation['body']['value']))
                an = onto.Annotation(str(annotation['id']))
                detail = get_nearest_individual(str(annotation['body']['value']))
                # print(detail)

                # if detail == None:

                #     # creo l'oggetto relativo
                #     if "Cas" in d or "Domu" in d:
                #         onto.Domus(d)
                #     elif "Strad" in d or "Vie" in d:
                #         onto.Vie(d)
                #     elif "Marcia" in d or "Coccio" in d:
                #         onto.Pavimenti(d)
                #     else:
                #         onto.Beni(d)
                #     detail = onto.search_one(iri = f"*{d}")

                # # assegno le object property
                # canvas.hasAnnotation.append(an)
                # an.isPartOf.append(norba)
                # an.isInCanvas.append(canvas)
                # an.hasDetail.append(detail)
                # detail.isPartOf.append(norba)
                # detail.isContainedIntoAnnotation.append(an)
                    
        except:
            continue

# onto.save(file = "ext_mara.owl", format = "rdfxml")