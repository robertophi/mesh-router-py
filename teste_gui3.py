from tkinter import *
root = Tk()
root.geometry("700x700")
root.resizable(0,0)
#root.state('normal')
#root.configure(bg = 'green4')
    

node_list = []
def click(event):
    print("Create node")
    global node_list
    new_w = canvas.create_rectangle(event.x-10, event.y-10,
                                event.x+10, event.y+10,
                                outline='white', fill='blue')
    node_list.append(new_w)                                
    print(event.x, event.y)


def intersect(node, x,y):
    [x0,y0,x1,y1] = canvas.coords(node)
    if x > x0 and x < x1 and y > y0 and y < y1:
        print('intersection')
        return True
    else:
        print('no intersection')
        return False
    

def delete(event):
    print("Delete node:")
    global node_list
    [x,y] = [event.x,event.y]
    for node in node_list.copy():
        if intersect(node, x,y) == True:
            canvas.delete(node)
            node_list.remove(node)
    canvas.update()


canvas = Canvas(root, width=500, height=500, bg='green')
canvas.place(x=250, y=250,anchor=CENTER)

w = canvas.create_rectangle(100,100,20,20,outline='white', fill='red')
canvas.move(w, 20,20)
canvas.bind("<Button-1>", click)
canvas.bind("<Button-3>", delete)
root.mainloop()