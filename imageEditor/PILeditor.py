from abc import ABC

from PIL import Image, ImageFont, ImageDraw
from imageEditor.editor import Editor


class PILEditor(Editor, ABC):
    def __init__(self, path):
        super().__init__(path)
        self.path = path
        self.img = Image.open(path)
        self.font = None
        self.draw = ImageDraw.Draw(self.img)

    def set_font(self, font_path, font_size: int):
        self.font = ImageFont.truetype(font_path, font_size)

    def draw_text_on_image(self, text, x, y, color: tuple[int, int, int]):
        self.draw.text((x, y), text, color, font=self.font)



