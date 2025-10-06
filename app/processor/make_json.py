import re
import json

from .base import Processor
from typing import List, Dict

class MakeJsonProcessor(Processor):
    def process(self, data: List[str]) -> Dict[str, str]:

        # Final Output
        res = {}

        # Checking for Duplicates
        key_ls = set()
        res_ls = []

        # Regex for Splitter
        delimeter = re.compile(r"[,;|]\s*")

        for line in data:
            arr = delimeter.split(line, maxsplit=1)
            key, value = arr

            # Resolve Duplicates First
            if key in key_ls:
                # We add the previous Here
                res_ls.append({**res})

                # Reset Object and Key List
                res = {}
                key_ls = set()

            # Value is Required to remove Quotes
            value = re.sub(r"^[\"']*(.*?)[\"']$", r'\1', value)

            # Replace all '\"' with "'"
            value = value.replace(r'\"', '"')

            # If the value is detected as json, we should parse it
            if re.match(r'^[\[{].*[\]}]$', value):
                value = json.loads(value)

            res[key] = value
            key_ls.add(key)

        # Add the Last Res List
        res_ls.append({**res})

        if len(res_ls) > 1:
            return res_ls

        return res_ls[0]