import tkinter as tk
from typing import Optional

from GUI.loaders import base
from GUI.fileview import text_view
from GUI.grid import template
from GUI.content import content

from messageSender.WhatsAppBusinessApiSender import waba_sender


class TemplateLoader(base.RemoteLoader, content.Base):
    def __init__(
            self,
            widgets: Optional[list] = None
    ):
        self.grid = template.TemplateView()
        super().__init__(
            text_view.TextView(),
            additional_widgets=widgets
        )
        self.templates: list[dict[str, any]] = waba_sender.WhatsAppApiSender.send_get_request(
            'templates'
        )['templates']
        if not isinstance(self.preview_instance, text_view.TextView):
            raise ValueError

        self.preview_instance: text_view.TextView = self.preview_instance

    def static_content(self, master: tk.Misc):
        pass

    @property
    def columns(self):
        return self.grid.data

    def get_content(self):
        return self.preview_instance.text

    def get_variables(self):
        return self.columns
