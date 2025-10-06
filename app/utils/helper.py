
import json

def check_json(data: str) -> bool:
    """Check if the given string is a valid JSON."""
    try:
        json.loads(data)
        return True
    except ValueError:
        return False