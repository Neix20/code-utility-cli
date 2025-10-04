from .base import Processor
from typing import List


class MakeArrayProcessor(Processor):
    def process(self, data: List[str]) -> List[str]:
        return data