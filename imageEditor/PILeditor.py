from imageEditor.editor import Editor

from PIL import Image, ImageFont, ImageDraw

class PILEditor(Editor):
    def __init__(self):
        super().__init__()
        self.font = None
        self.img = None
        self.draw = None

    def open_image(self, path): 
        self.img = Image.open(path)
        self.draw = ImageDraw.Draw(self.img)

    def set_font(self, font_path, font_size: int):
        self.font = ImageFont.truetype(font_path, font_size)

    def draw_text_on_image(self, text, x, y, color: tuple[int, int, int]):
        if self.draw is None:
            raise ValueError("setup image first")

        self.draw.text((x, y), text, color, font=self.font)

    def save_image(self, path):
        if self.img is None:
            raise ValueError("setup image first")
        
        self.img.save(path)


