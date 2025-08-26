from GUI.fileview import base

import tkinter as tk
from typing import Optional


class TextView(base.View):
    def __init__(self):
        self.view_zone: Optional[tk.Text] = None
        self.text: str = ""

    def setup(self, master: tk.Misc):
        scroll_x = tk.Scrollbar(master, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(master, orient=tk.VERTICAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.view_zone = tk.Text(
            master,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            wrap=tk.NONE,
        )
        self.view_zone.config(state=tk.DISABLED)
        self.view_zone.pack(expand=True, fill=tk.BOTH)

        self.fill()

    def fill(self):
        self.view_zone.config(state=tk.NORMAL)
        self.view_zone.delete('1.0', tk.END)
        self.view_zone.insert(tk.END, self.text)
        self.view_zone.config(state=tk.DISABLED)
