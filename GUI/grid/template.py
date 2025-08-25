from GUI import constants
from GUI.grid import grid

from typing import Callable
import tkinter as tk


class TemplateGrid(grid.GridFrame):
    def save(self, commit: bool = True):
        save = {
            "value": self.__variable_combobox.value,
            "templates": super().save(False)
        }

        self.drop(save)
        return save


    def __init__(
            self,
            master,
            add_button_text: str,
            columns: dict[str, (tk.Widget, dict[str, any])],
            data_drop: Callable,
            variables: list[str],
            *args,
            **kwargs
    ):
        super().__init__(master, add_button_text, columns, data_drop, *args, **kwargs)
        self.__variable_combobox = constants.WIDGETS['Combobox'](
            self.top_frame,
            values=variables,
            state="readonly",
        )
        self.__variable_combobox.pack(side=tk.RIGHT, fill=tk.X)
        self.top_frame.update()


class TemplateView(grid.GridViewer):
    def paste_variables(self, variables):
        self.kwargs['variables'] = variables

    def __init__(self):
        super().__init__(TemplateGrid)
        self.save_path = r"C:\Users\aleks\PycharmProjects\WhatsAppBotNative\configs\conf.json"
        self.add_button_text="Добавить шаблон"
        self.columns = {
            "variable":(
                constants.WIDGETS['Entry'],
                {
                    "placeholder": "Название шаблона"
                }
            ),
            "file": (
                constants.WIDGETS['File'],
                {
                    "filetypes": [("PNG File", "*.png")]
                }
            )
        }
