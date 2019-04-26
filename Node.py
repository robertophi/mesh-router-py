nodes_settings = {'router'     : ['red',30],
                  'basic_node' : ['blue',20]
                 }
 
class Node():
    def __init__(self, canvas, event, node_type='basic_node'):
        assert node_type in nodes_settings.keys(), "Undefined type of node: {}".format(node_type)
        self.type = node_type
        self.canvas = canvas

        self.color = nodes_settings[node_type][0]
        self.size  = nodes_settings[node_type][1]

        # Number of nodes that connect to this node
        self.connected_nodes = 0

        # Distance from this node to the router
        self.connection_tier = 0

        self.ID = canvas.create_rectangle(event.x-self.size, event.y-self.size,
                                    event.x+self.size, event.y+self.size,
                                    outline='white', fill=self.color)
        self.txt = canvas.create_text(event.x, event.y, text=str(self.connection_tier), fill='white')
        

    def get_center(self):
        x0,y0, x1, y1 = self.canvas.coords(self.ID)
        xc = int((x1+x0)/2)
        yc = int((y1+y0)/2)
        return xc, yc