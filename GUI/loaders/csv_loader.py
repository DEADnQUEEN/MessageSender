from GUI.loaders import fileview
from GUI import constants


class CSVLoader(fileview.FileLoad):
    def __init__(self, grid):
        self.grid = grid
        super().__init__(
            grid,
            [("CSV файл", "*.csv")],
            [
                (constants.WIDGETS['Button'], {"text": "Настроить переменные", "command": self.grid.view})
            ]
        )

