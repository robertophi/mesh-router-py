nodes_settings = {'router'     : ['red',30],
                  'basic_node' : ['blue',20]
                 }
 
class Node():
    def __init__(self, canvas, event, node_type='basic_node'):
        assert node_type in nodes_settings.keys(), "Undefined type of node: {}".format(node_type)
        self.type = node_type
        self.canvas = canvas

        color = nodes_settings[node_type][0]
        size  = nodes_settings[node_type][1]
        self.ID = canvas.create_rectangle(event.x-size, event.y-size,
                                    event.x+size, event.y+size,
                                    outline='white', fill=color)
        self.txt = canvas.create_text(event.x, event.y, text=str(self.ID))

    def get_center(self):
        x0,y0, x1, y1 = self.canvas.coords(self.ID)
        xc = int((x1+x0)/2)
        yc = int((y1+y0)/2)
        return xc, yc