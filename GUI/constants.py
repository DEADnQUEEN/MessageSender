import tkinter as tk
from GUI.widgets import check, entry, combobox, numberbox, filewidget


WIDGETS: dict[str: tk.Widget] = {
    "Button": tk.Button,
    "Label": tk.Label,
    "Checkbox": check.CheckButton,
    "Entry": entry.EntryWithPlaceholder,
    "Number": numberbox.NumberBox,
    "Combobox": combobox.PredefinedCmb,
    "Frame": tk.Frame,
    "File": filewidget.LoadFile
}
