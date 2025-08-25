from abc import ABC, abstractmethod


class BaseSender(ABC):
    def __init__(self):
        super().__init__()
        self.default_data = None
        self.values = None

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

class Sender(BaseSender):
    @abstractmethod
    def send_text(self, to) -> bool:
        raise NotImplementedError

    @abstractmethod
    def send_image(self, to, image_path) -> bool:
        raise NotImplementedError


class AsyncSender(BaseSender):
    @abstractmethod
    async def a_send_text(self, to) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def a_send_image(self, to, image_path) -> bool:
        raise NotImplementedError
