import tkinter as tk
from tkinter import messagebox
from typing import Optional

from GUI.loaders import csv_loader, text_loader
from GUI import constants
from GUI.sender_view import config

from utils import get_data, formaters, logger

class SenderUI:
    def setup_window(self):
        window = tk.Toplevel()

        csv_frame = tk.Frame(window, borderwidth=1, relief=tk.RIDGE)
        csv_label = tk.Label(csv_frame, text=f'CSV файл:', font=("Arial", 12))
        csv_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        csv_view = tk.Frame(csv_frame)
        self.__csv.setup_file_view(csv_view)
        csv_view.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        csv_frame.grid(row=0, column=0, padx=5, pady=5, rowspan=2, sticky=tk.NSEW)

        txt_container = tk.Frame(window, borderwidth=1, relief=tk.RIDGE)
        txt_label = tk.Label(txt_container, text="Текст сообщения", font=("Arial", 12))
        txt_label.pack(side=tk.TOP, padx=5, pady=5)
        txt_view = tk.Frame(txt_container)
        self.__txt.setup_file_view(txt_view)
        txt_view.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
        txt_container.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

        work_container = tk.Frame(window, borderwidth=1, relief=tk.RIDGE)

        self.__to_combobox = constants.WIDGETS['Combobox'](
            work_container,
            values=list(self.__csv_variables.keys()),
            state='readonly',
        )
        self.__to_combobox.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        select_button = tk.Button(
            work_container,
            text="Выбрать переменную с телефонами",
            command=lambda : messagebox.showinfo("Телефон", "Переменная с телефонами выбрана", parent=window),
        )
        select_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

        self.__engine_combobox = constants.WIDGETS['Combobox'](
            work_container,
            values=list(config.WORKING_SENDERS.keys()),
            state='readonly',
        )
        self.__engine_combobox.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        button = tk.Button(
            work_container,
            text="Отправлять",
            command=self.save_wrap
        )
        button.grid(row=1, column=1, padx=5, pady=5)

        self.state_label = tk.Label(
            work_container,
            text=""
        )
        self.state_label.grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky=tk.NSEW)

        work_container.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

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
        with open(self.__txt.filepath, 'r', encoding='utf-8') as f:
            base_text = ""
            for line in f.readlines():
                base_text += line

        with config.WORKING_SENDERS[self.__engine_combobox.value]() as bot:
            if not self.__csv.filepath:
                raise ValueError("csv file is empty")

            for number, csv_row in enumerate(
                get_data.get_from_csv(
                    self.__csv.filepath,
                    get_data.get_columns(
                        self.__csv_variables
                    )
                )
            ):
                replaces = {}

                for k, v in self.__txt.columns.items():
                    if k not in self.__csv_variables:
                        messagebox.showerror(
                            parent=self.state_label,
                            title='Ошибка',
                            message='Переменная не существует.\nВозможно вы их обновили, но забыли связать текстовый шаблон'
                        )
                        bot.__exit__(None, None, None)
                        raise ValueError("template error")
                    replaces[v['from']] = csv_row[k]

                self.state_label.config(text=f"Отправляется сообщение {number + 1}")
                phone_number = csv_row[self.__to_combobox.value]

                phone_number = "89182124943"
                bot.current = None

                text_message = formaters.paste_texts(
                    base_text,
                    **replaces
                )

                bot.send_text(phone_number, text_message)

                self.state_label.config(text=f"Cообщение {number + 1} отправлено")
                self.state_label.master.update()


    def __init__(self, csv: csv_loader.CSVLoader, txt: text_loader.TXTLoader):
        self.__txt = txt
        self.__csv = csv

        self.__engine_combobox = None
        self.__to_combobox = None
        self.state_label: Optional[tk.Label] = None

    @property
    def __csv_variables(self):
        return self.__csv.columns

