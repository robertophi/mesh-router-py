
import numpy as np

nodes_settings = {'router': ['red', 30],
                  'basic_node': ['blue', 20]
                  }


class Node():
    def __init__(self, canvas, x, y, node_type='basic_node', node_power=50):
        assert node_type in nodes_settings.keys(), "Undefined type of node: {}".format(node_type)
        self.type = node_type
        self.canvas = canvas
        self.node_power = node_power
        self.color = nodes_settings[node_type][0]
        self.size = nodes_settings[node_type][1]

        # Number of nodes that connect to this node
        self.connected_nodes = 0

        # Distance from this node to the router
        self.connection_tier = 0

        self.ID = canvas.create_rectangle(x-self.size, y-self.size,
                                          x+self.size, y+self.size,
                                          outline='white', fill=self.color)
        self.txt = canvas.create_text(x, y-10, text="", fill='white')
        self.txt_power = canvas.create_text(x, y+10, text="", fill='white')

        x0, y0, x1, y1 = self.canvas.coords(self.ID)
        xc = int((x1+x0)/2)
        yc = int((y1+y0)/2)
        self.center = [xc, yc]

    def get_center(self):
        return self.center

    def move(self, dx, dy):
        # if (self.center[0]+dx) > 800 or (self.center[0]+dx) < 0:
        #    dx = 0
        # if (self.center[1]+dy) > 800 or (self.center[1]+dy) < 0:
        #    dy = 0
        self.canvas.move(self.ID, dx, dy)
        self.canvas.move(self.txt, dx, dy)
        self.canvas.move(self.txt_power, dx, dy)
        self.center = [self.center[0] + dx, self.center[1]+dy]

    def move_to(self, x, y):
        # x = np.clip(x, 0, 800) # Allow node to be outside the drawing zone (zoom in/out)
        # y = np.clip(y, 0, 800)
        [x0, y0] = self.center
        dx = x-x0
        dy = y-y0
        self.move(dx, dy)

    def update_txt(self):
        self.canvas.itemconfigure(self.txt, text=self.connection_tier)
        # self.canvas.itemconfigure(self.txt,text=self.ID)
        self.canvas.itemconfigure(
            self.txt_power, text="P:"+str(self.node_power))
