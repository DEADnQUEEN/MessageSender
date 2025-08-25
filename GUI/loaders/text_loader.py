from GUI.loaders import fileview
from GUI import constants
from GUI.grid import text
from GUI.content import content


class TXTLoader(fileview.FileLoad, content.Base):
    def __init__(self):
        super().__init__(
            text.TextView(),
            [("TXT файл", "*.txt")],
            [
                (constants.WIDGETS['Button'], {"text": "Настроить замену", "command": self.grid.view})
            ]
        )

    def get_content(self):
        return self.preview_instance.text

    def get_variables(self):
        return self.columns
