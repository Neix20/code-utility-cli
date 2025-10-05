from .base import Processor
from typing import List

class MakeArrayProcessor(Processor):
    def process(self, data: List[str]) -> List[str]:
        """Convert list of strings into a JSON array string."""

        if len(data) == 1:
            return data[0]

        return data