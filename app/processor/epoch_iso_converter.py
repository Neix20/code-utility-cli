from .base import Processor
from typing import List, Dict

from datetime import datetime, timezone

def epoch_to_iso(epoch: str) -> str:
    """Convert epoch time in seconds or milliseconds to ISO 8601 formatted string."""

    # Convert to INT
    epoch = int(epoch)

    # Determine if epoch is in milliseconds or microseconds
    if epoch > 1e14:       # microseconds (e.g. 1759711015000000)
        epoch /= 1e6
    elif epoch > 1e11:     # milliseconds (e.g. 1759711015000)
        epoch /= 1e3
    
    # Convert to datetime object in UTC
    dt = datetime.fromtimestamp(epoch)

    # Convert to ISO 8601 format without microseconds and 'Z'
    return dt.isoformat(timespec='seconds').replace('+00:00', '')
    
def iso_to_epoch(iso: str) -> str:
    """Convert ISO 8601 formatted string to epoch time in seconds."""
    iso = iso.replace("Z", "+00:00")
    dt = datetime.fromisoformat(iso)
    res = int(dt.timestamp()) * 1000  # Convert to milliseconds
    return str(res)

class EpochIsoConverterProcessor(Processor):
    def process(self, data: List[str]) -> str:
        """Convert list of epoch times to ISO 8601 formatted strings."""
        output_ls = []
        for seconds in data:
            if seconds.isdigit():
                converted = epoch_to_iso(seconds)
            else:
                converted = iso_to_epoch(seconds)
            output_ls.append(converted)
        res = "\n".join(output_ls)
        return res
        
