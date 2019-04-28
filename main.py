from tkinter import *
from MeshManager import MeshManager
from ControlsManager import ControlsManager
from WindowManager import WindowManager
import cProfile


def mesh_simulation():
    root = Tk()
    root.geometry("1200x800")
    root.resizable(0,0)
    root.title('Mesh-routing Simulation')

    frame = Frame(root)
    frame.pack(side=LEFT, fill = BOTH, expand=True, padx=5, pady = 5)



    # Create the right side of the window - Controls Canvas
    canvas_controls = Canvas(frame, width = 400, height = 800)
    controls_manager = ControlsManager(canvas_controls, frame)
    canvas_controls.pack(side=RIGHT, expand=True)
    
    # Create the left side of the window - Mesh Canvas    
    canvas_mesh = Canvas(frame, width=800, height=800, bg='green')
    canvas_mesh.pack(side=LEFT, fill=NONE , expand=True)
    mesh_manager = MeshManager(canvas_mesh, frame)
    
    # Connect the canvases with a single manager
    window_manager = WindowManager(root, frame, mesh_manager, controls_manager)




    # Create the menu toolbar (top of screen)
    ''' Main menu '''
    menu_bar = Menu(root)
    ''' First menu item'''
    menu_bar.add_command(label='Randomize', command=mesh_manager.make_random_canvas_callback)
    ''' Second menu item'''
    menu_bar.add_command(label='Optimize',command=mesh_manager.optimize_router_position)
    ''' Third menu item - drop down menu '''
    file = Menu(menu_bar)
    file.add_command(label='Exit')
    menu_bar.add_cascade(label="File", menu=file)
    ''' Config root to use this menu'''
    root.config(menu=menu_bar)

    root.mainloop()

if __name__ == "__main__":
    mesh_simulation()