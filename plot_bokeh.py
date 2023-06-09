from bokeh.plotting import figure, show
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
import csv
import numpy as np
import main as m

"""
    TODO1: colorare in azzurro i canvas suggeriti, in grigio quelli già visitati, in rosso i non raggiungibili
    TODO2: realizzare l'immagine con le perle con all'interno i canvas, questo è però uno spazio geoposizionale 

    Tavola colori:
        - cyan: sono i canvas suggeriti
        - red: canvas attuali
        - green
"""
pearl = 0
chcanv_value = 0
chcanv_value2 = 0

def plot_point(canvas, examinated_canvas, user, suggested_canvas, route, actual_pearl):
    file_point = open("/home/h93/Piero/Uni/Storytelling/points.txt", "r")
    file_csv = csv.reader(file_point, delimiter=",")
    user_point = np.array(m.get_profile_point(user.preferences)).astype(float)
    # user_point = np.array(user_point).astype(float)
    X = []
    canvas_list = []
    actual_canvas_list = []
    suggested_canvas_point = []
    suggested_canvas_list = []
    reachable_canvas_point = []
    reachable_canvas_list = []
    visited_canvas_point = []
    visited_canvas_list = []
    
    for row in file_csv:
        
        if row[0] == canvas:
            actual_canvas_point = []
            actual_canvas_point.append([row[1], row[2]])
            actual_canvas_list.append(str(row[0].split("//")[1].split("/")[3])+", Canvas "+str(row[0].split("//")[1].split("/")[6]))
        elif row[0] in suggested_canvas:
            suggested_canvas_point.append([row[1], row[2]])
            suggested_canvas_list.append(str(row[0].split("//")[1].split("/")[3])+", Canvas "+str(row[0].split("//")[1].split("/")[6]))
        elif row[0] in examinated_canvas:
            reachable_canvas_point.append([row[1], row[2]])
            reachable_canvas_list.append(str(row[0].split("//")[1].split("/")[3])+", Canvas "+str(row[0].split("//")[1].split("/")[6]))
        elif row[0] in user.visited_canvas and len(user.visited_canvas)>0:
            visited_canvas_point.append([row[1], row[2]])
            visited_canvas_list.append(str(row[0].split("//")[1].split("/")[3])+", Canvas "+str(row[0].split("//")[1].split("/")[6]))
        else:
            X.append([row[1], row[2]])
            canvas_list.append(str(row[0].split("//")[1].split("/")[3])+", Canvas "+str(row[0].split("//")[1].split("/")[6]))

    file_point.close()
            
    # print(reachable_canvas_list)
    # print(len(reachable_canvas_list))
    X = np.array(X).astype(np.float_)
    actual_canvas_point = np.array(actual_canvas_point).astype(np.float_)
    suggested_canvas_point = np.array(suggested_canvas_point).astype(np.float_)
    reachable_canvas_point = np.array(reachable_canvas_point).astype(np.float_)
    visited_canvas_point = np.array(visited_canvas_point).astype(np.float_)
    
    TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,hover,save"
    TOOLTIPS = [
        ("(x, y)", "($x, $y)"),
        ("Canvas","@canvas_")
    ]
    
    source = ColumnDataSource(data=dict(
        x = X[:,0],
        y = X[:,1],
        canvas_ = canvas_list
    ))

    source_actual = ColumnDataSource(data=dict(
        x = actual_canvas_point[:,0],
        y = actual_canvas_point[:,1],
        canvas_ = actual_canvas_list
    ))

    p = figure(title = "BTE-Space", width=1200, height= 800, x_axis_label = "Beni", y_axis_label = "Tecniche Edilizie", tools=TOOLS, tooltips=TOOLTIPS, y_range =(-0.01, 0.35))
    
    profile_point = p.triangle(
            x = user_point[0],
            y = user_point[1],
            legend_label="User",
            fill_color="green",
            line_color="black", size = 18)
    
    actual_canvas_r = p.circle(
        source = source_actual,
        legend_label="Actual Canvas",
        fill_color="red",
        line_color="black", size = 18)
    

    canvas_r = p.circle(
        source=source,
        legend_label="Other Canvas",
        fill_color="plum",
        fill_alpha=0.5,
        line_color="blue", size = 12)

    renders = [canvas_r, actual_canvas_r]
    
    if len(reachable_canvas_list) > 2:

        source_reachable = ColumnDataSource(data=dict(
            x = reachable_canvas_point[:,0],
            y = reachable_canvas_point[:,1],
            canvas_ = reachable_canvas_list
        ))
    
        canvas_reachable_r = p.circle(
            source=source_reachable,
            legend_label="Reachable Canvas",
            fill_color="lightgreen",
            line_color="black", size = 12)
        renders.append(canvas_reachable_r)

    if len(visited_canvas_list) > 0:
        source_visited = ColumnDataSource(data=dict(
            x = visited_canvas_point[:,0],
            y = visited_canvas_point[:,1],
            canvas_ = visited_canvas_list
        ))

        canvas_visited_r = p.circle(
        source=source_visited,
        legend_label="Visited Canvas",
        fill_color="black",
        line_color="black", size = 12)

        renders.append(canvas_visited_r) 
    
    if len(suggested_canvas_list)>0:
        source_suggested = ColumnDataSource(data=dict(
            x = suggested_canvas_point[:,0],
            y = suggested_canvas_point[:,1],
            canvas_ = suggested_canvas_list
            )) 
        
        suggested_canvas_r = p.circle(
            source = source_suggested,
            legend_label="Suggested Canvas",
            fill_color="cyan",
            fill_alpha=0.9,
            line_color="blue", size = 16)
        
        renders.append(suggested_canvas_r)

    p.hover.renderers = renders 
    show(p)


