from tkinter import *

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
        self.connected_lines = []
        self.connected_nodes = []




class CanvasManager():
    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root

        self.canvas.bind("<Button-1>", self.create_node)
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
        print("Click:",event.x, event.y)
        print("Create new router:")
        [x,y] = [event.x,event.y]      
        if self.check_click_intersection(x,y) == -1:
            new_router = Node(self.canvas, event, node_type='router')
            self.node_list.append(new_router)
        self.draw_all_lines()

    def create_node(self, event):
        print("Click:",event.x, event.y)
        print("Create new node:")
        [x,y] = [event.x,event.y]
        if self.check_click_intersection(x,y) == -1:
            new_node = Node(self.canvas, event, node_type='basic_node')
            self.node_list.append(new_node)
        self.draw_all_lines()

    def get_node_center(self, node):
        x0,y0, x1, y1 = self.canvas.coords(node.ID)
        xc = int((x1+x0)/2)
        yc = int((y1+y0)/2)
        return xc, yc
              
    def get_mesh_connection(self):
        vertices = []
        for node1 in self.node_list:
            xc1,yc1 = self.get_node_center(node1)
            min_dst2 = 10**10 # +Inf
            best_node2  = -1
            for node2 in self.node_list:
                if node1 != node2:
                    xc2,yc2 = self.get_node_center(node2)
                    distance = (xc2-xc1)**2 + (yc2-yc1)**2
                    if distance < min_dst2:
                        min_dst2 = distance
                        best_node2 = node2
            if best_node2 != -1:
                vertices.append([node1,best_node2])

        return vertices
    
    def get_mesh_connection_ALL(self):
        vertices = []
        for node1 in self.node_list:
            for node2 in self.node_list:
                vertices.append([node1,node2])

        return vertices

    def draw_all_lines(self):
        for line in self.line_list.copy():
            self.canvas.delete(line)
            self.line_list.remove(line)

        vertices = self.get_mesh_connection_ALL()
        for pair in vertices:
            node1, node2 = pair    
            xc1,yc1 = self.get_node_center(node1)
            xc2,yc2 = self.get_node_center(node2)
            line = self.canvas.create_line(xc1,yc1,xc2,yc2)
            self.line_list.append(line)
    
            
    def drag_node_canvas(self, event):
        [x,y] = [event.x,event.y]
        print(x,y)
        obj = self.check_click_intersection(x,y)
        if obj != -1:
            xc, yc = self.get_node_center(obj)
            self.canvas.move(obj.ID, -(xc-x),-(yc-y))
 
        self.draw_all_lines()        
        print([c.ID for c in self.node_list])


    
    def delete_node_canvas(self,event):
        print("Delete node:")
        [x,y] = [event.x,event.y]
        obj = self.check_click_intersection(x,y)
        if obj != -1:       
            self.canvas.delete(obj.ID)
            self.node_list.remove(obj)
        self.draw_all_lines()

    def delete_all_canvas(self, event):
        for node in self.node_list.copy():
            self.canvas.delete(node.ID)
            self.node_list.remove(node)
        self.draw_all_lines()



