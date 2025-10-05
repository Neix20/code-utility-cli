import os
import json
from pathlib import Path

from .logger import logger

from strategy.base import InFileStrategy, OutFileStrategy

class FileHandler():
    def __init__(self, input: str = "", output: str = ""):
        fp = os.path.join("datakit.txt")
        
        try:
            self.input = Path(input) if input else Path(fp)
            self.output = Path(output) if output else Path(fp)
            self.validate_file()
        except Exception as ex:
            logger.error(f"Exception: {ex}")

        self._read_strategy: InFileStrategy | None = None
        self._write_strategy: OutFileStrategy | None = None

    def validate_file(self):
        if not self.input.exists():
            raise FileNotFoundError(f"Input file does not exist: {self.input}")
        if not self.input.is_file():
            raise ValueError(f"Input path is not a file: {self.input}")
        return True
    
    def set_read_strategy(self, strategy: InFileStrategy):
        self._read_strategy = strategy()

    def set_write_strategy(self, strategy: OutFileStrategy):
        self._write_strategy = strategy()

    def read(self) -> list[str]:
        """Read and strip lines, returns list of lines."""
        try:
            data = self._read_strategy.read(self.input)
            logger.info(f"Successfully read Data from {self.input}!")
            return data
        except Exception as ex:
            logger.error(f"Error! Unable to read Data from {self.input}! Exception: {ex}")
        
    def write(self, data: None) -> None:
        try:
            self._write_strategy.write(self.output, data)
            logger.info(f"Successfully write Data to {self.output}!")
        except Exception as ex:
            logger.error(f"Error! Unable to write Data to {self.output}! Exception: {ex}")