from tkinter import *
root = Tk()
#root.state('normal')
#root.configure(bg = 'green4')
    


class Node():
    def __init__(self, root, event):
        self.node = Canvas(root, width=74, height=97, bg='blue')
        self.node.place(x=event.x_root-50, y=event.y_root-20,anchor=CENTER)
        return



class NodeManager():
    def __init__(self, root):
        self.node_list = []
        self.root = root

    def add(self, node):
        self.node_list.append(node)

    def drag_node(self, event):
        event.widget.place(x=event.x_root-50, y=event.y_root-20,anchor=CENTER)
        print(event.x_root, event.y_root)

    def delete_node(self, event):
        canvas = event.widget
        canvas.destroy()
        print('Deleted canvas?')

    def root_click(self, event):
        print('canvas clicked')
        node = Node(self.root, event)
        node.node.bind("<B1-Motion>", self.drag_node)
        node.node.bind("<Control-Button-1>", self.delete_node)
        self.node_list.append(node)







node_manager = NodeManager(root=root)
frame = Frame(root, width = 500, height = 500)
frame.pack()
frame.bind("<Button-1>", node_manager.root_click)
frame.mainloop()