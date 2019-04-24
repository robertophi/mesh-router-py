from tkinter import *
root = Tk()
root.geometry("700x700")
root.resizable(0,0)
#root.state('normal')
#root.configure(bg = 'green4')
    

class Node():
    def __init__(self, canvas, event):
        self.node = canvas.create_rectangle(event.x-20, event.y-20,
                                    event.x+20, event.y+20,
                                    outline='white', fill='blue')
        self.connected_lines = []
        self.connected_nodes = []


def intersect(node, x,y):
    [x0,y0,x1,y1] = canvas.coords(node.node)
    if x > x0 and x < x1 and y > y0 and y < y1:
        print('intersection')
        return True
    else:
        print('no intersection')
        return False



line_list = []
node_list = []
def click(event):
    print("Click:",event.x, event.y)

    print("Create node")
    global node_list
    [x,y] = [event.x,event.y]
    intersect_flag = False
    for node in node_list.copy():
        if intersect(node, x,y) == True:
            intersect_flag = True
            continue
    if intersect_flag == False:
        new_w = Node(canvas, event)
        node_list.append(new_w)                                
    draw_lines()

def draw_lines():
    global node_list, line_list
    for line in line_list.copy():
        canvas.delete(line)
        line_list.remove(line)

    for node1 in node_list:
        for node2 in node_list[0:1]:
            x0,y0, x1, y1 = canvas.coords(node1.node)
            xs_A = int((x1+x0)/2)
            ys_A = int((y1+y0)/2)
            x3,y3, x4, y4 = canvas.coords(node2.node)
            xs_B = int((x3+x4)/2)
            ys_B = int((y3+y4)/2)
            line = canvas.create_line(xs_A,ys_A,xs_B,ys_B)
            line_list.append(line)
            node1.connected_lines.append(line)
            node2.connected_lines.append(line)
            
def draw_connected_lines(node):
    global node_list, line_list
    for line in node.connected_lines:
        canvas.delete(line)
        #line_list.remove(line)

    node1 = node
    for node2 in node_list[0:1]:
        x0,y0, x1, y1 = canvas.coords(node1.node)
        xs_A = int((x1+x0)/2)
        ys_A = int((y1+y0)/2)
        x3,y3, x4, y4 = canvas.coords(node2.node)
        xs_B = int((x3+x4)/2)
        ys_B = int((y3+y4)/2)
        line = canvas.create_line(xs_A,ys_A,xs_B,ys_B)
        line_list.append(line)
        node1.connected_lines.append(line)
    canvas.update()
def drag(event):
    global node_list
    [x,y] = [event.x,event.y]
    print(x,y)

    for node in node_list.copy():
        if intersect(node, x,y) == True:
            [x0,y0,x1,y1] = canvas.coords(node.node)
            xs = int((x0+x1)/2)
            ys = int((y0+y1)/2)
            canvas.move(node.node, -(xs-x),-(ys-y))
            draw_connected_lines(node)

    
    print([c.node for c in node_list])


    

def delete(event):
    print("Delete node:")
    global node_list
    [x,y] = [event.x,event.y]
    for node in node_list.copy():
        if intersect(node, x,y) == True:
            canvas.delete(node.node)
            node_list.remove(node)
    draw_lines()

def delete_all(event):
    global node_list
    for node in node_list.copy():
        canvas.delete(node.node)
        node_list.remove(node)
    draw_lines()


canvas = Canvas(root, width=500, height=500, bg='green')
canvas.place(x=250, y=250,anchor=CENTER)

w = canvas.create_rectangle(100,100,20,20,outline='white', fill='red')
canvas.move(w, 20,20)
canvas.bind("<Button-1>", click)
canvas.bind("<Button-3>", delete)
canvas.bind("<B1-Motion>", drag)
canvas.bind("<Double-Button-3>", delete_all)
root.mainloop()