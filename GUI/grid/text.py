from GUI import constants
from GUI.grid import grid

from typing import Callable
import tkinter as tk


class TextGrid(grid.GridFrame):
    def __init__(
            self,
            master,
            add_button_text: str,
            columns: dict[str, (tk.Widget, dict[str, any])],
            data_drop: Callable,
            *args,
            **kwargs
    ):
        super().__init__(master, add_button_text, columns, data_drop, *args, **kwargs)

class TextView(grid.GridViewer):
    def paste_variables(self, variables):
        for key, column in self.columns.items():
            widget, args = column
            if widget is constants.WIDGETS['Combobox']:
                args['values'] = variables

    def __init__(self):
        super().__init__(TextGrid)
        self.add_button_text="Добавить заменяемое"
        self.columns = {
            "from":(
                constants.WIDGETS['Entry'],
                {
                    "placeholder": "Заменить выражение"
                }
            ),
            "variable":(
                constants.WIDGETS['Combobox'],
                {
                    'state': 'readonly',
                }
            ),
        }
