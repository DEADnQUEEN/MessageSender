from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def default_data(self):
        raise NotImplementedError

    @abstractmethod
    def get_content(self):
        raise NotImplementedError
