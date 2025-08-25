from GUI.loaders import fileview
from GUI.grid import csvdata
from GUI import constants

import csv
from utils import logger, formaters, filters
from typing import Callable, Union


class CSVLoader(fileview.FileLoad):
    @property
    def header_exists(self):
        return self.additional_widgets[1].value

    def __init__(self):
        grid = csvdata.CSVData()
        super().__init__(
            grid,
            [("CSV файл", "*.csv")],
            [
                (constants.WIDGETS['Button'], {"text": "Настроить переменные", "command": grid.view}),
                (constants.WIDGETS['Checkbox'], {"text": "Начинать с 1 строки", "font": ("Arial", 10)})
            ]
        )

    def get_from_csv(self) -> list[dict[str, str]]:
        with open(self.filepath, encoding="utf-8", newline='') as csvfile:
            r = csv.reader(csvfile)

            if self.header_exists:
                r.__next__()

            fail = 0
            rows = 0

            columns = self.get_columns()
            for i, row in enumerate(r):
                rows += 1
                export_dict = {}
                for key, data in columns.items():
                    if isinstance(data, int):
                        export_dict[key] = row[data]
                        continue

                    column, data_formater, data_filter = data
                    value = data_formater(row[column])
                    filtered = data_filter(value)

                    if not filtered:
                        fail += 1
                        logger.collect_log(f"row {i} is not valid, column {key} fail filter")
                        break

                    export_dict[key] = value
                else:
                    yield export_dict

        if fail:
            logger.collect_log(f"Failed rows: {fail} of {rows}")

    def get_columns(
            self,
        ) -> dict[str, Union[int, tuple[int, Callable[[str], str], Callable[[str], bool]]]]:
        column_data = {}
        for column, data in self.columns.items():
            if "column" not in data:
                raise ValueError

            column_data[column] = (
                data['column'] - 1,
                formaters.FORMAT_FUNCTIONS[data['formater']],
                filters.FILTERS[data['filter']]
            ) if "formater" in data and "filter" in data else data['column']

        return column_data

