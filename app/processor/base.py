
from abc import ABC, abstractmethod
from typing import List

class Processor(ABC):
    @abstractmethod
    def process(self, data: List[str]) -> any:
        pass