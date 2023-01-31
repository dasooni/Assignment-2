import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import pandas as pd
import numpy as np

column = ["x", "y", "letter"]
data1 = pd.read_csv("data1.csv", header=None, names=column)
data2 = pd.read_csv("data2.csv", header=None, names=column)
data_x = data1['x']
data_y = data1['y']
data_l = data1['letter'] 



width = 1000
height = 800

x_min = min(data_x)
x_max = max(data_x)
y_min = min(data_y)
y_max = max(data_y)

default_origin = (width / 2, height / 2)

#Abs range scaling, special case for quadrants.
x_range = max(abs(x_min), abs(x_max)) * 2 + 50
y_range = max(abs(y_min), abs(y_max)) * 2 + 50

kx = (x_max - x_min) / x_range
ky = (y_max - y_min) / y_range
#Max min scaling
x_scale = (width- 80) / (x_max - x_min) if x_max - x_min != 0 else 1
y_scale = (height- 80) / (y_max - y_min) if y_max - y_min != 0 else 1


def determine_quadrants(x, y):
    #x0, y0 relative to the screen
    #x, y relative to the data

    if x >= 0 and y >= 0:
        return 1
    elif x <= 0 and y >= 0:
        return 2
    elif x <= 0 and y <= 0:
        return 3
    else:
        return 4

def determine_quadrant_color(quadrant):
    if quadrant == 1:
        return "red"
    elif quadrant == 2:
        return "green"
    elif quadrant == 3:
        return "blue"
    elif quadrant == 4:
        return "yellow"
    else:
        return "black"

def euclidean_distance(x0, y0, x, y):
    x = width/2 + x * x_scale
    y = height/2 - y * y_scale

    return np.sqrt((x0-x)**2 + (y0-y)**2)

colors = []
colors2letters = {}
def determine_color(data_l, letter):
    colors = ['green', 'yellow', 'red', 'green', 'white', 'black', 'cyan']
    colors2letters = {letter: colors[i % len(colors)]
                      for i, letter in enumerate(data_l.unique())}

    return colors2letters[letter]

def unique_letters(data_l):
    return set(data_l.unique())
    
legend = []
def draw_legend(canvas, data_l):
    legend = tk.Canvas(canvas, width=100, height=100,
                       borderwidth=2, relief="groove")
    legend.place(x=20, y=30)

    legend_x = 15
    legend_y = 15

    # draw the legend
    for letter in unique_letters(data_l):
        legend.create_oval(legend_x, legend_y, legend_x +
                                20, legend_y + 20, fill=determine_color(data_l, letter))
        legend.create_rectangle(legend_x, legend_y, legend_x +
                                20, legend_y + 20, fill=determine_color(data_l, letter))
        legend.create_polygon(legend_x, legend_y, legend_x +
                                20, legend_y + 20, fill=determine_color(data_l, letter))                       

        legend.create_text(legend_x + 25, legend_y + 10, text=letter)
        legend_y += 30

def draw_tickers(canvas, x_scale, y_scale, xmin, xmax, ymin, ymax):
    for i in range(int(xmin), int(xmax), 10):
        # Positive side
        canvas.create_line(
            width / 2 + i * x_scale, height / 2 + 2, 
            width / 2 + i * x_scale, height / 2 - 2)
        canvas.create_text(
            width / 2 + i * x_scale, 
            height / 2 + 20, text=str(i), anchor=tk.N)

        # Negative side
        canvas.create_line(
            width / 2 - i * x_scale, height / 2 + 2, 
            width / 2 - i * x_scale, height / 2 - 2)
        canvas.create_text(
            width / 2 - i * x_scale, height / 2 + 20, 
            text=str(-i), anchor=tk.N)

    for i in range(int(ymin), int(ymax), 10):
        # Positive side
        canvas.create_line(
            width / 2 + 2, height / 2 - i * y_scale, 
            width / 2 - 2, height / 2 - i * y_scale)
        canvas.create_text(width / 2 + 20, 
        height / 2 - i * y_scale, text=str(i), anchor=tk.E)

        # Negative side
        canvas.create_line(
            width / 2 + 2, height / 2 + i * y_scale, width / 2 - 2, height / 2 + i * y_scale)
        canvas.create_text(
            width / 2 + 20, height / 2 + i * y_scale, text=str(-i), anchor=tk.E)


def draw_axes(canvas, x0, y0):
    # draw the axes
    canvas.create_line(0, y0, width, y0)
    canvas.create_line(x0, 0, x0, height)

px = 5
points_id = []
def draw_data(canvas, data_x, data_y, data_l, x_scale, y_scale, x0, y0):
    tags = ["clickable", "circle", "square", "triangle", "oval"]
    # draw the data
    for i in range(len(data_x)):
        x = data_x[i]
        y = data_y[i]
        letter = data_l[i]
        quadrant = determine_quadrants( x, y)
        color = determine_quadrant_color(quadrant)
        #Different shapes for each unique letter
        if letter == data_l.unique()[0]:
            points_id.append(canvas.create_oval(x0 + x * x_scale - px, y0- y * y_scale - px,
                               x0 + x * x_scale + px, y0- y * y_scale + px, fill=color, tag=tags))
            
        elif letter == data_l.unique()[1]:
            points_id.append(canvas.create_rectangle(x0 + x * x_scale - px, y0 - y * y_scale - px,
                                    x0 + x * x_scale + px, y0 - y * y_scale + px, fill=color, tag=tags))
        elif letter == data_l.unique()[2]:
            points_id.append(canvas.create_polygon(x0 + x * x_scale - px, y0 - y * y_scale - px,
                                  x0 + x * x_scale + px, y0- y * y_scale - px,
                                  x0 + x * x_scale, y0 - y * y_scale + px, fill=color, tag=tags))
        else: 
            points_id.append(canvas.create_oval(x0 + x * x_scale - px, y0- y * y_scale - px,
                               x0 + x * x_scale + px*1.1, y0- y * y_scale + px*1.1, fill=color, tag=tags))
        canvas.create_text(x0 + x * x_scale, y0 - y * y_scale + 15, text=letter, font = "Times 10")
    
    
    print("ids of the points: ", points_id)

