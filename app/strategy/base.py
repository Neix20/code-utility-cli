
from pathlib import Path
from abc import ABC, abstractmethod

class InFileStrategy(ABC):
    @abstractmethod
    def read(self, file_path: Path) -> list[str]:
        pass

class OutFileStrategy(ABC):
    @abstractmethod
    def write(self, file_path: Path, data: str) -> None:
        pass