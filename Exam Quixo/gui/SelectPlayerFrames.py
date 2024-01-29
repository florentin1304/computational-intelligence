from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class MinmaxFrame(Frame):
    def __init__(self,parent):
        Frame.__init__(self, parent)
        self.parent = parent

        label = Label(self, text="Depth: ")
        label.grid(row=0, column=0)

        self.var_depth = StringVar(value=3)

        entry_depth = Entry(self, textvariable=self.var_depth)
        entry_depth.grid(row=0, column=1)

    def get_values(self):
        values = {}
        d_str = self.var_depth.get()
        if d_str.isnumeric() and int(d_str) > 0:
            values["depth"] = int(d_str)
        else:
            values["depth"] = None

        return values
    
class AlphaZeroFrame(Frame):
    def __init__(self,parent):
        Frame.__init__(self, parent)
        self.parent = parent

        label_n = Label(self, text="Search count: ")
        label_n.grid(row=0, column=0)
        self.var_n = StringVar(value=400)
        entry_n = Entry(self, textvariable=self.var_n)
        entry_n.grid(row=0, column=1)

        
        label_c = Label(self, text="C factor: ")
        label_c.grid(row=1, column=0)
        self.var_c = StringVar(value=2)
        entry_c = Entry(self, textvariable=self.var_c)
        entry_c.grid(row=1, column=1)

    def get_values(self):
        values = {}

        c_str = self.var_c.get()
        if c_str.isnumeric() and int(c_str) > 0:
            values["c"] = int(c_str)
        else:
            values["c"] = None

        n_str = self.var_n.get()
        if n_str.isnumeric() and int(n_str) > 0:
            values["num_searches"] = int(n_str)
        else:
            values["num_searches"] = None
        
        return values
