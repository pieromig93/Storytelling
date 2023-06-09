import tkinter as tk
from PIL import Image, ImageTk
import possible_route as pr
import create_cluster as cr
import debug_print as dp
import random
import time
import csv
import math
import user
import os
import urllib.request
import json 
from io import BytesIO
import requests
import tkinter.messagebox as messagebox

def print_canvas_wp(canvas_list):
    for i,fc in enumerate(canvas_list):
            print(str(i)+")"+str(fc)+", "+str(get_pearl_from_canvas(fc)))

def print_canvas(canvas_list):
    for i, c in enumerate(canvas_list):
        print(str(i)+") "+str(c))

def get_pearl_from_canvas(canvas):
    file = open("pearls.txt", "r")
    file_csv = csv.reader(file, delimiter=',')

    pearls_that_contain_canvas = []

    for row in file_csv:
        if str(canvas) == str(row[1]):
            pearls_that_contain_canvas.append(row[0])    
    file.close()

    return pearls_that_contain_canvas

def get_number_of_canvas_from_pearl(pearl):
    file_pearl = open("pearls.txt","r")
    file_pearl_csv = csv.reader(file_pearl, delimiter=',')
    canvas_counter = 0
    for row in file_pearl_csv:
        if row[0] == pearl:
            canvas_counter += 1
    
    file_pearl.close()
    return canvas_counter

def get_point_from_canvas(actual_canvas):
    file = open("points.txt","r")
    file_csv = csv.reader(file, delimiter=',')
    actual_canvas_point = []
    for row in file_csv:
        if str(row[0]) == str(actual_canvas):
            actual_canvas_point.append(row[1])
            actual_canvas_point.append(row[2])
    
    file.seek(0,0)
    return actual_canvas_point

def check_canvas_pearl(canvas, route, actual_pearl, canvas_counter):
    file_pearl = open("pearls.txt","r")
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

    return [user_num_x, user_num_y, user_den]

# ! FUNZIONE CHE RESTITUISCE LA LISTA CONTENENTE I CANVAS PIÙ VICINI
def get_next_canvas(actual_canvas, route, actual_pearl, canvas_counter, user, filtered_canvas):
    
    # apro il file dei punti
    file = open("points.txt","r")
    file_csv = csv.reader(file, delimiter=',')
    
    # recuper i punti dai quali calcolerò la distanza
    profile_point = get_profile_point(user.preferences)
    actual_canvas_point = get_point_from_canvas(actual_canvas)
    
    # struttura contenente i canvas con le relative distanze
    distances_between_canvas = []
    
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
            
            distances_between_canvas.append((row[0], pi*(alpha1+alpha2), get_pearl_from_canvas(row[0])))
    
    # print("CANVAS ANALYZED: "+str(len(distances_between_canvas))+"\n")
    distances_between_canvas.sort(key=lambda a:a[1])
    
    print(dp.debug_line)
    for d in distances_between_canvas:
        print(d)
    print(dp.end_line+"\n")
    suggested_canvas = []
    for i in range(3):
        suggested_canvas.append(distances_between_canvas[i][0])
    file.close()

    return suggested_canvas


# Function to handle the selection of a smaller image
def select_image(image_path, tmp_choice, has_image):
    # Load the selected image
    global actual_pearl
    global choiced_canvas
    global user
    global sample_route
    global canvas_counter
    global filtered_canvas
    global actual_canvas
    global actual_canvas_str
    global actual_pearl_str

    skip = 0
    if sample_route[actual_pearl] not in get_pearl_from_canvas(tmp_choice):
        #open popup alert
        change_pearl = messagebox.askquestion("Image Selected", "Attention! You're looking for another pearl, this need your move to another POI! Are you sure?(y/n): ", icon="warning")
        if change_pearl == 'yes':
            choiced_canvas = tmp_choice
            actual_pearl_str = get_pearl_from_canvas(choiced_canvas)
            actual_pearl = sample_route.index(actual_pearl_str[0])
            pr.print_route_pos(actual_pearl, sample_route)
        else:
            messagebox.showinfo("Image Selected", "So Please Select Another Canvas")            
            skip = 1
    else:
        choiced_canvas = tmp_choice

    if(skip == 0):
        user_maria_anna.preferences = update_profile_preferences(choiced_canvas, user_maria_anna, actual_pearl)
        suggested_canvas = get_next_canvas(choiced_canvas, sample_route, actual_pearl, user_maria_anna.canvas_in_pearl_counter[actual_pearl], user_maria_anna, 0)
        print_canvas_wp(suggested_canvas)
        Debug.configure(text="Canvas: "+str(choiced_canvas)+"\nPearl: "+str(actual_pearl)+"\nRoute: "+str(sample_route)+"\nCanvas counter: "+str(user_maria_anna.canvas_in_pearl_counter[actual_pearl])+"\n\nSuggested canvas: "+str(suggested_canvas))
        if(has_image == 0):
            image = Image.open(image_path)
            image = image.resize((300, 300))  # Resize the image to fit the label
            photo = ImageTk.PhotoImage(image)
            central_image.configure(image=photo)
            central_image.image = photo
        else:
            image = Image.open(BytesIO(image_path))
            image = image.resize((200, 200))
            photo = ImageTk.PhotoImage(image)
            central_image.configure(image=photo)
            central_image.image = photo
        to_suggest_images = []
        for x in suggested_canvas:
            link = x.split('mara.')[1].split('/canvas')[0]
            #open the remote json file

            with urllib.request.urlopen(link) as url:
                dat = url.read().decode()
                data = json.loads(dat)   
                for y in data['items']:
                    if(y['id'] == x.split('mara.')[1]):
                        try:
                            to_suggest_images.append([y['id'],y['items'][0]['items'][0]['body']['id']])
                        except:
                            to_suggest_images.append([y['id'],'no_image'])
        for i in range(3):
            if(to_suggest_images[i][1] == 'no_image'):
                image = Image.open('placeholder.png')
                image = image.resize((200, 200))  # Ridimensiona l'immagine per adattarla all'etichetta
                photo = ImageTk.PhotoImage(image)
                small_images[i].configure(image=photo)
                small_images[i].image = photo
                text_labels[i].configure(text=to_suggest_images[i][1].split('/')[-1].split('.')[0])

                small_images[i].bind("<Button-1>", lambda e, i=i: select_image('placeholder.png', suggested_canvas[i], 0))

            else:
                url = to_suggest_images[i][1]  # Replace with your remote image URL
                response = requests.get(url)
                image_data = response.content
                image = Image.open(BytesIO(image_data))
                image = image.resize((200, 200))
                photo = ImageTk.PhotoImage(image)
                small_images[i].configure(image=photo)
                small_images[i].image = photo
                #update text_label[i]
                text_labels[i].configure(text=to_suggest_images[i][1].split('/')[-1].split('.')[0])
                small_images[i].bind("<Button-1>", lambda e, i=i: select_image(image_data, suggested_canvas[i], 1))
