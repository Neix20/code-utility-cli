from .base import Processor
from typing import List, Dict

from datetime import datetime, timezone

def iso_to_epoch(iso_str: str) -> int:
    """Convert ISO 8601 formatted string to epoch time in seconds."""
    iso_str = iso_str.replace("Z", "+00:00")
    dt = datetime.fromisoformat(iso_str)
    res = int(dt.timestamp()) * 1000  # Convert to milliseconds
    return res

def epoch_to_iso(epoch: int | float) -> str:
    """Convert epoch time in seconds or milliseconds to ISO 8601 formatted string."""
    # Determine if epoch is in milliseconds or microseconds
    if epoch > 1e14:       # microseconds (e.g. 1759711015000000)
        epoch /= 1e6
    elif epoch > 1e11:     # milliseconds (e.g. 1759711015000)
        epoch /= 1e3
    
    dt = datetime.fromtimestamp(epoch, tz=timezone.utc)
    return dt.isoformat(timespec='seconds').replace('+00:00', '')

class EpochIsoConverterProcessor(Processor):
    def process(self, data: List[str]) -> str:
        """Convert list of epoch times to ISO 8601 formatted strings."""

        output_ls = []

        for dt in data:
            if dt.isdigit():
                ts = int(dt)
                dt = epoch_to_iso(ts)
            else:
                dt = iso_to_epoch(dt)

            output_ls.append(str(dt))

        

        res = "\n".join(output_ls)
        return res
        
