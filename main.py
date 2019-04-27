from tkinter import *
from CanvasManager import CanvasManager
import cProfile


def mesh_simulation():
    root = Tk()
    root.geometry("800x800")
    root.resizable(0,0)

    canvas = Canvas(root, width=800, height=800, bg='green')
    canvas.place(x=400, y=400,anchor=CENTER)
    CanvasManager(canvas, root)

    root.mainloop()



if __name__ == "__main__":
    mesh_simulation()