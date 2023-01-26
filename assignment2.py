import tkinter as tk
import pandas as pd

column = ["x", "y", "letter"]
data1 = pd.read_csv("data1.csv", header=None, names=column)
data2 = pd.read_csv("data2.csv", header=None, names=column)

data1_x = data1['x']
data1_y = data1['y']
data1_l = data1['letter']

width = 1000
height = 800

x_min = min(data1_x)
x_max = max(data1_x)

y_min = min(data1_y)
y_max = max(data1_y)

x_scale = width / (x_max- x_min)
y_scale = height / (y_max - y_min)

window = tk.Tk()  # The window is an object of type 'tk'
window.title("Scatter Plot")  # Title
window.geometry(f"{width}x{height}")

canvas = tk.Canvas(window, width=width, height=height, bg="white")
canvas.pack()

canvas.create_line(width/2, height-50, width/2, 50)  # draw x-axis
canvas.create_line(50, height/2, width-50, height/2)  # draw y-axis


# This function should create a scatter plot of the data
# using tkinter, a gui library
def scatter(x,y):

    #ticker for x-axis
    for i in range (int(x_min), int(x_max), 10):
        canvas.create_line(width / 2 + i * x_scale, height/2 + 5, width/2 + 2*x_scale, height/2 - 5)
        canvas.create_text(width / 2 + i * x_scale, height/2 + 20, text=str(i), anchor=tk.S)

        canvas.create_line(width/2 - i * x_scale, height/2 + 5, width/2 - i*x_scale, height/2 -5)
        canvas.create_text(width/2 - i*x_scale, height /2 + 20, text = str(-i), anchor=tk.S)

    #ticker for y-axis
    for i in range( int(y_min), int(y_max),  10):
        canvas.create_line(width / 2 + 5, height/2 - i*y_scale , width/2 -5, height/2 - i* y_scale)
        canvas.create_text(width/2+ 20, height/2 - i * y_scale, text = str(i), anchor=tk.E)

        canvas.create_line(width/2 + 5, height / 2 + i * y_scale, width/2 - 5, height/2 + i*y_scale)
        canvas.create_text(width/2 + 20, height / 2 + i*y_scale, text = str(-i), anchor=tk.E)


    # draw the points
    for j in range(len(x)):
        #canvas.create_oval(x_scale * (x[j] - min(data1_x)), y_scale * (y[j] - min(data1_y)), x_scale * (x[j] - min(data1_x))+5, y_scale * (y[j] - min(data1_y))+5, fill = 'red')
        canvas.create_oval(width / 2 + x[j] * x_scale - 2.5, height / 2 - y[j] * y_scale - 2.5, width/2 + x[j] * x_scale + 5, height/2 - y[j] * y_scale + 5, fill='blue')
        
    window.mainloop()


scatter(data1_x, data1_y)


