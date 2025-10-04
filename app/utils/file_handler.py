import os
import json
from pathlib import Path

from .logger import logger

class FileHandler():
    def __init__(self, input: str = "", output: str = ""):
        fp = os.path.join("datakit.txt")
        self.input = Path(input) if input else Path(fp)
        self.output = Path(output) if output else self.input
        self.validate_params()

    def validate_params(self):
        """Default validation: input must exist and be a file. Subclasses can override."""
        if not self.input.exists():
            raise FileNotFoundError(f"Input file does not exist: {self.input}")
        if not self.input.is_file():
            raise ValueError(f"Input path is not a file: {self.input}")
        
    def read(self, is_json: bool = False) -> list[str]:
        """Read and strip lines, returns list of lines."""
        try:
            with open(self.input, "r", encoding="utf-8") as file:
                
                if not is_json:
                    data = file.readlines()
                    for ind in range(len(data)):
                        data[ind] = data[ind].strip()
                else:
                    data = json.load(file)

            file.close()

            logger.info(f"Successfully read Data from {self.input}!")
            return data
        except Exception as ex:
            logger.error(f"Error! Unable to read Data from {self.input}! Exception: {ex}")
        
    def write(self, data: str, is_json: bool = False) -> None:
        try:
            with open(self.output, "w", encoding="utf-8") as file:
                if not is_json:
                    file.write(data)
                else:
                    json.dump(data, file, indent=4)
            file.close()

            logger.info(f"Successfully write Data to {self.output}!")
        except Exception as ex:
            logger.error(f"Error! Unable to write Data to {self.output}! Exception: {ex}")