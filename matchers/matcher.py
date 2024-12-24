from abc import ABC, abstractmethod

class Matcher(ABC):
    @abstractmethod
    def get(self, content: str) -> list[str]:
        pass