def plot_satisfaction_2(user):
    
    TOOLTIPS = [
        ("(x, y)", "($x, $y)"),
        ("Value","@value")
    ]
    
    p = figure(title = "Satisfaction-Space", width=800, height= 800, x_axis_label = "Visited Canvas", y_axis_label = "Satisfaction", tooltips=TOOLTIPS)
    x1 = []

    for i, vc in enumerate(user.visited_canvas):
        x1.append(i+1)

    
    source_sat = ColumnDataSource(data=dict(
        x = x1,
        y = user.satisfaction,
        value = user.satisfaction
    ))

    sat = p.line(source=source_sat, line_width=3, legend_label="Satisfaction")

    for i in user.change_pearl_satisfaction_value:
        p.line(x=x1, y=i, line_width = 3, color="red", line_alpha = 0.7, line_dash = "dashed", legend_label="Change Pearl")
    
    p.hover.renderers = [sat]
    p.legend.location = "top_left" 
    print(f"The user satisfaction is: {user.satisfaction}")
    show(p)

def plot_satisfaction_users(users):

        sat = []
        TOOLTIPS = [
            ("(x, y)", "($x, $y)"),
            ("Value","@value")
        ]
        
        p = figure(title = "Satisfaction-Space", width=800, height= 800, x_axis_label = "Visited Canvas", y_axis_label = "Satisfaction", tooltips=TOOLTIPS)
        
        for user in users:
            x1 = []
            for i, vc in enumerate(user.visited_canvas):
                x1.append(i+1)

            source_sat = ColumnDataSource(data=dict(
                x = x1,
                y = user.satisfaction,
                value = user.satisfaction
            ))

            sat.append(p.line(source=source_sat, line_width=3, legend_label="Satisfaction of "+user.name, color = user.color))
            print(f"The user {user.name} satisfaction is: {user.satisfaction}")
            for i in user.change_pearl_satisfaction_value:
                p.line(x=x1, y=i, line_width = 3, color="red", line_alpha = 0.7, line_dash = "dashed", legend_label="Change Pearl")
        
        p.hover.renderers = sat
        p.legend.location = "top_left" 
        
        show(p)

