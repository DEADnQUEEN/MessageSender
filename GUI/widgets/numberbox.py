import tkinter as tk

class NumberBox(tk.Spinbox):
    @property
    def value(self):
        return int(self.get())

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)