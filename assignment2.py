import tkinter as tk
import pandas as pd

column = ["x", "y", "letter"]
data1 = pd.read_csv("data1.csv", header=None, names=column)
data2 = pd.read_csv("data2.csv", header=None, names=column)

data1_x = data1['x']
data1_y = data1['y']
data1_l = data1['letter']


# This function should create a scatter plot of the data
# using tkinter, a gui library
def scatter(x,y):

    X = min(580 / x)
    Y = min(580 / y)

    window = tk.Tk()

    window.title("Scatter Plot") #Titel
    window.geometry("600x600") # Size
    window.configure(background="grey") #Background color
    window.resizable(width=False, height=False) #Can't resize

    canvas = tk.Canvas(window, width=580, height=580, bg="white")
    canvas.pack(pady=10)

    canvas.create_line(50,550,550,550, width = 2) # draw x-axis
    canvas.create_line(50,550,50,50, width=2) # draw y-axis

    for i in range(len(x)):
        canvas.create_oval(X[i], Y[i], X[i]+5, Y[i]+5, fill="blue")

    window.mainloop()


scatter(data1_x , data1_y)

