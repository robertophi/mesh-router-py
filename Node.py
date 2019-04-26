nodes_settings = {'router'     : ['red',30],
                  'basic_node' : ['blue',20]
                 }
 
class Node():
    def __init__(self, canvas, event, node_type='basic_node', node_power=50):
        assert node_type in nodes_settings.keys(), "Undefined type of node: {}".format(node_type)
        self.type = node_type
        self.canvas = canvas
        self.node_power = node_power
        self.color = nodes_settings[node_type][0]
        self.size  = nodes_settings[node_type][1]

        # Number of nodes that connect to this node
        self.connected_nodes = 0

        # Distance from this node to the router
        self.connection_tier = 0

        self.ID = canvas.create_rectangle(event.x-self.size, event.y-self.size,
                                    event.x+self.size, event.y+self.size,
                                    outline='white', fill=self.color)
        self.txt = canvas.create_text(event.x, event.y-10, text=str(self.connection_tier), fill='white')        
        self.txt_power = canvas.create_text(event.x, event.y+10, text="P:"+str(self.node_power), fill='white')


    def get_center(self):
        x0,y0, x1, y1 = self.canvas.coords(self.ID)
        xc = int((x1+x0)/2)
        yc = int((y1+y0)/2)
        return xc, yc

    def move(self, dx, dy):
        self.canvas.move(self.ID, dx,dy)
        self.canvas.move(self.txt, dx, dy)
        self.canvas.move(self.txt_power, dx, dy)
    
    def update_txt(self):
        self.canvas.itemconfigure(self.txt,text=self.connection_tier)
        self.canvas.itemconfigure(self.txt_power,text=self.node_power)
