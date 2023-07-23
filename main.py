from tkinter import *

root = Tk()
root.title("Face Recognition System")
root.geometry("800x485+300+200")
root.resizable(False, False)

frame_label = Label(root)
frame_label.place(x=2, y=2)


Button(root, text="Present", height=2, width=10, font=(None, 11)).place(x=670, y=100)
Button(root, text="Add new", height=2, width=10, font=(None, 11)).place(x=670, y=200)
Button(root, text="Exit", height=2, width=10, font=(None, 11)).place(x=670, y=300)

root.mainloop()