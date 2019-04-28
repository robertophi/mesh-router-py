



from tkinter import *

class WindowManager():

    def __init__(self, root, frame, mesh_manager, controls_manager):
        self.root = root
        self.frame = frame
        self.mesh_manager = mesh_manager
        self.controls_manager = controls_manager

        self.setup_controls()
        self.setup_mesh()

        print("Window manager activated . . . ")
    
    def setup_controls(self):
        self.controls_manager.button1.config(command=self.mesh_manager.make_random_canvas_callback)
        self.controls_manager.button2.config(command=self.mesh_manager.optimize_router_position)
        self.controls_manager.button3.config(command=self.mesh_manager.clear_canvas_callback)


    def overloaded_average_node_distance(self):
        avg_dist = self.mesh_manager.router_optimizer.get_average_node_distance()
        self.controls_manager.text.config(state = NORMAL)
        self.controls_manager.text.insert(END, str(avg_dist)+'\n')
        self.controls_manager.text.see("end")
        self.controls_manager.text.config(state = DISABLED)
        return avg_dist

    def setup_mesh(self):
        # Replace the function call for 'optimizer' in order to display the avg_distance on the txt widget
        self.mesh_manager.router_optimizer.average_node_distance = self.overloaded_average_node_distance