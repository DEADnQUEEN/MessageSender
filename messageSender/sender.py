from abc import ABC, abstractmethod
from imageEditor import editor

class Sender(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def send(self) -> None:
        pass

    @abstractmethod
    def send_text(self, to, text) -> bool:
        pass

    @abstractmethod
    def send_image(self, to, image_path) -> bool:
        pass

    @abstractmethod
    async def a_send_text(self, to, text) -> bool:
        pass

    @abstractmethod
    async def a_send_image(self, to, image_path) -> bool:
        pass
