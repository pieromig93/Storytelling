import csv
import random
import create_cluster as cp
import test as t
import requests
import itertools


def get_canvas_from_pearl(pearl):

    pearls_file = open("/home/h93/Piero/Uni/Storytelling/pearls.txt", "r")
    file_csv = csv.reader(pearls_file, delimiter=",")
    canvas_from_pearl = []
    for row in file_csv:
        # print(str(row[0])+"----"+str(pearl))
        if str(row[0]) == str(pearl):
            canvas_from_pearl.append(row[1])
    pearls_file.seek(0,0) 
    pearls_file.close()
    return canvas_from_pearl

def get_pearls():
    
    pearls_file = open("/home/h93/Piero/Uni/Storytelling/pearls.txt", "r")
    file_csv = csv.reader(pearls_file, delimiter=",")
    pearls = []
    tmp = ''    
    for row in file_csv:
        if row[0] != tmp:
            pearls.append(row[0])
            tmp = row[0]
    
    pearls_file.close()
    return pearls

def filter_canvas(canvas_list):
    
    cluster_file = open("/home/h93/Piero/Uni/Storytelling/kmeans4C.txt", "r")
    file_csv = csv.reader(cluster_file, delimiter=',')
    suggested_canvas = []
    for canvas in canvas_list:
        # 1) controllo presenza nel cluster omogenei rispetto alle preferenze utente (cluster 2)
        for row in file_csv:
            if str(cp.remove_prefix(row[0])) == str(canvas) and str(row[1])==str(2):
                suggested_canvas.append(canvas)
        
        cluster_file.seek(0,0)

    return suggested_canvas

def get_travel_time(start_location, end_location):
    url = "http://www.mapquestapi.com/directions/v2/route"
    
    params = {
        "key": "10FvhA7t7wxFsUM7GGn5DIMFQPcyXQFx",
        "from": start_location,
        "to": end_location,
        "routeType":"pedestrian"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Estrai il tempo di percorrenza dalla risposta
    travel_time = data["route"]["time"]
    
    return travel_time

def get_total_time(route):
    coord = []
    total_time = 0
    for r in route:
        coord.append(t.get_coordinates(r))
    
    for i in range(len(coord)-1):
            start_location = str(coord[i][0][0])+","+str(coord[i][0][1])
            end_location = str(coord[i+1][0][0])+","+str(coord[i+1][0][1])
            tmp = get_travel_time(start_location, end_location)
            total_time += tmp

    return  total_time

def create_time_route(route_list):
    file = open("/home/h93/Piero/Uni/Storytelling/possibile_route.txt", "w")
    for r in route_list:
        print(str(r).replace(" ", "_").replace('"', '').replace("(","").replace(")","")+","+str(get_total_time(r)), file=file)
        # print(str(r).replace("(", "").replace(")","").replace(" ", "").replace("'", "").replace('"', ""), file=file)
    file.close()

def pearls_time_filter(user_max_time):
    file = open("/home/h93/Piero/Uni/Storytelling/possibile_route.txt", "r")
    file_csv = csv.reader(file, delimiter=',')
    possible_route = []
    for row in file_csv:
        if int(row[3])< int(user_max_time):
            route_tuple = (row[0], row[1], row[2])
            possible_route.append(route_tuple)

    return possible_route

def print_route_pos(actual_pearl, route):
    print("\nRoute: ")
    for i,r in enumerate(route):
        if i == actual_pearl:
            print(str(i)+")"+str(r)+" <---")
        else:
            print(str(i)+")"+str(r))

    print("")


# ! MAIN
if __name__ == '__main__':
    print("Starting...\n")
    # Supponiamo che l'utente abbia preferenze (Beni, Tecniche_edilizie)
    # perle le ho, devo creare un percorso che sia minore di una certa durata
    pearls = get_pearls()
    # eseguo tutte le possibili permutazioni delle perle di dimensione 3 e le salvo nel file indicato
    result = list(itertools.permutations(pearls, 3))
    create_time_route(result)



    



    