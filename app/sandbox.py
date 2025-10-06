import time
import yaml
import json

from utils import FileHandler

from strategy.base import InFileStrategy, OutFileStrategy

from strategy import (
    JsonReadFileStrategy, 
    JsonWriteFileStrategy,
    TxReadFileStrategy, 
    TxWriteFileStrategy
)

def main():
    start_time = time.time()

    file_handler = FileHandler()
    file_handler.set_read_strategy(TxReadFileStrategy)

    data = file_handler.read()
    data = "\n".join(data)

    res = yaml.safe_load(data)
    res = json.dumps(res, indent=2)
    print(res)

    end_time = time.time() - start_time
    print(f"Time Taken: {end_time:.2f} seconds")

if __name__ == "__main__":
    main()