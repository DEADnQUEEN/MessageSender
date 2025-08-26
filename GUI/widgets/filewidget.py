import tkinter as tk
from tkinter import filedialog
import os

class LoadFile(tk.Frame):
    @property
    def value(self):
        return self.file

    def load_file(self):
        filepath = filedialog.askopenfilename(
            title="Выберете фото",
            filetypes=self.filetypes,
            parent=self,
        )
        if filepath:
            self.file = filepath
            self.__load_label.config(text=os.path.basename(filepath))

    def __init__(self, master, filetypes, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.filetypes = filetypes
        self.file = None
        load_button = tk.Button(
            self,
            text="Загрузить шаблон",
            command=self.load_file
        )
        load_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.__load_label = tk.Label(self, text='')
        self.__load_label.pack(side=tk.LEFT, padx=10, pady=10)


