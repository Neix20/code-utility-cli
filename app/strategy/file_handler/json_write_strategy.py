
import json
from pathlib import Path
from ..base import OutFileStrategy

class JsonWriteFileStrategy(OutFileStrategy):
    def write(self, file_path: Path, data: str) -> None:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        file.close()