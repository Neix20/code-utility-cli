from .base import Processor
from typing import List, Dict

class MakeJsonProcessor(Processor):
    def process(self, data: List[str]) -> Dict[str, str]:
        res = {}
        for line in data:
            key, value = line.split("; ")
            res[key] = value
        return res