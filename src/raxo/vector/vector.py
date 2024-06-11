from abc import ABC, abstractmethod


class Vector(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def add_ddl(self, ddl, embedding):
        pass

    def add_documentation(self, doc, embedding):
        pass