# Create the main window
window = tk.Tk()
window.title("Image Selector")
window.geometry("650x800")  # Set the width and height as desired
global actual_pearl
global choiced_canvas
global user_maria_anna
global sample_route
global canvas_counter
global filtered_canvas
global actual_canvas
global actual_canvas_str
global actual_pearl_str
sample_route = ('extended_mara_with_poi.12._Complesso_termale', 
                'extended_mara_with_poi.2._Porta_Maggiore_e_le_mura_di_Norba', 
                'extended_mara_with_poi.14._Tempio_di_Giunone_Lucina')
user_maria_anna = user.User("MariaAnna", [], sample_route)
actual_pearl = 0
total_canvas = 0
for pearl in sample_route:
    total_canvas += get_number_of_canvas_from_pearl(pearl)

canvas_list = pr.get_canvas_from_pearl(sample_route[actual_pearl])
filtered_canvas = pr.filter_canvas(canvas_list)
print("\nBased on clustering, I suggest you this canvas: ")
to_suggest_images = []
for x in filtered_canvas:
    link = x.split('mara.')[1].split('/canvas')[0]
    #open the remote json file

    with urllib.request.urlopen(link) as url:
        dat = url.read().decode()
        data = json.loads(dat)   
        for y in data['items']:
            if(y['id'] == x.split('mara.')[1]):
                try:
                    to_suggest_images.append([y['id'],y['items'][0]['items'][0]['body']['id']])
                except:
                    to_suggest_images.append([y['id'],'no_image'])



Debug = tk.Label(window, text="")
Debug.pack()


title = tk.Label(window, text="Selected image:")
title.pack()

# Create the placeholder image
placeholder_image = ImageTk.PhotoImage(Image.open("placeholder.png"))

# Create the central image label
central_image = tk.Label(window, width=500, height=500)
central_image.pack(pady=10)
central_image.configure(image=placeholder_image)

# Insert a divider with a line
tk.Frame(height=2, bd=1, relief="sunken").pack(fill="x")

# Create the frame for the three smaller images
frame = tk.Frame(window)
frame.pack(pady=10)

# Create the three smaller image labels
small_images = []
text_labels = []
for i in range(3):
    try:
        if(to_suggest_images[i][1] == 'no_image'):
            image = Image.open('placeholder.png')
            image = image.resize((200, 200))
            photo = ImageTk.PhotoImage(image)

            # Create a frame to contain the image and text
            frame = tk.Frame(window)
            frame.pack(side="left", padx=10)

            # Create the image label inside the frame
            image_label = tk.Label(frame, image=photo)
            image_label.image = photo
            image_label.pack()

            # Create the text label below the image inside the frame
            text_label_bottom = tk.Label(frame, text=to_suggest_images[i][1].split('/')[-1].split('.')[0])
            text_label_bottom.pack()

            image_label.bind("<Button-1>", lambda e, i=i: select_image('placeholder.png', filtered_canvas[i],0))
            text_labels.append(text_label_bottom)
            small_images.append(image_label)
        else:
            url = to_suggest_images[i][1]  # Replace with your remote image URL
            response = requests.get(url)
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            image = image.resize((200, 200))
            photo = ImageTk.PhotoImage(image)

            # Create a frame to contain the image and text
            frame = tk.Frame(window)
            frame.pack(side="left", padx=10)

            # Create the image label inside the frame
            image_label = tk.Label(frame, image=photo)
            image_label.image = photo
            image_label.pack()

            # Create the text label below the image inside the frame
            text_label_bottom = tk.Label(frame, text=to_suggest_images[i][1].split('/')[-1].split('.')[0])
            text_label_bottom.pack()

            image_label.bind("<Button-1>", lambda e, i=i: select_image(image_data, filtered_canvas[i], 1))
            text_labels.append(text_label_bottom)

            small_images.append(image_label)

    except IOError:
        print("Error loading image:", to_suggest_images[i])

# Start the main event loop
window.mainloop()
