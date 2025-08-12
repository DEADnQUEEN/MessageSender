from GUI import constants
from GUI.grid import grid


class CSVData(grid.GridViewer):
    def __init__(self):
        add_button_text = "Добавить значение"
        columns = {
            "column": (
                constants.WIDGETS['Number'],
                {
                    'from_': 1.0,
                    'to': 100000,
                    "validate": "key"
                }
            ),
            "variable": (
                constants.WIDGETS['Entry'],
                {
                    "placeholder": "Название"
                }
            ),
            "formater": (
                constants.WIDGETS['Combobox'],
                {
                    "values": [
                        "Ничего не делать",
                        "Оставить только цифры",
                        "Сделать заглавными",
                        "Сделать с заглавной"
                    ],
                    'state': "readonly"
                }
            ),
            "filter": (
                constants.WIDGETS['Combobox'],
                {
                    "values": [
                        "Ничего не делать",
                        "Есть значение",
                    ],
                    'state': "readonly"
                }
            )
        }

        super().__init__(grid.GridFrame, add_button_text, columns)
