import tkinter as tk
from  tkinter import messagebox

from GUI.loaders import csv_loader, template

from GUI.sender_view import sender_ui
from messageSender.WhatsAppBusinessApiSender import waba_sender


class UserView(tk.Frame):
    @property
    def variables(self):
        return self.__csv_viewer.columns

    def setup_replaces(self):
        if not self.variables:
            self.bell()
            messagebox.showerror(parent=self, title="Ошибка", message="Необходимо добавить CSV файл и указать переменные")
            return

        self.__template_loader.grid.paste_variables(list(self.variables.keys()))
        self.__template_loader.load_file()

    def setup_sender(self):
        if not self.variables:
            self.bell()
            messagebox.showerror(parent=self, title="Ошибка", message="Переменные не указаны.\nНеобходимо указать переменные")
            return
        self.__sender_view_type(
            waba_sender.WhatsAppApiSender,
            self.__csv_viewer,
            self.__template_loader,

        ).setup_window()

    def __init__(
            self,
            master,
            csv_viewer: csv_loader.CSVLoader,
            template_loader: template.TemplateLoader,
            sender_view_type: type[sender_ui.SenderUI],
            *args,
            **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        self.__csv_viewer = csv_viewer
        self.__template_loader = template_loader
        self.__sender_view_type = sender_view_type

        self.load_csv_button = tk.Button(
            self,
            text="Загрузить CSV",
            command=csv_viewer.load_file
        )
        self.load_csv_button.pack(side=tk.TOP, anchor=tk.CENTER, padx=5, pady=5)
        self.connect_templates = tk.Button(
            self,
            text="Выбрать шаблон",
            command=self.setup_replaces
        )
        self.connect_templates.pack(side=tk.TOP, anchor=tk.CENTER, padx=5, pady=5)
        self.connect_templates = tk.Button(
            self,
            text="Отправить сообщения",
            command=self.setup_sender
        )
        self.connect_templates.pack(side=tk.TOP, anchor=tk.CENTER, padx=5, pady=5)

