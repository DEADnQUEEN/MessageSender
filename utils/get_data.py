import csv
import json
from typing import Callable, Union
from utils import logger, formaters, filters


def get_from_csv(
        file_path,
        columns: dict[str, Union[int, tuple[int, Callable[[str], str], Callable[[str], bool]]]],
        have_title: bool = True,
        **kwargs
) -> list[dict[str, str]]:
    with open(file_path, encoding="utf-8", newline='') as csvfile:
        r = csv.reader(csvfile, **kwargs)

        if have_title:
            r.__next__()

        fail = 0
        rows = 0
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
    columns: dict[str, dict[str, Union[str, int]]]
) -> dict[str, Union[int, tuple[int, Callable[[str], str], Callable[[str], bool]]]]:
    column_data = {}
    for column, data in columns.items():
        if "column" not in data:
            raise ValueError

        column_data[column] = (
            data['column'] - 1,
            formaters.FORMAT_FUNCTIONS[data['formater']],
            filters.FILTERS[data['filter']]
        ) if "formater" in data and "filter" in data else data['column']

    return column_data


def parse_column_config(config_file_path):
    with open(config_file_path, encoding="utf-8") as json_file:
        columns: dict[str, dict[str, Union[str, int]]] = json.load(json_file)

    return get_columns(columns)