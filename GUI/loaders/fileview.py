from tkinter import filedialog
from typing import Optional

from GUI.loaders import base
from GUI.fileview import text_view


class FileLoad(base.FileLoader):
    def show_in_file_zone(self):
        if self.filepath:
            with open(self.filepath, "r", encoding='utf-8') as f:
                text = ""
                for line in f.readlines():
                    text += line
            if not isinstance(self.preview_instance, text_view.TextView):
                raise ValueError

            self.preview_instance.text = text

        super().show_in_file_zone()

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
            view_instance=text_view.TextView(),
            additional_widgets=widgets
        )
        if not isinstance(self.preview_instance, text_view.TextView):
            raise ValueError

        self.preview_instance: text_view.TextView = self.preview_instance

    @property
    def columns(self):
        return self.grid.data
