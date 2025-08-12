import tkinter as tk
from tkinter import filedialog
from typing import Optional

from GUI.loaders import base


class FileLoad(base.FileLoader):
    def setup_file_view(self, master: tk.Misc):
        scroll_x = tk.Scrollbar(master, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(master, orient=tk.VERTICAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.view_zone = tk.Text(
            master,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            wrap=tk.NONE,
        )
        self.view_zone.config(state=tk.DISABLED)
        self.view_zone.pack(expand=True, fill=tk.BOTH)

        self.show_in_file_zone()

    def show_in_file_zone(self):
        if self.filepath:
            with open(self.filepath, "r", encoding='utf-8') as f:
                text = ""
                for line in f.readlines():
                    text += line

            self.view_zone.config(state=tk.NORMAL)
            self.view_zone.delete('1.0', tk.END)
            self.view_zone.insert(tk.END, text)
            self.view_zone.config(state=tk.DISABLED)

    def open_file(self):
        if self.parent_view is None:
            raise ValueError("Parent View cannot be None")

        filepath = filedialog.askopenfilename(
            title="Загрузить файл",
            filetypes=self.file_types,
            parent=self.parent_view,
        )
        if filepath:
            self.filepath = filepath
            self.show_in_file_zone()

    def __init__(self, show_grid, file_types, widgets: Optional[list] = None):
        self.grid = show_grid
        super().__init__(
            file_types=file_types,
            additional_widgets=widgets
        )

    @property
    def columns(self):
        return self.grid.data

    def load_file(self):
        self.parent_view = self.load_ui()
        self.setup_file_view(self.view_frame)
        self.show_in_file_zone()
        self.parent_view.grab_set()
        self.parent_view.focus_set()
