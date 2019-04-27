from tkinter import *
import numpy as np
from DijkstraSolver import Graph
from Node import Node
import time
import os
import types

class CanvasManager():
    def __init__(self, canvas, root, **kwargs):
        self.canvas = canvas
        self.root = root
        self.dijkstra_graph = Graph(0)

        self.canvas.bind("<Button-1>", self.create_node)
        self.canvas.bind("<Button-3>", self.delete_node_canvas)
        self.canvas.bind("<B1-Motion>", self.drag_node_canvas)
        self.canvas.bind("<Double-Button-3>", self.delete_all_canvas)
        self.canvas.bind("<Control-Button-1>", self.create_router)
        self.canvas.bind("<Shift-Button-1>", self.measure_distance)
        self.canvas.bind("<ButtonRelease-1>", self.release_canvas)
        self.canvas.bind_all("r", self.make_random_canvas)
        self.canvas.bind_all("d", self.measure_all_distances_from_node)
        self.canvas.bind_all("s", self.optimize_router_position)
        #self.canvas.bind_all("<space>", self.make_random_canvas)
        if os.name == 'nt': # Windows
            self.canvas.bind("<MouseWheel>", self.change_power_canvas)
        else:               #Linux
            self.canvas.bind("<Button-4>", self.change_power_canvas)
            self.canvas.bind("<Button-5>", self.change_power_canvas)

        self.line_list = []
        self.node_list = []
        self.txt_list = []
        self.last_moved_node = -1
        self.prev_measure_node = -1 
        self.last_measure_distance_time = time.time()


    def get_connections_list(self):
        if self.node_list == []:
            return []
        else:
            # Find source node (any router)
            source_node = -1
            for i,node in enumerate(self.node_list):
                if node.type == 'router':
                    source_node = i
            if source_node == -1:
                print("No router node in the current graph")
                for node in self.node_list:
                    node.connection_tier = 0
                return []
            else:
                # Apply dijkstra algorithm
                self.dijkstra_graph.node_list = self.node_list
                rx_connection_list = self.dijkstra_graph.dijkstra(source_node)                   
                return rx_connection_list

    def draw_current_canvas(self):
        # Delete all lines and text
        for line in self.line_list.copy():
            self.canvas.delete(line)
            self.line_list.remove(line)
        for txt in self.txt_list.copy():
            self.canvas.delete(txt)
            self.txt_list.remove(txt)

        # No nodes in graph or no router in graph
        if self.rx_connection_list == []:
            for node in self.node_list:
                node.update_txt()
            return 

        # Draw the new lines
        for i in range(len(self.node_list)):            
            node_child  = self.node_list[i]
            if node_child.type != 'router':
                node_parent = self.node_list[self.rx_connection_list[i]]
                xc1,yc1 = node_child.get_center()
                xc2,yc2 = node_parent.get_center()
                line = self.canvas.create_line(xc1,yc1,xc2,yc2)
                txt = self.canvas.create_text(int(xc1/2+xc2/2), int(yc1/2+yc2/2),
                                              text=str(round(self.dijkstra_graph.get_distance(node_tx=node_parent, node_rx=node_child),3))
                                              )
                self.line_list.append(line)
                self.txt_list.append(txt)
        
        # Update the info inside the nodes
        for node in self.node_list:
            node.update_txt()
        return            

    def update_canvas_complete(self):
        '''
        Update the current canvas (recalculate the graph, update the drawings)
        '''
        # Get the connection
        self.rx_connection_list = self.get_connections_list()
        self.draw_current_canvas()    
        
    
        
    def update_last_moved(self, event):
        '''
        Slowly drag the last activated node to the current cursor position
         - Solves the 'move mouse too fast' problem
        '''
        xc, yc = self.last_moved_node.get_center()  
        [x,y] = [event.x,event.y]
        deltax = int(-(xc-x))
        deltay = int(-(yc-y))
        
        self.last_moved_node.move(deltax, deltay)
        self.update_canvas_complete()


        
    def move_node(self, node, event):
        [x,y] = [event.x,event.y]
        xc, yc = node.get_center()
        node.move(-(xc-x),-(yc-y))
        self.last_moved_node = node    

    def delete_node(self, node):
        self.canvas.delete(node.ID)
        self.canvas.delete(node.txt)
        self.canvas.delete(node.txt_power)
        self.node_list.remove(node)

    def delete_line(self, line):
        self.canvas.delete(line)
        self.line_list.remove(line)

    ''' 
    Buttons callbacks
     - Button1 click         : add node
     - Button2 click         : remove node
     - Button2 double click  : remove all nodes
     - Ctrol + Button1 click : add router
     - Shift + Button1 click : measure distance between two nodes (shift click one, shift click another one)
     - Keyboard <r> press    : make random graph with 20 nodes
    '''
    def average_node_distance(self):
        ''' 
        Get the average distance from a node to a router
        '''
        distance_list = self.dijkstra_graph.rx_distance_list
        return np.mean(distance_list)

    def optimize_router_position(self, event):
        '''
        Callback for keyboard key 's'
        '''
        router = -1
        for node in self.node_list:
            if node.type == 'router':
                router = node
                continue
        if router == -1:
            return
        else:
            ## Optimize position
            ##### Move router to N random positions first, and first the best initial value
            last_average_dist = self.average_node_distance()
            dx = 10
            dy = 10
            alpha = 500
            for N in range(0,100):
                min_delta = int(1000/(N+4)**2 + 100/(N+3))
                # Check x-axis gradient
                router.move(10,0)
                self.update_canvas_complete()
                new_average_dist = self.average_node_distance()
                delta_f = new_average_dist- last_average_dist
                delta_fx = delta_f/dx
                # Update x-axis (go back -10 units, plus mx)
                mx = - alpha*delta_fx
                mx = np.sign(mx)*max(abs(mx),min_delta)
                router.move(-10+mx,0)
                self.update_canvas_complete()
                last_average_dist = self.average_node_distance()

                # Check y-axis gradient
                router.move(0,10)
                self.update_canvas_complete()
                new_average_dist = self.average_node_distance()
                delta_f = new_average_dist- last_average_dist
                delta_fy = delta_f/dy
                # Update y-axis (go back 10 units, plus my)
                my = - alpha*delta_fy
                my = np.sign(my)*max(abs(my),min_delta)
                router.move(0,-10+my)                
                self.update_canvas_complete()  
                last_average_dist = self.average_node_distance()
                print(last_average_dist)              

                if abs(alpha*delta_fy) < 0.1 and abs(alpha*delta_fx)<0.1 and N > 25:
                    self.canvas.update()
                    return
                self.canvas.update()
        




    def make_random_canvas(self, event):
        '''
        Callback for 'r' keyboard key press
        '''
        def make_random_fake_event():
            [x, y] = [np.random.randint(30,self.canvas.winfo_height()-30),
                      np.random.randint(30,self.canvas.winfo_width() -30)]
            fake_event = types.SimpleNamespace()
            fake_event.x = x
            fake_event.y = y
            return fake_event

        print('Random board...')
        self.delete_all_canvas(None)       
        self.create_router(make_random_fake_event())

        for n in range(0,20):
            tries = 0
            while(tries < 1000):
                tries += 1
                event = make_random_fake_event()
                if self.check_any_intersection(event.x,event.y) == -1:
                    self.create_node(event)
                    tries = 1000

    def change_power_canvas(self, event):
        '''
        Callback for mouse wheel
        '''
        obj = self.check_any_intersection(event.x,event.y)
        if obj != -1:
            if os.name == 'nt': # Windows
                if event.delta > 0:
                    obj.node_power += 5
                else:
                    obj.node_power = np.max([obj.node_power-5,0])

            else: # Linux
                if event.num == 4:
                    obj.node_power += 5
                elif event.num == 5:
                    obj.node_power = np.max([obj.node_power-5,0])
                obj.update_txt()
            self.update_canvas_complete()



    def drag_node_canvas(self, event):
        '''
        Callback for left mouse motion
        '''
        if (time.time()-self.last_measure_distance_time) < 1:
            return 
        else:
            [x,y] = [event.x,event.y]
            obj = self.check_any_intersection(x,y)
            if obj != -1:
                self.move_node(obj, event)
            else:
                self.move_node(self.last_moved_node, event)

        self.update_canvas_complete()  
        print(self.average_node_distance())

    def release_canvas(self, event):
        '''
        Callback for button1 release
        '''
        if (time.time()-self.last_measure_distance_time) < 1:
            return 
        else:
            self.update_canvas_complete()

    def delete_node_canvas(self,event):
        '''
        Callback for right click
        '''
        [x,y] = [event.x,event.y]
        obj = self.check_any_intersection(x,y)
        if obj != -1:       
            self.delete_node(obj)
        self.update_canvas_complete()
 

    def delete_all_canvas(self, event):
        '''
        Callback for double right click
        '''
        for node in self.node_list.copy():
            self.delete_node(node)
        for line in self.line_list.copy():
            self.delete_line(line)
        self.last_moved_node = -1
        self.prev_measure_node = -1
        self.update_canvas_complete()

    def intersect(self, node, x,y):
        '''
         Check if [x,y] is in node
        '''
        [x0,y0,x1,y1] = self.canvas.coords(node.ID)
        if x > x0 and x < x1 and y > y0 and y < y1:
            return True
        else:
            return False

    def check_any_intersection(self, x,y):
        '''
        Check if the mouse click intersects any node,
         - returns the first intersected node or -1 in case of false
        '''
        if self.node_list != []:
            for node in self.node_list:
                if self.intersect(node, x, y) == True:
                    return node
        return -1

    def measure_all_distances_from_node(self, event):
        [x,y] = [event.x,event.y]      
        clicked_node = self.check_any_intersection(x,y)
        if clicked_node == -1:
            return
        else:
            for target_node in self.node_list:
                xc1,yc1 = clicked_node.get_center()
                xc2,yc2 = target_node.get_center()
                line = self.canvas.create_line(xc1,yc1,xc2,yc2,dash=(5,5))
                txt = self.canvas.create_text(int(xc1/2+xc2/2), int(yc1/2+yc2/2),
                                              text=str(round(self.dijkstra_graph.get_distance(node_tx=clicked_node,node_rx= target_node),3)))
                self.line_list.append(line)
                self.txt_list.append(txt)

    def measure_distance(self, event):
        '''
        Callback for shift click
        '''
        [x,y] = [event.x,event.y]      
        clicked_node = self.check_any_intersection(x,y)
        if clicked_node != -1:
            if self.prev_measure_node == -1:
                self.prev_measure_node = clicked_node
            else:
                previous_node = self.prev_measure_node
                self.prev_measure_node = clicked_node

                xc1,yc1 = previous_node.get_center()
                xc2,yc2 = clicked_node.get_center()
                line = self.canvas.create_line(xc1,yc1,xc2,yc2,dash=(5,5))
                txt = self.canvas.create_text(int(xc1/2+xc2/2), int(yc1/2+yc2/2), 
                                              text=str(round(self.dijkstra_graph.get_distance(node_tx=clicked_node, node_rx=previous_node),3)))
                self.line_list.append(line)
                self.txt_list.append(txt)
                self.prev_measure_node = clicked_node
        self.last_measure_distance_time = time.time()

    def create_router(self, event):
        '''
        Callback for Ctrl + left mouse click
        '''
        [x,y] = [event.x,event.y]      
        if self.check_any_intersection(x,y) == -1:
            new_router = Node(self.canvas, event, node_type='router')
            self.node_list.append(new_router)
            self.last_moved_node = new_router

        self.update_canvas_complete()

    def create_node(self, event):
        '''
        Callback for left mouse click
        '''
        [x,y] = [event.x,event.y]
        if self.check_any_intersection(x,y) == -1:
            new_node = Node(self.canvas, event, node_type='basic_node')
            self.node_list.append(new_node)
            self.last_moved_node = new_node
        self.update_canvas_complete()
