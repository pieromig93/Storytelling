import possible_route as pr
import create_cluster as cr
import debug_print as dp
import plot_bokeh as pl
import numpy as np
import random
import time
import csv
import math
import user
import os
    
def compute_satisfaction(user):
    with open("/home/h93/Piero/Uni/Storytelling/points.txt", "r") as file:
        file_csv = csv.reader(file, delimiter=",")

        point = [0,0]
        lastx = 0
        lasty = 0
        for row in file_csv:
            if row[0] in user.visited_canvas:
                point[0]+= float(row[1])
                point[1] += float(row[2])
            if(row[0] == user.visited_canvas[-1]):
                lastx = float(row[1])
                lasty= float(row[1])

        point[0] = point[0]/len(user.visited_canvas)
        point[1] = point[1]/len(user.visited_canvas)


    distance =  math.sqrt(pow(float(point[0])-lastx,2)+pow(float(point[1])-lasty,2))

    if(distance < 0.2):
        satisfaction = 5
    elif(distance > 0.2 and distance < 0.3):
        satisfaction = 4
    elif(distance > 0.3 and distance < 0.4):
        satisfaction = 3
    elif(distance > 0.4 and distance < 0.6):
        satisfaction = 2
    elif(distance > 0.6 and distance < 1):
        satisfaction = 1
    else:
        satisfaction = 0
    
    if len(user.satisfaction) > 0:
        user.satisfaction.append(user.satisfaction[-1]+satisfaction)
    else:
        user.satisfaction.append(satisfaction)
    
    return point

def print_canvas_wp(canvas_list):
    for i,fc in enumerate(canvas_list):
            print(str(i)+")"+str(fc)+", "+str(get_pearl_from_canvas(fc)))

def print_canvas(canvas_list):
    for i, c in enumerate(canvas_list):
        print(str(i)+") "+str(c))

def get_awareness_from_route(route):
    awareness = []
    total_awareness = 0
    
    for i in range(len(route)):
        awareness.append(float(0))
    
    for i, pearl in enumerate(route):
        canvas_list = get_canvas_from_pearl(pearl)
        for canvas in canvas_list:
            point = []
            point = np.array(get_point_from_canvas(canvas))
            awareness[i]+= np.linalg.norm(point)
        
        total_awareness += awareness[i]

    return awareness, total_awareness

def get_canvas_from_pearl(pearl):
    file_pearl = open("/home/h93/Piero/Uni/Storytelling/pearls.txt","r")
    file_pearl_csv = csv.reader(file_pearl, delimiter=',')
    canvas_in_pearl = []
    for row in file_pearl_csv:
        if row[0] == pearl:
            canvas_in_pearl.append(row[1])
    
    file_pearl.close()
    return canvas_in_pearl

def get_pearl_from_canvas(canvas):
    file = open("/home/h93/Piero/Uni/Storytelling/pearls.txt", "r")
    file_csv = csv.reader(file, delimiter=',')

    pearls_that_contain_canvas = []

    for row in file_csv:
        if str(canvas) == str(row[1]):
            pearls_that_contain_canvas.append(row[0])    
    file.close()

    return pearls_that_contain_canvas

def get_number_of_canvas_from_pearl(pearl):
    file_pearl = open("/home/h93/Piero/Uni/Storytelling/pearls.txt","r")
    file_pearl_csv = csv.reader(file_pearl, delimiter=',')
    canvas_counter = 0
    for row in file_pearl_csv:
        if row[0] == pearl:
            canvas_counter += 1
    
    file_pearl.close()
    return canvas_counter

def get_point_from_canvas(actual_canvas):
    file = open("/home/h93/Piero/Uni/Storytelling/points.txt","r")
    file_csv = csv.reader(file, delimiter=',')
    actual_canvas_point = []
    for row in file_csv:
        if str(row[0]) == str(actual_canvas):
            actual_canvas_point.append(row[1])
            actual_canvas_point.append(row[2])
    
    file.seek(0,0)
    return actual_canvas_point

