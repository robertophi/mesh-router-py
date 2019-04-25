from tkinter import *
from canvas_manager import CanvasManager
root = Tk()
root.geometry("500x500")
root.resizable(0,0)

    


canvas = Canvas(root, width=500, height=500, bg='green')
canvas.place(x=250, y=250,anchor=CENTER)

canvas_manager = CanvasManager(canvas, root)


root.mainloop()