# create the window
window = tk.Tk()
window.title("A2")
window.geometry("1000x800")

# create the canvas
canvas = tk.Canvas(window, width=width, height=height, borderwidth=2, relief="groove")
canvas.place(x=0, y=0)

def draw_on_start():
    draw_axes(canvas, default_origin[0], default_origin[1])
    draw_tickers(canvas, x_scale, y_scale, x_min, x_max, y_min, y_max)
    draw_legend(canvas, data_l)
    draw_data(canvas, data_x, data_y, data_l, x_scale, y_scale, 
    default_origin[0], default_origin[1])
    

def change_data():
    #TODO: Implement read_csv(csv), min_max_scale(min, max, data)
    #Scaling does not work properly...
    #Clear the canvas
    canvas.delete("all")
    #hardcoding YES SIR
    data2 = pd.read_csv("data2.csv", header=None, names=column)
    data_x = data2['x']
    data_y = data2['y']
    data_l = data2['letter'] 

    x_min = data_x.min()
    x_max = data_x.max()
    y_min = data_y.min()
    y_max = data_y.max()

    x_scale = (width/2.1) / (x_max - x_min)
    y_scale = (height/4) / (y_max - y_min)

    # Redraw x- and y-axis
    draw_axes(canvas, default_origin[0], default_origin[1])
    # Redraw tickers
    draw_tickers(canvas, x_scale, y_scale, x_min, x_max, y_min, y_max)
    # Redraw legend
    draw_legend(canvas, data_l)

    # Redraw data + add origo point
    draw_data(canvas, data_x, data_y, data_l, x_scale, y_scale, 
    default_origin[0], default_origin[1])

    canvas.create_rectangle(default_origin[0] - 10, default_origin[1] - 10,
        default_origin[0] + 10, default_origin[1] + 10, fill='red', tag="origo")

    window.update()
    
def on_left_click(event):
    #New origin is the point where the user clicked
    print("Left click")
    x0 = event.x
    y0 = event.y
    print(x0, y0)

    event_id = event.widget.find_withtag('current')[0]

    #Clear the canvas
    canvas.delete("all")

    canvas.create_oval(x0 - 12, y0 - 12, x0 + 12, y0 + 12,outline='red', width=5, tag="origo")
    # Redraw x- and y-axis
    canvas.create_line(0, y0, width - 50, y0)
    canvas.create_line(x0, 0, x0, height - 50)
    # Redraw tickers
    draw_tickers(canvas, x_scale, y_scale, x_min, x_max, y_min, y_max)
    # Redraw legend
    draw_legend(canvas, data_l)


    # Redraw data + add origo point to return to default state (data1)
    canvas.create_rectangle(default_origin[0] - 10, default_origin[1] - 10, 
        default_origin[0] + 10, default_origin[1] + 10, fill='red', tag="origo")
    draw_data(canvas, data_x, data_y, data_l, x_scale, y_scale, x0, y0)


def on_right_click(event):
    print("right click")
    print("position",event.x, event.y)

    # Find the five geometrically closest points using euclidean distance
    # and store their indices in a list
    closest_points = []
    for i in range(len(data_x)):
        distance = euclidean_distance(event.x, event.y, data_x[i], data_y[i]) #euclidean distance between the point and the data point
        closest_points.append(distance)

    closest_points = np.argsort(closest_points)[:6] # INDEX!
    # Change the color of the five closest points to green
    for i in closest_points:
        canvas.itemconfig(points_id[i], outline = 'red', width = 2,fill='green', tag ='origo')

    # Draw a line between the clicked point and the five closest points
    #for i in closest_points:
     #   canvas.create_line(event.x, event.y, data_x[i] * kx + event.x, event.y + data_y[i] * ky, fill='red')

    canvas.create_rectangle(default_origin[0] - 10, default_origin[1] - 10, 
    default_origin[0] + 10, default_origin[1] + 10, fill='red', tag="origo")

# Return to the default view
def reset(event):
    #Clear the canvas
    canvas.delete("all")
    #Redraw the canvas
    draw_on_start()

draw_on_start()
canvas.tag_bind("clickable", "<Button-1>", on_left_click)
canvas.tag_bind("origo", "<Double-Button-1>", reset)

canvas.tag_bind("clickable", "<Button-2>", on_right_click)
canvas.tag_bind("origo", "<Double-Button-2>", on_right_click)

canvas.tag_bind("clickable", "<Button-3>", on_right_click)
canvas.tag_bind("origo", "<Double-Button-3>", on_right_click)

change_data = ttk.Button(window, text="Change data", command=change_data)
change_data.pack()
change_data.place(x=20, y=5)

window.mainloop()



    