def check_canvas_pearl(canvas, route, actual_pearl, canvas_counter):
    file_pearl = open("/home/h93/Piero/Uni/Storytelling/pearls.txt","r")
    file_pearl_csv = csv.reader(file_pearl, delimiter=',')

    for row in file_pearl_csv:

        if row[0] == route[actual_pearl] and cr.remove_prefix(row[1]) == canvas:
            return canvas_counter/(get_number_of_canvas_from_pearl(route[actual_pearl]))
        else:
            if actual_pearl == 0:
                # se la mia perla è la zero oltre ad analizzare i canvas interni alla mia perla considero anche quelli della perla successiva
                if cr.remove_prefix(row[1]) == canvas and row[0] == route[actual_pearl+1]:
                    return  (get_number_of_canvas_from_pearl(route[actual_pearl]))/canvas_counter  
            elif actual_pearl == len(route)-1:
                # se sto nell'ultima perla analizzo sempre i miei canvas e quelli della perla precedente dando una penality se torno indietro
                if cr.remove_prefix(row[1]) == canvas and row[0] == route[actual_pearl-1]:
                    return  10*(get_number_of_canvas_from_pearl(route[actual_pearl]))/canvas_counter
            else:
                # sono la perla centrale (o una di esse) e quindi analizzo i canvas che sono prima e dopo di me
                if cr.remove_prefix(row[1]) == canvas and row[0] == route[actual_pearl+1]:
                    return (get_number_of_canvas_from_pearl(route[actual_pearl]))/canvas_counter
                elif cr.remove_prefix(row[1]) == canvas and row[0] == route[actual_pearl-1]:
                    return 10*(get_number_of_canvas_from_pearl(route[actual_pearl]))/canvas_counter
        
    file_pearl.close()
    return -1

def get_profile_point(preferences):
    return [preferences[0]/preferences[2], preferences[1]/preferences[2]]

def update_profile_preferences(canvas, user, actual_pearl):

    # aggiungo il canvas alla lista di canvas visitati dell'utente
    user.visited_canvas.append(str(canvas))
    user.canvas_in_pearl_counter[actual_pearl] += 1

    # inizializzo la lista delle preferenze a seconda dei canvas visitati dall'utente
    if len(user.preferences) == 0:
        user_num_x = 0
        user_num_y = 0
        user_den = 0
    else:
        user_num_x = user.preferences[0]
        user_num_y = user.preferences[1]
        user_den = user.preferences[2]

    cluster_axis = ['ext_mara.Beni','ext_mara.Tecniche_Edilizie'] # supponiamo siano le preferenze dell'utente
    user_info = cr.clustering([canvas],cluster_axis)
    user_num_x += user_info[0][1][cluster_axis[0]]
    user_num_y += user_info[0][1][cluster_axis[1]]
    user_den += user_info[1]
    
    compute_satisfaction(user_maria_anna)
    
    return [user_num_x, user_num_y, user_den]

# ! FUNZIONE CHE RESTITUISCE LA LISTA CONTENENTE I CANVAS PIÙ VICINI
def get_next_canvas(actual_canvas, route, actual_pearl, canvas_counter, user, filtered_canvas):
    
    # apro il file dei punti
    file = open("/home/h93/Piero/Uni/Storytelling/points.txt","r")
    file_csv = csv.reader(file, delimiter=',')
    
    # recuper i punti dai quali calcolerò la distanza
    profile_point = get_profile_point(user.preferences)
    actual_canvas_point = get_point_from_canvas(actual_canvas)
    
    # struttura contenente i canvas con le relative distanze
    distances_between_canvas = []
    examinated_canvas = []    
    for row in file_csv:
        
        pi = check_canvas_pearl(cr.remove_prefix(str(row[0])), route, actual_pearl, canvas_counter)

        # se qui nell'if aggiungo anche la condizione se presente o meno nella filtered_list lavoro solo su quelli appartenenti a quel cluster
        if pi > 0 and str(row[0]) not in user.visited_canvas:
        # if pi > 0 and str(row[0]) not in user.visited_canvas and str(row[0]) in filtered_canvas:    
            
            alpha1 = math.sqrt(pow(float(actual_canvas_point[0])-float(row[1]),2)+pow(float(actual_canvas_point[1])-float(row[2]),2))
            alpha2 = math.sqrt(pow(float(profile_point[0])-float(row[1]),2)+pow(float(profile_point[1])-float(row[2]),2))
            
            # print("\nCanvas: "+str(cr.remove_prefix(str(row[0])))
                #   +"\nDistance(alpha1): "+str(alpha1)+" \nDistance(alpha2): "+str(alpha2)
                #   +"\nTotal distance: "+str(pi*(alpha1+alpha2))+"\npi: "+str(pi)+"\n"+"Pearl: "+
                #   str(get_pearl_from_canvas(row[0])[0])+"\n")
            
            distances_between_canvas.append((row[0], pi*(alpha1+alpha2), get_pearl_from_canvas(row[0]), (alpha1+alpha2)))
            examinated_canvas.append(row[0])
    # print("CANVAS ANALYZED: "+str(len(distances_between_canvas))+"\n")
    distances_between_canvas.sort(key=lambda a:a[1])
    
    # print(dp.debug_line)
    # for d in distances_between_canvas:
    #     print(d)
    # print(dp.end_line+"\n")
    
    suggested_canvas = []
    for i in range(2):
        try:
            suggested_canvas.append(distances_between_canvas[i][0])
        except:
            continue
    file.close()

    return suggested_canvas, examinated_canvas

