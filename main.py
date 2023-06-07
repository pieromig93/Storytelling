import csv
import random
import create_pearls as cp
import requests
import itertools

pearls_file = open("/home/h93/Piero/Uni/Storytelling/pearls.txt", "r")
file_csv = csv.reader(pearls_file, delimiter=",")

visited_pearl = []
visited_canvas = []

def get_canvas_from_pearl(pearl):

    pearls_file = open("/home/h93/Piero/Uni/Storytelling/pearls.txt", "r")
    file_csv = csv.reader(pearls_file, delimiter=",")
    canvas_from_pearl = []
    for row in file_csv:
        if str(row[0]) == str(pearl):
            canvas_from_pearl.append(row[1])
    
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
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Estrai il tempo di percorrenza dalla risposta
    travel_time = data["route"]["time"]
    
    return travel_time


if __name__ == '__main__':

    # Supponiamo che l'utente abbia preferenze (Beni, Tecniche_edilizie)
    # perle le ho, devo creare un percorso che sia minore di una certa durata
    pearls = get_pearls()
    # starting_pearl = random.choice(pearls)
    
    # print("You started from POI: "+ str(starting_pearl))
    # visited_pearl.append(starting_pearl)

    # print("From this pearl you get this canvas: ")
    # print(get_canvas_from_pearl(starting_pearl))
    # print("But based on your preferences I suggest you...")
    # print(filter_canvas(get_canvas_from_pearl(starting_pearl)))
    cp.get_coordinates(pearls[0])