from owlready2 import *
import create_pearls as cp

onto_path.append("/home/h93/Piero/Uni/Storytelling/")
onto = get_ontology("extended_mara_with_poi.owl").load()

def getPOIwithDetail():
    poi = list(default_world.
                                       sparql("""SELECT DISTINCT ?poi  WHERE{ 
                                                ?poi
                                                rdf:type 
                                                <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#POI>
                                                ?poi <http://www.semanticweb.org/ontologies/2011/0/ProgettoAteneo2.owl#hasDetail> ?X
                                                } """))
    poi = cp.clean_list(poi)
    return poi 

def getCanvasFromPOI(poi_list):
    pearls_file = open("/home/h93/Piero/Uni/Storytelling/pearls.txt", "w")
    for poi in poi_list:
        detail_list = cp.hasDetailList(poi)
        for detail in detail_list:
            annotation_list = cp.isContainedIntoAnnotation(detail)
            for an in annotation_list:
                canvas = cp.isInCanavs(an)
                print(str(poi)+","+str(cp.remove_prefix(canvas[0])), file=pearls_file)

if __name__ == '__main__':
    print("creating Perls...")
    poi_list = getPOIwithDetail()
    getCanvasFromPOI(poi_list)

        
