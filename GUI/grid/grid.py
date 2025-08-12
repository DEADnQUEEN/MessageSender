import tkinter as tk
from tkinter.messagebox import askyesno, showerror

from typing import Callable

from utils.translates import TRANSLATES
from GUI import constants

VAR_KEY = 'variable'

class GridFrame(tk.Frame):
    def add_row(self):
        self.saved = False
        self.rows += 1

        for index, column_widget in enumerate(self.columns.values()):
            widget = column_widget[0](self.__content_frame, **column_widget[1])
            widget.grid(row=self.rows, column=index, padx=5, pady=5)

    def save(self, commit: bool = True):
        self.__content_frame.update()

        save = {}

        for row_index in range(self.rows):
            row_index += 1
            column = {}
            for index, key in enumerate(self.columns.keys()):
                widget = self.__content_frame.grid_slaves(row=row_index, column=index)[0]
                column[key] = widget.value

                if isinstance(widget, constants.WIDGETS['Combobox']) and key not in self.exceptions:
                    column[key] = TRANSLATES[column[key]]

                if column[key] is None:
                    self.bell()
                    showerror(
                        parent=self,
                        title='Ошибка переменной',
                        message=f"Значение отсутствует\nСтрока: {row_index}"
                    )
                    return

            if VAR_KEY in column:
                variable = column[VAR_KEY]

                if variable in save.keys():
                    self.bell()
                    showerror(
                        parent=self,
                        title='Ошибка переменной',
                        message=f"Переменная с таким именем уже существует\nСтрока: {row_index}"
                    )
                    return
                elif not len(variable):
                    self.bell()
                    showerror(
                        parent=self,
                        title='Ошибка переменной',
                        message=f"Переменная без названия\nСтрока: {row_index}"
                    )
                    return

                save[variable] = {k:v for k,v in column.items() if k != VAR_KEY}

        self.saved = True
        self.drop(save)
        self.destroy()

        return save

    def destroy(self):
        if self.rows > 0 and not self.saved:
            result = askyesno(title="Выход", message="Сохранить изменения?", parent=self)

            if result:
                self.save()
            self.rows= 0

        super().destroy()
        self.master.destroy()

    def __init__(
            self,
            master,
            add_button_text: str,
            columns: dict[str, (tk.Widget, dict[str, any])],
            data_drop: Callable,
            *args,
            **kwargs
    ):
        self.exceptions = ('variable', )
        super().__init__(
            master,
            *args,
            **{k: v for k, v in kwargs.items() if k != "variables"}
        )
        self.rows = 0
        self.columns = columns

        self.saved = False
        self.drop = data_drop

        self.top_frame = tk.Frame(self)

        self.__add_button = tk.Button(
            self.top_frame,
            text=add_button_text,
            command=self.add_row
        )
        self.__add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.top_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

        self.__content_frame = tk.Frame(self)

        for index, column_name in enumerate(columns.keys()):
            column_label = tk.Label(
                self.__content_frame,
                text=column_name if column_name not in TRANSLATES else TRANSLATES[column_name]
            )
            column_label.grid(row=0, column=index)

        self.__content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.save_frame = tk.Frame(self)

        cancel = tk.Button(
            self.save_frame,
            text="Отменить",
            command=self.destroy
        )
        save = tk.Button(
            self.save_frame,
            text="Сохранить",
            command=self.save
        )
        cancel.pack(side=tk.RIGHT, padx=5, pady=5)
        save.pack(side=tk.RIGHT, padx=5, pady=5)

        self.save_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)


class GridViewer:
    def grab_data(self, data):
        self.data = data

    def __init__(self, grid_frame: type[GridFrame], button_text = None, columns = None, *args, **kwargs):
        self.add_button_text = button_text
        self.columns = columns

        self.grid = grid_frame
        self.args = args
        self.kwargs = kwargs

        self.data = None

    def view(self) -> GridFrame:
        if self.add_button_text is None:
            raise ValueError(f"text for add_button must be defined")
        elif self.columns is None:
            raise ValueError(f"columns must be defined")

        window = tk.Toplevel()
        form = self.grid(
            window,
            self.add_button_text,
            self.columns,
            self.grab_data,
            *self.args,
            **self.kwargs
        )

        form.pack(fill=tk.BOTH, expand=True)
        window.grab_set()
        window.focus_set()

        return form

