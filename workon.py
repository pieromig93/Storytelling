import csv

if __name__ == '__main__':
    print("Starting...")
    
    file_kmeans_4C = open("/home/h93/Piero/Uni/Storytelling/kmeans4C.txt", "r")
    fout = open("/home/h93/Piero/Uni/Storytelling/points.txt", "r")
    csv_file = csv.reader(file_kmeans_4C, delimiter=',')

    visited_canvas = []
    tmp_canvas = []
    for element in csv_file:
        if element[1] == str(3):
            tmp_canvas.append(element[0])

    print("Suggested canvas: ")
    for i, canvas in enumerate(tmp_canvas):
        print(str(i)+") --> "+str(canvas))

    choice = ""
    while choice != 'exit':
        choice = input("Select canvas: ")
        try:
            visited_canvas.append(tmp_canvas[int(choice)])
        except:
            continue
        print("You have visited the canvas: "+str(tmp_canvas[int(choice)]))
