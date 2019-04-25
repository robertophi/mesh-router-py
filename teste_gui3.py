from tkinter import *
from CanvasManager import CanvasManager
root = Tk()
root.geometry("800x800")
root.resizable(0,0)

    


canvas = Canvas(root, width=800, height=800, bg='green')
canvas.place(x=400, y=400,anchor=CENTER)
canvas_manager = CanvasManager(canvas, root)


root.mainloop()
