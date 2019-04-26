from tkinter import *
from solve_dijkstra import Graph
import numpy as np

nodes_settings = {'router'     : ['red',30],
                  'basic_node' : ['blue',20]
                 }
 
class Node():
    def __init__(self, canvas, event, node_type='simple_node'):
        self.type = node_type
        try:
            color = nodes_settings[node_type][0]
            size  = nodes_settings[node_type][1]
        except:
            print('Node typer not correctly defined')
            color = 'black'
            

        self.ID = canvas.create_rectangle(event.x-size, event.y-size,
                                    event.x+size, event.y+size,
                                    outline='white', fill=color)

        self.txt = canvas.create_text(event.x, event.y,
                                    text=str(self.ID))
        self.connected_lines = []
        self.connected_nodes = []




class CanvasManager():
    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root
        self.dijkstra_graph = Graph(0)

        self.canvas.bind("<Button-1>", self.create_node)
        self.canvas.bind("<Button-2>", self.get_connections_list)
        self.canvas.bind("<Button-3>", self.delete_node_canvas)
        self.canvas.bind("<B1-Motion>", self.drag_node_canvas)
        self.canvas.bind("<Double-Button-3>", self.delete_all_canvas)
        self.canvas.bind("<Control-Button-1>", self.create_router)
        self.line_list = []
        self.node_list = []

    def intersect(self, node, x,y):
        print("intersection:")
        print(node)
        [x0,y0,x1,y1] = self.canvas.coords(node.ID)
        if x > x0 and x < x1 and y > y0 and y < y1:
            print('intersection')
            return True
        else:
            print('no intersection')
            return False

    def check_click_intersection(self, x,y):
        if self.node_list != []:
            for node in self.node_list:
                if self.intersect(node, x, y) == True:
                    return node
        return -1

    def create_router(self, event):
        '''
        Callback for Ctrl + left mouse click
        '''
        print("Click:",event.x, event.y)
        print("Create new router:")
        [x,y] = [event.x,event.y]      
        if self.check_click_intersection(x,y) == -1:
            new_router = Node(self.canvas, event, node_type='router')
            self.node_list.append(new_router)
        self.draw_connections()

    def create_node(self, event):
        '''
        Callback for left mouse click
        '''
        print("Click:",event.x, event.y)
        print("Create new node:")
        [x,y] = [event.x,event.y]
        if self.check_click_intersection(x,y) == -1:
            new_node = Node(self.canvas, event, node_type='basic_node')
            self.node_list.append(new_node)
        self.draw_connections()

    def get_node_center(self, node):
        x0,y0, x1, y1 = self.canvas.coords(node.ID)
        xc = int((x1+x0)/2)
        yc = int((y1+y0)/2)
        return xc, yc
              
    
    
    

    def get_mesh_connection_matrix(self):
        n = len(self.node_list)
        dist_matrix = np.zeros((n,n))
        for i,node1 in enumerate(self.node_list):
            xc1,yc1 = self.get_node_center(node1)
            for j,node2 in enumerate(self.node_list):                
                xc2,yc2 = self.get_node_center(node2)
                distance = (xc2-xc1)**2 + (yc2-yc1)**2
                dist_matrix[i,j] = distance  
        #return dist_matrix

        m_base = np.ones((n+1,n+1))*1000000000
        m_base[1:,1:] = dist_matrix
        for i in range(len(self.node_list)):
            if self.node_list[i].type == 'router':
                m_base[0,i+1] = 0.1
                m_base[i+1,0] = 0.1
        m_base[0,0] = 0
        print(np.round(m_base,3))
        return m_base


        
        
    def get_connections_list(self):
        dist_matrix = self.get_mesh_connection_matrix()
        self.dijkstra_graph.V = dist_matrix.shape[0]
        self.dijkstra_graph.graph = dist_matrix

        rx_connection_list = self.dijkstra_graph.dijkstra(0)
        rx_connection_list = rx_connection_list[1:]
        rx_connection_list = [c-1 for c in rx_connection_list]
        return rx_connection_list


    def draw_connections(self):
        rx_connection_list = self.get_connections_list()

        for line in self.line_list.copy():
            self.canvas.delete(line)
            self.line_list.remove(line)
        
        for i in range(len(self.node_list)):            
            #i = i-1
            node_child  = self.node_list[i]
            if node_child.type != 'router':
                node_parent = self.node_list[rx_connection_list[i]]
                xc1,yc1 = self.get_node_center(node_child)
                xc2,yc2 = self.get_node_center(node_parent)
                line = self.canvas.create_line(xc1,yc1,xc2,yc2)
                self.line_list.append(line)


            
    def move_node(self, obj, event):
        [x,y] = [event.x,event.y]
        xc, yc = self.get_node_center(obj)
        self.canvas.move(obj.ID, -(xc-x),-(yc-y))
        self.canvas.move(obj.txt, -(xc-x),-(yc-y))
        

    def drag_node_canvas(self, event):
        '''
        Callback for left mouse motion
        '''
        [x,y] = [event.x,event.y]
        print(x,y)
        obj = self.check_click_intersection(x,y)
        if obj != -1:
            self.move_node(obj, event)

 
        self.draw_connections()        
        print([c.ID for c in self.node_list])


    def delete_node(self, node):
        self.canvas.delete(node.ID)
        self.canvas.delete(node.txt)
        self.node_list.remove(node)
        
    def delete_node_canvas(self,event):
        '''
        Callback for right click
        '''
        print("Delete node:")
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
        self.draw_connections()
