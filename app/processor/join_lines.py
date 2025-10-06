from .base import Processor
from typing import List

class JoinLinesProcessor(Processor):
    def process(self, data: List[str]) -> str:
        _data = [line.strip() for line in data if line.strip()]
        return " ".join(_data)