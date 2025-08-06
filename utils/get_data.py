import csv
import json
from typing import Callable, Any, Union
from utils import logger, formaters, filters


def get_from_csv(
        file_path,
        columns: list[Union[int, tuple[int, Callable[[str], Any], Callable[[str], bool]]]],
        have_title: bool = True,
        delimiter=',',
        quote_char='"'
):
    with open(file_path, encoding="utf-8", newline='') as csvfile:
        r = csv.reader(csvfile, delimiter=delimiter, quotechar=quote_char)

        if have_title:
            r.__next__()

        fail = 0
        rows = 0
        for i, row in enumerate(r):
            rows += 1
            export_array = []
            for index, column in enumerate(columns):
                if isinstance(column, int):
                    export_array.append(row[column])
                    continue

                value = column[1](row[column[0]])
                if not column[2](value):
                    fail += 1
                    logger.collect_log(f"row {i} is not valid, column {index} fail filter")
                    break

                export_array.append(value)
            else:
                yield export_array

    if fail:
        logger.collect_log(f"Failed rows: {fail} of {rows}")


def get_columns(file) -> list[Union[int, tuple[int, Callable[[str], Any], Callable[[str], bool]]]]:
    with open(file, encoding="utf-8", newline='') as json_file:
        data = json.load(json_file)
        output_array = []

        if not isinstance(data, list):
            raise TypeError

        for item in data:
            if isinstance(item, dict):
                if "column" not in item or \
                    "formater" not in item or \
                    "filter" not in item:
                    raise ValueError

                output_array.append(
                    (
                        item['column'],
                        formaters.FORMATERS[item['formater']],
                        filters.FILTERS[item['filter']]
                    )
                )
            elif isinstance(item, int):
                output_array.append(item)
            else:
                raise ValueError

    return output_array
