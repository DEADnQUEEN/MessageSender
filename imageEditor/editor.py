from abc import ABC, abstractmethod


class Editor(ABC):
    def __init__(self):
        self.font_path = None
        self.font_size = None

    @abstractmethod
    def set_font(self, font_path, font_size: int):
        self.font_path = font_path
        self.font_size = font_size

    @abstractmethod
    def draw_text_on_image(self, text, x, y, color: tuple[int, int, int]):
        pass

    @abstractmethod
    def open_image(self, path): 
        pass

    @abstractmethod
    def save_image(self, path):
        pass
