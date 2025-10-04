from .base import Processor
from typing import List

class JoinLinesProcessor(Processor):
    def process(self, data: List[str]) -> str:
        return " ".join(data).strip()