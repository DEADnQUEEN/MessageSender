from abc import ABC, abstractmethod
import tkinter as tk

class View(ABC):
    @abstractmethod
    def setup(self, master: tk.Misc):
        raise NotImplementedError

    @abstractmethod
    def fill(self):
        raise NotImplementedError

