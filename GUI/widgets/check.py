import tkinter as tk


class CheckButton(tk.Checkbutton):
    def __init__(self, master, value: bool = False, **kwargs):
        self.value = tk.BooleanVar(value=value)
        super().__init__(master, variable=self.value, **kwargs)
