import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import pymysql
from tkinter import Entry
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from tkinter import Toplevel, Label




def create_registration_window():
    def exit_application():
        root.destroy()

    def back_to_main():
        pass


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

    def Add():
        emplyid = e1.get()
        emplyname = e2.get()
        mobile = e3.get()
        email = e4.get()
        img = img_data

        mysqldb = pymysql.connect(host="localhost", user="root", password="", database="pfrsdb")
        mycursor = mysqldb.cursor()

        try:
            sql = "INSERT INTO  registration (Id,Name,Mobile,Email,Image) VALUES (%s, %s, %s, %s, %s)"
            val = (emplyid, emplyname, mobile, email, img)
            mycursor.execute(sql, val)
            mysqldb.commit()
            lastid = mycursor.lastrowid
            messagebox.showinfo("information", "Employee inserted successfully...")
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)
            image_label.config(image=None)
            image_label.image = None
            e1.focus_set()
        except Exception as e:
            print(e)
            mysqldb.rollback()
            mysqldb.close()

    def update():
        emplyid = e1.get()
        emplyname = e2.get()
        mobile = e3.get()
        email = e4.get()
        img = img_data

        mysqldb = pymysql.connect(host="localhost", user="root", password="", database="pfrsdb")
        mycursor = mysqldb.cursor()

        try:
            sql = "Update registration set Name= %s,Mobile= %s,Email= %s,Image=%s where id= %s"
            val = (emplyname, mobile, email, img, emplyid)
            mycursor.execute(sql, val)
            mysqldb.commit()
            lastid = mycursor.lastrowid
            messagebox.showinfo("information", "Record Updateddddd successfully...")

            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)
            e1.focus_set()

        except Exception as e:

            print(e)
            mysqldb.rollback()
            mysqldb.close()

    def delete():
        emplyid = e1.get()

        mysqldb = pymysql.connect(host="localhost", user="root", password="", database="pfrsdb")
        mycursor = mysqldb.cursor()

        try:
            sql = "delete from registration where id = %s"
            val = (emplyid)
            mycursor.execute(sql, val)
            mysqldb.commit()
            lastid = mycursor.lastrowid
            messagebox.showinfo("information", "Record Deleteeeee successfully...")

            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)
            e1.focus_set()

        except Exception as e:

            print(e)
            mysqldb.rollback()
            mysqldb.close()

    def show():
        mysqldb = pymysql.connect(host="localhost", user="root", password="", database="pfrsdb")
        mycursor = mysqldb.cursor()
        mycursor.execute("SELECT Id,Name,Mobile,Email FROM registration")
        records = mycursor.fetchall()
        print(records)

        for i, (emplyid, emplyname, mobile, email) in enumerate(records, start=1):
            listBox.insert("", "end", values=(emplyid, emplyname, mobile, email))

        mysqldb.close()

    root = Tk()
    root.title("Face Recognition Attendance System")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 800) // 2
    y = (screen_height - 485) // 2
    root.geometry(f"800x485+{x}+{y}")
    root.resizable(False, False)

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

    Button(root, text="Add", command=Add, height=2, width=10, font=(None, 11)).place(x=10, y=180)
    Button(root, text="update", command=update, height=2, width=10, font=(None, 11)).place(x=130, y=180)
    Button(root, text="Delete", command=delete, height=2, width=10, font=(None, 11)).place(x=250, y=180)
    Button(root, text="Back", command=back_to_main, height=2, width=10, font=(None, 11)).place(x=370, y=180)
    Button(root, text="Exit", command=exit_application, height=2, width=10, font=(None, 11)).place(x=490, y=180)

    cols = ('Id', 'Name', 'Mobile', 'Email')
    listBox = ttk.Treeview(root, columns=cols, show='headings')

    for col in cols:
        listBox.heading(col, text=col, )
        listBox.grid(row=1, column=0, columnspan=2)
        listBox.place(x=10, y=250)

    show()
    listBox.bind('<Double-Button-1>', GetValue)

    root.mainloop()
