from tkinter import *

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.hi_there = Button(frame, text="Hola", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print("hola todo el mundo!")

root = Tk()
root.title("Ventana de pruebas")
#root.resizable(True, False)
#root.iconbitmap("favicon.ico")
#root.geometry("650x350") # tamaño
root.config(bg="blue")

frame=Frame()
frame.pack()
frame.config(width="650", height="350", bg="red")
frame.config(bd=5)
frame.config(relief="groove")
frame.pack(fill="both", expand="True")
#app = App(root)
root.mainloop()
