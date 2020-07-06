from tkinter import *
import open_save as osf
from tkinter.simpledialog import askstring, askinteger, askfloat
import numpy as np
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from spectral.io.envi import *
import spectral.io.envi as envi
from spectral import imshow
import os
import functools
from Hyspeclib.hyspeclib.preprocessing import noise_removal


def quit():
    global top
    if messagebox.askyesno("Quit", message="Are you sure you want to quit?") == True:
        top.destroy()

top = Tk()
top.title("HyperImage")
top.geometry("3900x1200")
top.configure(bg="#37474f")

canvas = Canvas(top, width=3900, height=1200)
canvas.pack()

# Software name

widget = Label(canvas, text='HyperImage', fg='white', bg='#37474f', font='Ubuntu 50 bold italic', pady=595).pack()


# Creating the navigation bar

menubar = Menu(canvas)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=osf.open_file)
filemenu.add_command(label="Save", command=osf.save)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Bands", command=osf.open_band)
menubar.add_cascade(label="Edit", menu=editmenu)

exitmenu = Menu(menubar, tearoff=0)
exitmenu.add_command(label="Quit", command=quit)
menubar.add_cascade(label="Quit", menu=exitmenu)

top.config(menu=menubar)

top.mainloop()