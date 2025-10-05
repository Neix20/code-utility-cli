
from pathlib import Path
from ..base import InFileStrategy

class TxReadFileStrategy(InFileStrategy):
    def read(self, file_path: Path) -> list[str]:
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.readlines()
            for ind in range(len(data)):
                data[ind] = data[ind].strip()
        file.close()
        return data