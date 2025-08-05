from abc import ABC, abstractmethod


class Editor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def set_font(self, font_path, font_size: int):
        pass

    @abstractmethod
    def draw_text_on_image(self, text, x, y, color: tuple[int, int, int]):
        pass

