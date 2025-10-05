from .base import Processor
from typing import List, Dict

class GetKeysAndValuesProcessor(Processor):
    def process(self, data: Dict[str, str]) -> str:
        """Convert list of strings into a JSON array string."""

        output_ls = []

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    for key, value in item.items():
                        output = f"{key}; {value}"
                        output_ls.append(output)
        elif isinstance(data, dict):
            for key, value in data.items():
                output = f"{key}; {value}"
                output_ls.append(output)

        res = "\n".join(output_ls)
        return res