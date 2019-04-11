from tkinter import *

root=Tk()

frame=Frame(root, width=500, height=400)
frame.pack()

Label(frame, text="Hola mundo", font=("Comic Sans MS", 18)).place(x=50, y=50)

root.mainloop()