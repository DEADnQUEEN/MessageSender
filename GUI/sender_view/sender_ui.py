import tkinter as tk
from tkinter import messagebox
from typing import Optional

from GUI import constants
from GUI.loaders import csv_loader, text_loader, base
from GUI.content import content

from utils import logger
from messageSender import sender


class SenderUI:
    def setup_window(self):
        window = tk.Toplevel()

        for index, loader in enumerate((self.__loaded_content, self.__data)):
            label = tk.Label(window, text=loader.get_name(), font=("Arial", 12))
            label.grid(padx=5, pady=5, column=index, row=0, sticky=tk.NSEW)

            frame = tk.Frame(window, borderwidth=1, relief=tk.RIDGE)
            loader.setup_file_view(frame)
            loader.show_in_file_zone()
            frame.grid(row=1, column=0, padx=5, pady=5, rowspan=2, sticky=tk.NSEW)

        work_container = tk.Frame(window, borderwidth=1, relief=tk.RIDGE)

        self.__to_combobox = constants.WIDGETS['Combobox'](
            work_container,
            values=list(self.__data.columns.keys()),
            state='readonly',
        )
        self.__to_combobox.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        select_button = tk.Button(
            work_container,
            text="Выбрать переменную с телефонами",
            command=lambda : messagebox.showinfo("Телефон", "Переменная с телефонами выбрана", parent=window),
        )
        select_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

        button = tk.Button(
            work_container,
            text="Отправлять",
            command=self.save_wrap
        )
        button.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

        self.state_label = tk.Label(
            work_container,
            text=""
        )
        self.state_label.grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky=tk.NSEW)

        work_container.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)

        window.update()

        for grid in [window, work_container]:
            rows, columns = grid.grid_size()
            for column in range(columns):
                grid.grid_columnconfigure(column, weight=1)
            for row in range(columns):
                grid.grid_rowconfigure(row, weight=1)

    def save_wrap(self):
        try:
            self.send_message()
        except Exception as e:
            self.state_label.config(text="Произошла ошибка")
            logger.collect_log(str(e), "ui_exception")

    def send_message(self):
        if self.__bot_instance is None:
            raise ValueError

        for k in self.__loaded_content.get_variables.keys():
            if k not in self.__data.columns:
                messagebox.showerror(
                    parent=self.state_label,
                    title='Ошибка',
                    message='Переменная не существует.\nВозможно вы их обновили, но забыли связать текстовый шаблон'
                )
                raise KeyError

        text = self.__loaded_content.get_content

        with self.__bot_instance() as bot:
            bot.set_template(text)

            for number, csv_row in enumerate(
                self.__data.get_from_csv()
            ):
                self.state_label.config(text=f"Отправляется сообщение {number + 1}")
                bot.set_variables(
                    {
                        value['from']: csv_row[key]
                        for key, value in self.__loaded_content.get_variables.keys()
                    }
                )

                phone_number = csv_row[self.__to_combobox.value]

                bot.send_text(phone_number)

                self.state_label.config(text=f"Cообщение {number + 1} отправлено")
                self.state_label.master.update()

    def __init__(
            self,
            bot: Optional[type[sender.Sender]] = None,
            data: csv_loader.CSVLoader = None,
            loader_content: content.Base = None,
    ):
        self.__data = data
        self.__loaded_content = loader_content

        self.__bot_instance: Optional[type[sender.Sender]] = bot

        self.__to_combobox = None
        self.state_label: Optional[tk.Label] = None
