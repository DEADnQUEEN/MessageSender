import tkinter as tk
from abc import abstractmethod, ABC
from typing import Optional
from tkinter import messagebox


class FileLoader(ABC):
    def __init__(self, file_types, additional_widgets: Optional[list[tuple[type[tk.Widget], dict[str, any]]]] = None):
        self.window = tk.Toplevel
        self.view = None
        self.filepath: Optional[str] = None
        self.file_types = file_types
        self.view_zone = None

        self.parent_view = None
        self.view_frame = None

        self.widgets = [] if additional_widgets is None else additional_widgets
        self.additional_widgets = []

    @abstractmethod
    def open_file(self):
        raise NotImplementedError

    @abstractmethod
    def load_file(self):
        raise NotImplementedError

    @abstractmethod
    def setup_file_view(self, master: tk.Misc):
        raise NotImplementedError


    def cancel(self):
        answer = messagebox.askokcancel(parent=self.view, title="Отмена", message="Данные будут утеряны")

        if answer:
            self.filepath = None
            self.view.destroy()

    def save(self):
        if self.filepath is None:
            messagebox.showerror(parent=self.view, title="Ошибка", message="Файл ещё не выбран")
            return
        messagebox.showinfo(parent=self.view, title="Сохранено", message="Файл успешно сохранен")
        self.view.destroy()

    def load_ui(self) -> tk.Toplevel:
        self.view = self.window()

        content_frame = tk.Frame(self.view)
        button_frame = tk.Frame(content_frame)

        load_button = tk.Button(
            button_frame,
            text="Выбрать файл",
            command=self.open_file
        )
        load_button.pack(side=tk.TOP, anchor=tk.W)

        self.additional_widgets = []
        for widget_object in self.widgets:
            widget_class, widget_data = widget_object
            widget = widget_class(button_frame, **widget_data)
            widget.pack(side=tk.TOP, anchor=tk.W)
            self.additional_widgets.append(widget)

        button_frame.pack(anchor=tk.NW, padx=5, pady=5, side=tk.LEFT)

        self.view_frame = tk.Frame(content_frame)

        self.view_frame.pack(expand=True, fill=tk.BOTH, side=tk.BOTTOM)
        content_frame.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

        bottom_frame = tk.Frame(self.view)
        cancel = tk.Button(
            bottom_frame,
            text="Отменить",
            command=self.cancel
        )
        save = tk.Button(
            bottom_frame,
            text="Сохранить",
            command=self.save
        )
        cancel.pack(side=tk.RIGHT, padx=5, pady=5)
        save.pack(side=tk.RIGHT, padx=5, pady=5)
        bottom_frame.pack(expand=False, fill=tk.X, side=tk.BOTTOM)

        return self.view
