from Node import Node


class CanvasBase():

    def __init__(self, canvas, frame, **kwargs):
        self.canvas = canvas
        self.frame = frame
        self.line_list = []
        self.node_list = []
        self.txt_list = []
        self.last_moved_node = -1

    def create_node(self, x, y):
        if self.check_any_intersection(x, y) == -1:
            new_node = Node(self.canvas, x, y, node_type='basic_node')
            self.node_list.append(new_node)
            self.last_moved_node = new_node

    def create_router(self, x, y):
        if self.check_any_intersection(x, y) == -1:
            new_router = Node(self.canvas, x, y, node_type='router')
            self.node_list.append(new_router)
            self.last_moved_node = new_router

    def delete_node(self, node):
        self.canvas.delete(node.ID)
        self.canvas.delete(node.txt)
        self.canvas.delete(node.txt_power)
        self.node_list.remove(node)

    def delete_line(self, line):
        self.canvas.delete(line)
        self.line_list.remove(line)

    def move_node(self, node, event):
        [x, y] = [event.x, event.y]
        xc, yc = node.get_center()
        node.move(-(xc-x), -(yc-y))
        self.last_moved_node = node

    def intersect(self, node, x, y):
        [x0, y0, x1, y1] = self.canvas.coords(node.ID)
        if x > x0 and x < x1 and y > y0 and y < y1:
            return True
        else:
            return False

    def check_any_intersection(self, x, y):
        if self.node_list != []:
            for node in self.node_list:
                if self.intersect(node, x, y) == True:
                    return node
        return -1
