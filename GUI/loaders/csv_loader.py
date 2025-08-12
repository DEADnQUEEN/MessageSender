import tkinter as tk

from GUI.loaders import fileview
from GUI import constants


class CSVLoader(fileview.FileLoad):
    @property
    def header_exists(self):
        return self.additional_widgets[1].value

    def __init__(self, grid):
        self.grid = grid
        super().__init__(
            grid,
            [("CSV файл", "*.csv")],
            [
                (constants.WIDGETS['Button'], {"text": "Настроить переменные", "command": self.grid.view}),
                (constants.WIDGETS['Checkbox'], {"text": "Начинать с 1 строки", "font": ("Arial", 10)})
            ]
        )

