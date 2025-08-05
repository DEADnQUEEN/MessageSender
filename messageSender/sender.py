from abc import ABC, abstractmethod


class Sender(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def send(self, to, text: str) -> None:
        pass

