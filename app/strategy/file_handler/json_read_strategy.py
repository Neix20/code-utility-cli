
import json
from pathlib import Path
from ..base import InFileStrategy

class JsonReadFileStrategy(InFileStrategy):
    def read(self, file_path: Path) -> list[str]:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        file.close()
        return data