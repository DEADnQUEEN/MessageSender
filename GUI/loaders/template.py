import tkinter as tk
from typing import Optional
from tkinter import messagebox

from GUI.loaders import base
from GUI.fileview import text_view
from GUI.grid import template
from GUI.content import content
from GUI.widgets import combobox

from messageSender.WhatsAppBusinessApiSender import waba_sender


class TemplateLoader(base.RemoteLoader, content.Base):
    def __init__(
            self,
            widgets: Optional[list] = None
    ):
        self.grid = template.TemplateView()
        self.__view = text_view.TextView()
        super().__init__(
            self.__view,
            additional_widgets=widgets
        )
        self.templates: dict[str, dict[str, any]] = {
            tmp['name']: tmp
            for tmp in waba_sender.send_request("templates", 'get')['templates']
        }

        if not isinstance(self.preview_instance, text_view.TextView):
            raise ValueError

        self.preview_instance: text_view.TextView = self.preview_instance
        self.__combobox: Optional[combobox.PredefinedCmb] = None
        self.__entry_frame: Optional[tk.Frame] = None

        self.variables = None
        self.template_values = []

    def change_cmb(self, *_, **__) -> None:
        if self.__combobox is None:
            raise ValueError

        self.preview_instance.text = self.create_text()
        self.show_in_file_zone()

        self.__entry_frame.update()

        for child in self.__entry_frame.winfo_children():
            child.destroy()

        self.setup_variables()

    def setup_variables(self):
        if self.variables is None:
            raise ValueError

        for component in self.templates[self.__combobox.value]['components']:
            if "example" in component.keys() and "body_text" in component['example'].keys():
                for i in range(len(component['example']['body_text'][0])):
                    label = tk.Label(
                        master=self.__entry_frame,
                        text=f"Замена {{{{{i + 1}}}}}:",
                        font=("Arial", 10),
                    )
                    label.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5)

                    cmb = combobox.PredefinedCmb(
                        master=self.__entry_frame,
                        values=self.variables,
                        state="readonly"
                    )
                    cmb.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5)

    def create_text(self):
        text = ""

        for component in self.templates[self.__combobox.value]['components']:
            if "text" in component.keys():
                text += f"{component['text']}\n"

        return text

    def static_content(self, master: tk.Misc):
        label = tk.Label(
            master=master,
            text="Шаблоны: ",
            font=("Arial", 16),
        )
        label.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5)

        self.__combobox = combobox.PredefinedCmb(
            master=master,
            values=list(self.templates.keys()),
            state='readonly'
        )

        self.__combobox.variable.trace_add(
            "write",
            self.change_cmb
        )

        self.__view.text = self.create_text()

        self.__combobox.pack(side=tk.TOP, anchor=tk.W)
        self.__entry_frame = tk.Frame(master=master)
        self.__entry_frame.pack(side=tk.TOP, anchor=tk.W)

        self.setup_variables()

    @property
    def columns(self):
        return self.grid.data

    def default_data(self):
        if self.__combobox is None:
            return None
        active_template = self.templates[self.__combobox.value]
        return {
            "namespace": active_template['namespace'],
            "template": active_template['name'],
            "language": {
                "policy": "deterministic",
                "code": active_template['language'],
            },
            "params": [
                {
                    "type": "body",
                    "parameters": []
                }
            ],
        }

    def get_content(self):
        return self.template_values

    def paste_variables(self, variables):
        self.variables = variables

    def get_name(self):
        return "Шаблон"

    def save(self):
        self.template_values = []
        for child in self.__entry_frame.winfo_children():
            if isinstance(child, combobox.PredefinedCmb):
                self.template_values.append(child.value)
        super().save()

    def cancel(self):
        if self.template_values is None or len(self.template_values) == 0:
            self.__combobox.bell()
            if messagebox.askyesno(
                    title="Отмена",
                    message="Выбранные данные будут утеряны\n"
                            "Вы уверены что хотите выйти?"
                ):
                super().cancel()
