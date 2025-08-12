from abc import ABC, abstractmethod
from imageEditor import editor

class WithUsage(ABC):
    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


class Sender(WithUsage):
    @abstractmethod
    def send_text(self, to, text: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def send_image(self, to, image_path) -> bool:
        raise NotImplementedError


class AsyncSender(WithUsage):
    @abstractmethod
    async def a_send_text(self, to, text) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def a_send_image(self, to, image_path) -> bool:
        raise NotImplementedError
