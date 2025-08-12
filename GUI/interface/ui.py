import tkinter as tk
from typing import Callable


from GUI.loaders.csv_loader import CSVLoader
from GUI.loaders.image_loader import ImageLoader
from GUI.jcon_decode import ui
from GUI import constants
from GUI.grid import grid


class UserView(ui.JSONEncodedUI):
    def parse_columns(self):
        self.columns = grid.GridFrame(
            **self.__grid_data
        ).data

    @property
    def csv_data(self):
        return self.csv_viewer.columns

    def __init__(
            self,
            root: tk.Tk,
            ui_json,
            *args,
            **kwargs
    ):
        self.csv_viewer = CSVLoader()
        self.img_loader = ImageLoader()

        commands: dict[str, Callable] = {
            "load_file": lambda *_, **__: self.csv_viewer.load_file,
            "load_IMG": lambda *_, **__: self.img_loader.load_file,
            "connect_templates": lambda *_, **__: self.parse_columns
        }

        self.__grid_data = {
            "save_json_path": r"C:\Users\aleks\PycharmProjects\WhatsAppBotNative\configs\files.json",
            "columns": {
                "variable":(
                    constants.WIDGETS['Entry'],
                    {
                        "placeholder": "Название"
                    }
                ),
                "file": (
                    constants.WIDGETS['File'],
                    {
                        "filetypes": [("PNG File", "*.png")]
                    }
                )
            }
        }
        self.columns = None

        super().__init__(root, ui_json, commands, *args, **kwargs)

        self.pack(anchor=tk.N)
