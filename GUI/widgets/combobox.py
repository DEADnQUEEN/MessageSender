from tkinter import ttk
from tkinter import StringVar

class PredefinedCmb(ttk.Combobox):
    @property
    def value(self):
        return self.__value.get()

    @property
    def variable(self) -> StringVar:
        return self.__value

    def __init__(self, master, *args, **kwargs):
        self.__value = StringVar(master=master, value=kwargs['values'][0] if 'values' in kwargs else "")
        kwargs['textvariable'] = self.__value
        super().__init__(master, *args, **kwargs)
