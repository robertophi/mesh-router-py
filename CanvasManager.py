from tkinter import *
import numpy as np
from DijkstraSolver import Graph
from Node import Node
import time

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
                return []
            else:
                # Apply dijkstra algorithm
                self.dijkstra_graph.node_list = self.node_list
                rx_connection_list = self.dijkstra_graph.dijkstra(source_node)                   
                return rx_connection_list




    def draw_connections(self):
        '''
        Draw all the nodes connections in the graph
        '''

        # Get the connection
        rx_connection_list = self.get_connections_list()
            
        for line in self.line_list.copy():
            self.canvas.delete(line)
            self.line_list.remove(line)
        for txt in self.txt_list.copy():
            self.canvas.delete(txt)
            self.txt_list.remove(txt)

        # No nodes in graph or no router in graph
        if rx_connection_list == []:
            return

        for i in range(len(self.node_list)):            
            node_child  = self.node_list[i]
            if node_child.type != 'router':
                node_parent = self.node_list[rx_connection_list[i]]
                xc1,yc1 = node_child.get_center()
                xc2,yc2 = node_parent.get_center()
                line = self.canvas.create_line(xc1,yc1,xc2,yc2)
                txt = self.canvas.create_text(int(xc1/2+xc2/2), int(yc1/2+yc2/2),
                                              text=str(round(self.dijkstra_graph.get_distance(node_child, node_parent),3))
                                              )
                self.line_list.append(line)
                self.txt_list.append(txt)
        for node in self.node_list:
            node.update_txt()
        return            
    
        
    def update_last_moved(self, event):
        '''
        Slowly drag the last activated node to the current cursor position
         - Solves the 'move mouse too fast' problem
        '''
        xc, yc = self.last_moved_node.get_center()  
        [x,y] = [event.x,event.y]

        N = 20
        t = 0.1
        deltax = int(-(xc-x)/N)
        deltay = int(-(yc-y)/N)
        for _ in range(0,N):
            self.last_moved_node.move(deltax, deltay)
            self.canvas.update()
            time.sleep(t/N)

        
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
    '''

    def change_power_canvas(self, event):
        '''
        Callback for mouse wheel
        '''
        obj = self.check_click_intersection(event.x,event.y)
        if obj != -1:
            if event.num == 4:
                obj.node_power += 2
            elif event.num == 5:
                obj.node_power -= 2
            obj.update_txt()
            self.draw_connections()



    def drag_node_canvas(self, event):
        '''
        Callback for left mouse motion
        '''
        if (time.time()-self.last_measure_distance_time) < 1:
            return 
        else:
            [x,y] = [event.x,event.y]
            obj = self.check_click_intersection(x,y)
            if obj != -1:
                self.move_node(obj, event)
            else:
                self.move_node(self.last_moved_node, event)
            
            
            if len(self.node_list)<20:
                self.draw_connections()        

    def release_canvas(self, event):
        '''
        Callback for button1 release
        '''
        if len(self.node_list) >= 20:
            self.draw_connections()

    def delete_node_canvas(self,event):
        '''
        Callback for right click
        '''
        [x,y] = [event.x,event.y]
        obj = self.check_click_intersection(x,y)
        if obj != -1:       
            self.delete_node(obj)
        self.draw_connections()

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
        self.draw_connections()

    def intersect(self, node, x,y):
        '''
         Check if [x,y] is in node
        '''
        [x0,y0,x1,y1] = self.canvas.coords(node.ID)
        if x > x0 and x < x1 and y > y0 and y < y1:
            return True
        else:
            return False


        
    def check_click_intersection(self, x,y):
        '''
        Check if the mouse click intersects any node,
         - returns the first intersected node or -1 in case of false
        '''
        if self.node_list != []:
            for node in self.node_list:
                if self.intersect(node, x, y) == True:
                    return node
        return -1

    def measure_distance(self, event):
        '''
        Callback for shift click
        '''
        [x,y] = [event.x,event.y]      
        clicked_node = self.check_click_intersection(x,y)
        if clicked_node != -1:
            if self.prev_measure_node == -1:
                self.prev_measure_node = clicked_node
            else:
                previous_node = self.prev_measure_node
                self.prev_measure_node = clicked_node

                xc1,yc1 = previous_node.get_center()
                xc2,yc2 = clicked_node.get_center()
                line = self.canvas.create_line(xc1,yc1,xc2,yc2,dash=(5,5))
                txt = self.canvas.create_text(int(xc1/2+xc2/2), int(yc1/2+yc2/2), text=str(round(self.dijkstra_graph.get_distance(clicked_node, previous_node),3)))
                self.line_list.append(line)
                self.txt_list.append(txt)
                self.prev_measure_node = clicked_node
        self.last_measure_distance_time = time.time()

    def create_router(self, event):
        '''
        Callback for Ctrl + left mouse click
        '''
        [x,y] = [event.x,event.y]      
        if self.check_click_intersection(x,y) == -1:
            new_router = Node(self.canvas, event, node_type='router')
            self.node_list.append(new_router)
            self.last_moved_node = new_router

        self.draw_connections()

    def create_node(self, event):
        '''
        Callback for left mouse click
        '''
        [x,y] = [event.x,event.y]
        if self.check_click_intersection(x,y) == -1:
            new_node = Node(self.canvas, event, node_type='basic_node')
            self.node_list.append(new_node)
            self.last_moved_node = new_node
        self.draw_connections()
