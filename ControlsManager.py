
from tkinter import *

class ControlsManager():
    def __init__(self, canvas, frame):
        self.canvas = canvas
        self.frame = frame

        self.bsize = 30
        self.bborder = 10
        self.button1 = Button(canvas, text='R', fg='black', command=self.b1_command)
        self.button2 = Button(canvas, text='S', fg='black', command=self.b2_command)
        self.button3 = Button(canvas, text='C', fg='black', command=self.b3_command)
        self.button4 = Button(canvas, text='?', fg='black', command=self.b4_command)
        
        self.button1.place(x=20, y = 50, width=self.bsize, height = self.bsize)
        self.button2.place(x=20, y = 50+1*(self.bsize+self.bborder), width=self.bsize, height = self.bsize)
        self.button3.place(x=20, y = 50+2*(self.bsize+self.bborder), width=self.bsize, height = self.bsize)
        self.button4.place(x=20, y = 50+3*(self.bsize+self.bborder), width=self.bsize, height = self.bsize)

        self.label1 = Label(canvas, text='Randomize mesh', fg='black', bg =self.canvas.config('bg')[4] ).place(x=20+self.bsize + self.bborder, y = 50, height = self.bsize)
        self.label2 = Label(canvas, text='Optimize router', fg='black', bg =self.canvas.config('bg')[4] ).place(x=20+self.bsize + self.bborder, y = 50+1*(self.bsize+self.bborder), height = self.bsize)
        self.label3 = Label(canvas, text='Clear mesh', fg='black', bg =self.canvas.config('bg')[4] ).place(x=20+self.bsize + self.bborder, y = 50+2*(self.bsize+self.bborder), height = self.bsize)
        self.label4 = Label(canvas, text='???', fg='black', bg =self.canvas.config('bg')[4] ).place(x=20+self.bsize + self.bborder, y = 50+3*(self.bsize+self.bborder), height = self.bsize)


        self.text = Text(canvas, height=22, width=45)
        self.text.place(x=20, y = 420)
        self.text.config(state = DISABLED)

    def b1_command(self):
        print('Undefined Button callback')

    def b2_command(self):
        print('Undefined Button callback')

    def b3_command(self):
        print('Undefined Button callback')

    def b4_command(self):
        print('Undefined Button callback')



     