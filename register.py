import os
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

def create_registration_window():



    root = Tk()
    root.title("Face Recognition Attendance System")
    root.geometry("820x500")

    tk.Label(root, text="Employee Registration", fg="red", font=(None, 15)).place(x=290, y=5)

    tk.Label(root, text="Employee ID", font=(None, 11)).place(x=10, y=40)
    Label(root, text="Employee Name", font=(None, 11)).place(x=10, y=70)
    Label(root, text="Mobile", font=(None, 11)).place(x=10, y=100)
    Label(root, text="Email", font=(None, 11)).place(x=10, y=130)

    Button(root, text="Upload Image", font=(None, 11)).place(x=400, y=35)
    image_label = Label(root, text="Image", font=(None, 11))
    image_label.place(x=550, y=35)

    global e1
    global e2
    global e3
    global e4

    e1 = Entry(root, font=(None, 11))
    e1.place(x=140, y=40)

    e2 = Entry(root, font=(None, 11))
    e2.place(x=140, y=70)

    e3 = Entry(root, font=(None, 11))
    e3.place(x=140, y=100)

    e4 = Entry(root, font=(None, 11))
    e4.place(x=140, y=130)

    Button(root, text="Add",  height=2, width=10, font=(None, 11)).place(x=10, y=180)
    Button(root, text="update", height=2, width=10, font=(None, 11)).place(x=130, y=180)
    Button(root, text="Delete",  height=2, width=10, font=(None, 11)).place(x=250, y=180)
    Button(root, text="Back",  height=2, width=10, font=(None, 11)).place(x=370, y=180)
    Button(root, text="Exit",  height=2, width=10, font=(None, 11)).place(x=490, y=180)

    cols = ('Id', 'Name', 'Mobile', 'Email')
    listBox = ttk.Treeview(root, columns=cols, show='headings')

    for col in cols:
        listBox.heading(col, text=col, )
        listBox.grid(row=1, column=0, columnspan=2)
        listBox.place(x=10, y=250)




    root.mainloop()

create_registration_window()