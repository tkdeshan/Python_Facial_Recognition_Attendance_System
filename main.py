import os
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, filedialog

import cv2
import face_recognition as fr
from PIL import Image, ImageTk
import numpy as np
import pyttsx3
import pymysql


def show_register_window():
    root.withdraw()
    register_window.deiconify()


def show_main_window():
    register_window.withdraw()
    root.deiconify()


def exit_application():
    root.destroy()


engine = pyttsx3.init()


def speaknow(text):
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def retrieve_images_and_names_from_database():
    try:
        mysqldb = pymysql.connect(host="localhost", user="root", password="", database="pfrsdb")
        mycursor = mysqldb.cursor()
        mycursor.execute("SELECT Image, Name FROM registration")
        # Assuming you have a table named 'images' with columns 'id', 'image_data', and 'name'

        images = []
        names = []
        for image_data, name in mycursor.fetchall():
            # Assuming your image_data column is of type BLOB
            images.append(np.frombuffer(image_data, dtype=np.uint8))
            names.append(name)

        mycursor.close()
        mysqldb.close()

        return images, names

    except Exception as e:
        print("Error retrieving images and names:", e)
        return [], []


known_face_encodings = []
known_face_names = []

# Retrieve images and names from the database
images_from_database, names_from_database = retrieve_images_and_names_from_database()
for image_data, name in zip(images_from_database, names_from_database):
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    # Make sure to check if any face is detected before attempting to get the first face encoding
    face_encodings = fr.face_encodings(image)
    if len(face_encodings) > 0:
        image_face_encoding = face_encodings[0]
        known_face_encodings.append(image_face_encoding)
        known_face_names.append(name)



root = tk.Tk()
root.title("Main Window")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 800) // 2
y = (screen_height - 485) // 2
root.geometry(f"800x485+{x}+{y}")
root.resizable(False, False)

frame_label = Label(root)
frame_label.place(x=2, y=2)

video_capture = cv2.VideoCapture(0)

text = "Please try again."


def update_frame():
    global text
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]
    fc_location = fr.face_locations(rgb_frame)
    fc_encodings = fr.face_encodings(rgb_frame, fc_location)

    for (top, right, bottom, left), face_encoding in zip(fc_location, fc_encodings):
        name = "Unknown"
        text = "Please try again. If not registered, please register first."
        matches = fr.compare_faces(known_face_encodings, face_encoding)

        fc_distances = fr.face_distance(known_face_encodings, face_encoding)
        match_index = np.argmin(fc_distances)

        if matches[match_index]:
            name = known_face_names[match_index]
            text = "Good Morning " + name + ". You are presented. Have a nice day."

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
    frame_tk = ImageTk.PhotoImage(image=frame)
    frame_label.config(image=frame_tk)
    frame_label.image = frame_tk

    root.after(10, update_frame)  # Update the frame after 10 milliseconds

update_frame()

Button(root, text="Present", command=lambda: speaknow(text), height=2, width=10, font=(None, 11)).place(x=670, y=100)
Button(root, text="Add new", command=show_register_window, height=2, width=10, font=(None, 11)).place(x=670, y=200)
Button(root, text="Exit", command=exit_application, height=2, width=10, font=(None, 11)).place(x=670, y=300)



# register window

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
        image_label.config(image=None)
        image_label.image = None
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


register_window = tk.Toplevel(root)
register_window.title("Register Window")
screen_width1 = register_window.winfo_screenwidth()
screen_height1 = register_window.winfo_screenheight()
a = (screen_width1 - 800) // 2
b = (screen_height1 - 485) // 2
register_window.geometry(f"800x485+{a}+{b}")
register_window.resizable(False, False)
register_window.withdraw()  # Hide the second window initially

tk.Label(register_window, text="Employee Registration", fg="red", font=(None, 15)).place(x=290, y=5)

tk.Label(register_window, text="Employee ID", font=(None, 11)).place(x=10, y=40)
Label(register_window, text="Employee Name", font=(None, 11)).place(x=10, y=70)
Label(register_window, text="Mobile", font=(None, 11)).place(x=10, y=100)
Label(register_window, text="Email", font=(None, 11)).place(x=10, y=130)

Button(register_window, text="Upload Image", command=upload_image, font=(None, 11)).place(x=400, y=35)
image_label = Label(register_window, text="Image", font=(None, 11))
image_label.place(x=550, y=35)

e1 = Entry(register_window, font=(None, 11))
e1.place(x=140, y=40)

e2 = Entry(register_window, font=(None, 11))
e2.place(x=140, y=70)

e3 = Entry(register_window, font=(None, 11))
e3.place(x=140, y=100)

e4 = Entry(register_window, font=(None, 11))
e4.place(x=140, y=130)

Button(register_window, text="Add", command=Add, height=2, width=10, font=(None, 11)).place(x=10, y=180)
Button(register_window, text="update", command=update, height=2, width=10, font=(None, 11)).place(x=130, y=180)
Button(register_window, text="Delete", command=delete, height=2, width=10, font=(None, 11)).place(x=250, y=180)
Button(register_window, text="Back", command=show_main_window, height=2, width=10, font=(None, 11)).place(x=370,
                                                                                                          y=180)
Button(register_window, text="Exit", command=exit_application, height=2, width=10, font=(None, 11)).place(x=490,
                                                                                                          y=180)

cols = ('Id', 'Name', 'Mobile', 'Email')
listBox = ttk.Treeview(register_window, columns=cols, show='headings')

for col in cols:
    listBox.heading(col, text=col, )
    listBox.grid(row=1, column=0, columnspan=2)
    listBox.place(x=10, y=250)

show()
listBox.bind('<Double-Button-1>', GetValue)

root.mainloop()

video_capture.release()
cv2.destroyAllWindows()
