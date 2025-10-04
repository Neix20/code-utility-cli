
from abc import ABC, abstractmethod

class Processor(ABC):
    @abstractmethod
    def process(self, data: list[str]) -> any:
        pass

class JoinLinesProcessor(Processor):
    def process(self, data: list[str]) -> str:
        return " ".join(data).strip()
    
class MakeArrayProcessor(Processor):
    def process(self, data: list[str]) -> list[str]:
        return data
    
class MakeJsonProcessor(Processor):
    def process(self, data: list[str]) -> dict[str, str]:
        res = {}
        for line in data:
            key, value = line.split("; ")
            res[key] = value
        return res