# ? ―――――――――――――――――――――――――――――――――― MAIN ――――――――――――――――――――――――――――――――――

if __name__ == '__main__':     
    print(dp.initial)
    
    # user_max_time = input("Enter time max(sec):")
    # possibile_route = pr.pearls_time_filter(240)
    # route = random.choice(possibile_route)
    # sample_route = ('extended_mara_with_poi.12._Complesso_termale', 
    #                 'extended_mara_with_poi.2._Porta_Maggiore_e_le_mura_di_Norba', 
    #                 'extended_mara_with_poi.14._Tempio_di_Giunone_Lucina')
    
    sample_route = ('extended_mara_with_poi.12._Complesso_termale', 
                    'extended_mara_with_poi.3._Strada_basolata_e_Storia_degli_studi', 
                    'extended_mara_with_poi.14._Tempio_di_Giunone_Lucina')
    
    
    # devo calcolare l'awareness totale del percorso

    user_maria_anna = user.User("MariaAnna", [], sample_route,"cyan")

    
    actual_pearl = 0
    pr.print_route_pos(actual_pearl, sample_route)
    total_canvas = 0
    
    for pearl in sample_route:
        total_canvas += get_number_of_canvas_from_pearl(pearl)
    
    # prendo tutti i canvas cotenuti nella perla
    canvas_list = pr.get_canvas_from_pearl(sample_route[actual_pearl])
    # print("The canvas inside this perl are: ")
    # print_canvas(canvas_list)
    
    # prendo i canvas contenuti nel cluster che parla "di più" di beni e tecniche edilizie;
    filtered_canvas = pr.filter_canvas(canvas_list)
    print("\nBased on clustering, I suggest you this canvas: ")
    print_canvas_wp(filtered_canvas)
    
    initial_choice = 0
    while initial_choice != -1:
        initial_choice = input("\nChoose the first canvas: ")
        try:
            choiced_canvas = filtered_canvas[int(initial_choice)]
            # choiced_canvas = canvas_list[int(initial_choice)]
            initial_choice = -1
        except:
            initial_choice = 0
            print("Wrong input, retry.")
            continue

    print("\nYou are looking the canvas: "+str(choiced_canvas)+"\n")
    user_maria_anna.preferences = update_profile_preferences(choiced_canvas, user_maria_anna, actual_pearl)
    suggested_canvas, examinated_canvas = get_next_canvas(choiced_canvas, sample_route, actual_pearl, user_maria_anna.canvas_in_pearl_counter[actual_pearl], user_maria_anna, 0)
    pl.plot_point(choiced_canvas, examinated_canvas, user_maria_anna, suggested_canvas, sample_route, actual_pearl)
    print_canvas_wp(suggested_canvas)
    
    choice = ''
    while len(user_maria_anna.visited_canvas) < total_canvas:
        while choice == '':
            choice = input("\nChoose the next canvas: ")
            try:
                tmp_choice = suggested_canvas[int(choice)]

                if sample_route[actual_pearl] not in get_pearl_from_canvas(tmp_choice):    
                    change_pearl = input("Attention! You're looking for another pearl, this need your move to another POI! Are you sure?(y/n): ")
                    if change_pearl == 'y':
                        previous_pearl = actual_pearl
                        user_maria_anna.change_pearl_satisfaction_value.append(user_maria_anna.satisfaction[-1])
                        user_maria_anna.change_pearl_counter+=1
                        choiced_canvas = tmp_choice
                        actual_pearl_str = get_pearl_from_canvas(choiced_canvas)
                        actual_pearl = sample_route.index(actual_pearl_str[0])
                        pr.print_route_pos(actual_pearl, sample_route)
                    elif change_pearl == 'n':
                        print("So, please, select another canvas!")
                        choice = ''
                else:
                    choiced_canvas = tmp_choice
            except:
                print("Wrong input, retry.")
                choice = ''
        
        print("You are looking the canvas: "+str(choiced_canvas)+"\n")
        user_maria_anna.preferences = update_profile_preferences(choiced_canvas, user_maria_anna,actual_pearl)
        suggested_canvas, examinated_canvas = get_next_canvas(choiced_canvas, sample_route, actual_pearl, user_maria_anna.canvas_in_pearl_counter[actual_pearl], user_maria_anna, 0)
        pl.plot_point(choiced_canvas, examinated_canvas, user_maria_anna, suggested_canvas, sample_route, actual_pearl)
        print_canvas_wp(suggested_canvas)
        print(f"\nWatched {user_maria_anna.canvas_in_pearl_counter} of {get_number_of_canvas_from_pearl(sample_route[actual_pearl])} canvas. Total canvas are: {total_canvas}")    
        choice = ''

    # pl.plot_satisfaction_2(user_maria_anna)
    print("End of the route! Byeee :3")