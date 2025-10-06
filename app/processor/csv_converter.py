from .base import Processor
from typing import List, Dict
import pandas as pd
import json

from utils.helper import check_json
from utils import logger

from io import StringIO

class CsvConverterProcessor(Processor):
    def __init__(self, type: str):
        self.type = type.lower()
        
        selection = ["json-to-csv", "csv-to-json"]
        if self.type not in selection:
            raise ValueError(f"Type must be either '{"', ".join(selection[:-1])}' or '{selection[-1]}'")
        
    def process(self, data: str) -> List[str]:
        """Convert json string to yaml string"""

        res = "Error"
        
        # Parse Text File as Original
        data = "\n".join(data)

        if self.type == "json-to-csv":
            json_data = json.loads(data)
            df = pd.json_normalize(json_data)
            res = df.to_csv(index=False)
        else:
            df = pd.read_csv(StringIO(data))
            res = df.to_json(orient="records", indent=2)

            # Unflatten JSON

            # This is where every single record of JSON always returns as an object
            res = json.loads(res)
            if len(res) == 1:
                res = res[0]
            res = json.dumps(res, indent=2)

        return res