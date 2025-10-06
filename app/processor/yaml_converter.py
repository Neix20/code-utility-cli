from .base import Processor
from typing import List, Dict
import yaml
from textwrap import dedent
import json

from utils.helper import check_json

class YamlConverterProcessor(Processor):

    def __init__(self, type: str):
        self.type = type.lower()
        
        selection = ["yaml-to-json", "json-to-yaml"]
        if self.type not in selection:
            raise ValueError(f"Type must be either '{"', ".join(selection[:-1])}' or '{selection[-1]}'")

    def process(self, data: str) -> List[str]:
        """Convert json string to yaml string"""

        # We Need something to detect if its JSON String or YAML
        res = "Error"

        # Parse Text File as Original
        data = "\n".join(data)

        # Convert From JSON to YAML
        if self.type == "json-to-yaml":
            json_data = json.loads(data)
            res = yaml.safe_dump(json_data, sort_keys=False, indent=2, allow_unicode=True)
        else:
            # Convert From YAML to JSON
            yaml_data = yaml.safe_load(data)
            res = json.dumps(yaml_data, indent=2)

        return res