from .base import Processor
from typing import List, Dict
import yaml
from textwrap import dedent
import json

from utils.helper import check_json

class YamlConverterProcessor(Processor):
    def process(self, data: str) -> List[str]:
        """Convert json string to yaml string"""

        # We Need something to detect if its JSON String or YAML
        res = "Error"

        # Parse Text File as Original
        data = "\n".join(data)

        # Convert From JSON to YAML
        if check_json(data):
            json_data = json.loads(data)
            res = yaml.safe_dump(json_data, sort_keys=False, indent=2, allow_unicode=True)
        else:
            # Convert From YAML to JSON
            yaml_data = yaml.safe_load(data)
            res = json.dumps(yaml_data, indent=2)

        return res