import possible_route as pr
import create_cluster as cr
import random
import time
import csv
import math
import user

visited_pearl = []
visited_canvas = []

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
        if actual_pearl == 0:
            if row[0] == route[actual_pearl] or row[0] == route[actual_pearl+1]:
                if cr.remove_prefix(row[1]) == canvas and row[0] == route[actual_pearl]:
                    return canvas_counter/get_number_of_canvas_from_pearl(route[actual_pearl])
                elif cr.remove_prefix(row[1]) == canvas and row[0] == route[actual_pearl+1]:
                    return  get_number_of_canvas_from_pearl(route[actual_pearl])/canvas_counter     
        # elif actual_pearl == len(route)-1:
        #     if row[0] == route[actual_pearl] or row[0] == route[actual_pearl-1]:
        #         return 2
        # else:
        #     if row[0] == route[actual_pearl] or row[0] == route[actual_pearl+1] or row[0] == route[actual_pearl-1]:
        #         return 3
    
    file_pearl.close()
    return -1

def get_profile_point(preferences):
    return [preferences[0]/preferences[2], preferences[1]/preferences[2]]

def update_profile_preferences(canvas, user):

    # aggiungo il canvas alla lista di canvas visitati dell'utente
    user.visited_canvas.append(str(canvas))
    
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

    return [user_num_x, user_num_y, user_den]

def get_next_canvas(actual_canvas, route, actual_pearl, counter, user, filtered_canvas):
    file = open("/home/h93/Piero/Uni/Storytelling/points.txt","r")
    file_csv = csv.reader(file, delimiter=',')
    profile_point = get_profile_point(user.preferences)
    actual_canvas_point = get_point_from_canvas(actual_canvas)
    distances_between_canvas = []
    for row in file_csv:
        pi = check_canvas_pearl(cr.remove_prefix(str(row[0])), route, actual_pearl, counter)
        # se qui nell'if aggiungo anche la condizione se presente o meno nella filtered_list lavoro solo su quelli appartenenti a quel cluster
        if pi > 0 and str(row[0]) not in user.visited_canvas:    
        # if check_canvas_pearl(cr.remove_prefix(str(row[0])), route, actual_pearl, counter) > 0 and str(row[0]) not in user.visited_canvas and str(row[0]) in filtered_canvas:    
            alpha1 = math.sqrt(pow(float(actual_canvas_point[0])-float(row[1]),2)+pow(float(actual_canvas_point[1])-float(row[2]),2))
            alpha2 = math.sqrt(pow(float(profile_point[0])-float(row[1]),2)+pow(float(profile_point[1])-float(row[2]),2))
            # print("Canvas: "+str(cr.remove_prefix(str(row[0])))+"\nDistance(alpha1): "+str(alpha1)+" \nDistance(alpha2): "+str(alpha2)+ "\nTotal distance: "+str(pi*(alpha1+alpha2))+"\npi: "+str(pi)+"\n")
            distances_between_canvas.append((row[0], pi*(alpha1+alpha2)))
    
    # print("CANVAS ANALYZED: "+str(len(distances_between_canvas))+"\n")
    distances_between_canvas.sort(key=lambda a:a[1])
    suggested_canvas = []
    for i in range(2):
        suggested_canvas.append(distances_between_canvas[i][0])
    file.close()
    return suggested_canvas

# ? ―――――――――――――――――――――――――――――――――― MAIN ――――――――――――――――――――――――――――――――――

if __name__ == '__main__':
    print("Starting...")    
    
    user_maria_anna = user.User("MariaAnna", [])
    # user_max_time = input("Enter time max(sec):")
    # possibile_route = pr.pearls_time_filter(240)
    # route = random.choice(possibile_route)
    sample_route = ('extended_mara_with_poi.12._Complesso_termale', 'extended_mara_with_poi.2._Porta_Maggiore_e_le_mura_di_Norba', 'extended_mara_with_poi.14._Tempio_di_Giunone_Lucina')
    print(sample_route)
    actual_pearl = 0
    pr.print_route_pos(actual_pearl, sample_route)
    
    canvas_list = pr.get_canvas_from_pearl(sample_route[actual_pearl])
    print("The canvas inside this perl are: ")
    for i, c in enumerate(canvas_list):
        print(str(i)+" "+str(c))
    
    # prendo i canvas contenuti nello stesso cluster del canvas iniziale scelto in modo da fornire sempre contenuti affini al primo
    filtered_canvas = pr.filter_canvas(canvas_list)
    print("\nBased on your preferences, I suggest you this canvas: ")
    for i,fc in enumerate(filtered_canvas):
        print(str(i)+")"+str(fc))
    

    canvas_counter_in_pearl = 0
    initial_choice = input("\nChoose the first canvas: ")
    # starting_canvas = filtered_canvas[int(choiced_canvas)]
    # print("Starting Canvas: "+str(starting_canvas))
    # start_time_on_actual_canvas = time.time()
    # starting_canvas = "ext_mara.https://cosme.unicampania.it/rasta/norba/7-TERME/index.json/canvas/1"
    # test_canvas = "ext_mara.https://cosme.unicampania.it/rasta/norba/7-TERME/index.json/canvas/5"
    # user_maria_anna.preferences = update_profile_preferences(starting_canvas, user_maria_anna)

    # canvas_counter_in_pearl += 1
    # user_maria_anna.preferences = update_profile_preferences(test_canvas, user_maria_anna)
    # canvas_counter_in_pearl += 1
    
    # suggested_canvas = get_next_canvas(starting_canvas, sample_route, actual_pearl, canvas_counter_in_pearl, user_maria_anna, 0)
    # print("The nearest canvas, between all are: ")
    # for i,fc in enumerate(suggested_canvas):
    #     print(str(i)+")"+str(fc))
    
    choice = ''
    choiced_canvas = filtered_canvas[int(initial_choice)]
    print("\nYou are looking the canvas: "+str(choiced_canvas))
    user_maria_anna.preferences = update_profile_preferences(choiced_canvas, user_maria_anna)
    canvas_counter_in_pearl += 1
    suggested_canvas = get_next_canvas(choiced_canvas, sample_route, actual_pearl, canvas_counter_in_pearl, user_maria_anna, 0)
    for i,fc in enumerate(suggested_canvas):
        print(str(i)+")"+str(fc))
    
    while choice != 'exit':
        choice = input("\nChoose the next canvas: ")
        choiced_canvas = suggested_canvas[int(choice)]
        print("\nYou are looking the canvas: "+str(choiced_canvas))
        user_maria_anna.preferences = update_profile_preferences(choiced_canvas, user_maria_anna)
        canvas_counter_in_pearl+=1

        if get_number_of_canvas_from_pearl(sample_route[actual_pearl]) == canvas_counter_in_pearl:
            print("You have to change pearl!")

        suggested_canvas = get_next_canvas(choiced_canvas, sample_route, actual_pearl, canvas_counter_in_pearl, user_maria_anna, 0)
        for i,fc in enumerate(suggested_canvas):
            print(str(i)+")"+str(fc))

        print(f"\nWatched {canvas_counter_in_pearl} of {get_number_of_canvas_from_pearl(sample_route[actual_pearl])} canvas")