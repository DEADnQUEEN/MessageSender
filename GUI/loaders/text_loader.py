from GUI.loaders import fileview
from GUI import constants


class TXTLoader(fileview.FileLoad):
    def __init__(self, grid):
        self.grid = grid
        super().__init__(
            grid,
            [("TXT файл", "*.txt")],
            [
                (constants.WIDGETS['Button'], {"text": "Настроить замену", "command": self.grid.view})
            ]
        )

