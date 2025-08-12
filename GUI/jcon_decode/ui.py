import json
import tkinter as tk
from tkinter import ttk
from typing import Optional

from GUI import constants


class JSONEncodedUI(tk.Frame):
    def __init__(self, master, json_path, commands: Optional[dict] = None, *args, **kw):
        super().__init__(master, *args, **kw)
        self.filepath = json_path
        self.commands = commands if commands is not None else {}
        self.frames = []
        self.widgets = []

        with open(json_path, "r", encoding="utf-8") as json_file:
            self.data = json.load(json_file)

        for data in self.data:
            self.__create_widget(self, data)


    @staticmethod
    def place_widget(widget: tk.Widget, widget_data: dict[str, any]):
        if "x" in widget_data['place'] and "y" in widget_data['place']:
            widget.place(**widget_data['place'])
        elif "row" in widget_data['place'] and "column" in widget_data['place']:
            widget.grid(**widget_data['place'])
        else:
            raise ValueError

    def __create_widget(self, master, widget_data: dict[str, any]):
        """
        Create a widget for a master widget and place it in the master widget.
        :param master:
        :param widget_data: json data for widget
        :return: widget object
        """
        if 'editable' in widget_data:
            copy = {
                k: v
                for k, v in widget_data.items()
                if k != "editable"
            }

            edit = {
                k: v
                for k, v in widget_data['editable'].items()
                if k != "count"
            }

            count = widget_data['editable']['count']
            for i in range(count):
                for edit_group, edit_data in edit.items():
                    for edit_arg, step in edit_data.items():
                        if isinstance(step, (int, float)):
                            copy[edit_group][edit_arg] += step
                        elif isinstance(step, list):
                            copy[edit_group][edit_arg] = step[i]
                        else:
                            raise ValueError(copy, '\n', widget_data)

                self.__create_widget(master, copy)

            return

        widget_kwarg = {
            'master': master,
        }

        widget_type = constants.WIDGETS[widget_data['type']]

        for function, function_data in (widget_data['callable'] if "callable" in widget_data else {}).items():
            widget_kwarg[function] = self.commands[function_data['name']](
                **function_data['args'],
                label=self.widgets[function_data["label_index"]]
            )

        if widget_type is tk.Frame:
            self.__create_frame(master, widget_data)
            return

        widget: tk.Widget = widget_type(
            **widget_kwarg,
            **widget_data['args']
        )

        self.place_widget(widget, widget_data)
        widget.update()
        self.widgets.append(widget)

    def __create_frame(
            self,
            master,
            frame_data: dict[str, any],
    ) -> ttk.Frame:
        new_frame = ttk.Frame(
            master,
            **frame_data['args'] if 'args' in frame_data else {},
        )
        new_frame.pack_propagate(False)
        if "place" in frame_data:
            new_frame.grid(**frame_data['place'])
        else:
            new_frame.pack()

        for item in frame_data['items']:
            self.__create_widget(new_frame, item)

        self.frames.append(new_frame)
        return new_frame

