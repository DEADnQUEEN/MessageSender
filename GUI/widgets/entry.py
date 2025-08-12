import tkinter as tk


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", placeholder_color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.default_fg_color = self['fg']
        self.placeholder_active: bool = True

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
        self.placeholder_active = True

    def foc_in(self, *args):
        if self.placeholder_active:
            self.placeholder_active = False
            self.delete(0, tk.END)
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

    def get(self):
        if self.placeholder_active:
            return ''

        return super().get()

    @property
    def value(self):
        return self.get()