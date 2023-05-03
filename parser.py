from owlready2 import *

STRING_SEPARATOR = '|'
NULL_INFO = ' ""                               '

onto_path.append("/home/h93/Piero/Uni/Storytelling/file/files prof/mara ontology")
onto = get_ontology("mara.owl").load()
class_list = list(onto.classes())

annotation_file = open("/home/h93/Piero/Uni/Storytelling/file/files prof/mara ontology/output.annotations", "r") 

# non considero l'intestazione del file
annotation_file.seek(516)

last_canvas_added = ''

for line in annotation_file:
    
    if line[0] == STRING_SEPARATOR:
        
        entry = line.split('|')[1:4]
        if entry[1] == NULL_INFO:
            
            # creo le istanze
            an = onto.Annotation()
            an.name = entry[0].strip(" <>")
            if last_canvas_added != entry[2].strip(" <>"):
                can = onto.Canvas()
                can.name = entry[2].strip(" <>")
                last_canvas_added = can.name
        
        else:
            
            # recupero individui
            annotation = onto.search_one(iri = f"*{entry[0].strip(' <>')}")
            d = entry[1].strip('" "')[6:].capitalize()
            canvas = onto.search_one(iri = f"*{entry[2].strip(' <>')}")
            norba = onto.search_one(iri = "*Norba")
            
            if "mara."+d in str(class_list): 
                d = "N_"+d
            
            detail = onto.search_one(iri = f"*{d}")

            if detail == None:

                # creo l'oggetto relativo
                if "Cas" in d or "Domu" in d:
                    onto.Domus(d)
                elif "Strad" in d or "Vie" in d:
                    onto.Vie(d)
                elif "Marcia" in d or "Coccio" in d:
                    onto.Pavimenti(d)
                else:
                    onto.Beni(d)
                detail = onto.search_one(iri = f"*{d}")
                 
            # assegno le object property
            canvas.hasAnnotation.append(annotation)
            canvas.isPartOf.append(norba)
            annotation.detail.append(entry[1].replace(" ",""))
            annotation.hasDetail.append(detail)
            annotation.isPartOf.append(norba)
            annotation.isInCanvas.append(canvas)
            detail.isPartOf.append(norba)
            detail.isContainedIntoAnnotation.append(annotation)

            
onto.save(file = "ext_mara.owl", format = "rdfxml")