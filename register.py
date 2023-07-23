import os
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import pymysql
from PIL import Image, ImageTk

def create_registration_window():

    def GetValue(event):
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)

        row_id = listBox.selection()[0]
        select = listBox.set(row_id)
        e1.insert(0, select['id'])
        e2.insert(0, select['empname'])
        e3.insert(0, select['mobile'])
        e4.insert(0, select['salary'])

    def show():
        mysqldb = pymysql.connect(host="localhost", user="root", password="", database="pfrsdb")
        mycursor = mysqldb.cursor()
        mycursor.execute("SELECT Id,Name,Mobile,Email FROM registration")
        records = mycursor.fetchall()
        print(records)

        for i, (emplyid, emplyname, mobile, email) in enumerate(records, start=1):
            listBox.insert("", "end", values=(emplyid, emplyname, mobile, email))

        mysqldb.close()

    def convert_image_to_binary_data(image_path):
        with open(image_path, 'rb') as file:
            binary_data = file.read()
        return binary_data

    def upload_image():
        global img_data
        global image

        file_path = filedialog.askopenfilename()
        img_data = convert_image_to_binary_data(file_path)

        temp_file_path = "temp_image.jpg"
        with open(temp_file_path, 'wb') as file:
            file.write(img_data)

        image = Image.open(temp_file_path)
        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)

        image_label.config(image=photo)
        image_label.image = photo

        os.remove(temp_file_path)


    root = Tk()
    root.title("Face Recognition Attendance System")
    root.geometry("820x500")

    tk.Label(root, text="Employee Registration", fg="red", font=(None, 15)).place(x=290, y=5)

    tk.Label(root, text="Employee ID", font=(None, 11)).place(x=10, y=40)
    Label(root, text="Employee Name", font=(None, 11)).place(x=10, y=70)
    Label(root, text="Mobile", font=(None, 11)).place(x=10, y=100)
    Label(root, text="Email", font=(None, 11)).place(x=10, y=130)

    Button(root, text="Upload Image", command=upload_image, font=(None, 11)).place(x=400, y=35)
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


    listBox.bind('<Double-Button-1>', GetValue)
    show()
    root.mainloop()


create_registration_window()