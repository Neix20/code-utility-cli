
from pathlib import Path
from ..base import OutFileStrategy

class TxWriteFileStrategy(OutFileStrategy):
    def write(self, file_path: Path, data: str) -> None:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data)
        file.close()