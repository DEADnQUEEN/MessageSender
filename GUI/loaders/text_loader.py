from GUI.loaders import fileview
from GUI import constants
from GUI.grid import text
from GUI.content import content


class TXTLoader(fileview.FileLoad, content.Base):
    def __init__(self):
        grid = text.TextView()
        super().__init__(
            grid,
            [("TXT файл", "*.txt")],
            [
                (constants.WIDGETS['Button'], {"text": "Настроить замену", "command": self.grid.view})
            ]
        )

    def get_name(self):
        return "Txt"

    def get_content(self):
        return self.columns

    def default_data(self):
        return self.preview_instance.text
