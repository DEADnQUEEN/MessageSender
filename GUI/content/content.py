from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def get_content(self):
        raise NotImplementedError

    @abstractmethod
    def get_variables(self):
        raise NotImplementedError
