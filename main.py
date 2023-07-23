from tkinter import *
import cv2
import face_recognition as fr
from PIL import Image, ImageTk
import numpy as np
import pyttsx3
import pymysql

from register import create_registration_window


def register():
    root.destroy()  # Close the main window
    create_registration_window()


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


root = Tk()
root.title("Face Recognition System")

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
Button(root, text="Add new", command=register, height=2, width=10, font=(None, 11)).place(x=670, y=200)
Button(root, text="Exit", command=exit_application, height=2, width=10, font=(None, 11)).place(x=670, y=300)

root.mainloop()

video_capture.release()
cv2.destroyAllWindows()
