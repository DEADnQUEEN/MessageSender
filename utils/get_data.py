import csv
from typing import Callable, Any, Union
from utils import logger, formaters, filters


def get_from_csv(
        file_path,
        columns: list[Union[int, tuple[int, Callable[[str], Any], Callable[[str], bool]]]],
        have_title: bool = True,
        **kwargs
):
    with open(file_path, encoding="utf-8", newline='') as csvfile:
        r = csv.reader(csvfile, **kwargs)

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


def get_columns(
        columns: list[Union[int, dict[str, Union[str, int]]]],
) -> list[Union[int, tuple[int, Callable[[str], str], Callable[[str], bool]]]]:
    column_data = []

    for column in columns:
        if isinstance(column, dict):
            if "column" not in column or \
                "formater" not in column or \
                "filter" not in column:
                raise ValueError

            column_data.append(
                (
                    column['column'],
                    formaters.FORMATERS[column['formater']],
                    filters.FILTERS[column['filter']]
                )
            )
        elif isinstance(column, int):
            column_data.append(column)
        else:
            raise ValueError

    return column_data
