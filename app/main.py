import os
import json
from datetime import datetime
import typer

from utils import (
    FileHandler, logger
)

from processor import (
    Processor, JoinLinesProcessor, MakeArrayProcessor, MakeJsonProcessor, GetKeysAndValuesProcessor,
    EpochIsoConverterProcessor
)

from strategy.base import InFileStrategy, OutFileStrategy

from strategy import (
    JsonReadFileStrategy, JsonWriteFileStrategy,
    TxReadFileStrategy, TxWriteFileStrategy
)

app = typer.Typer()

#region Utility Functions
DEBUG = True

log_file_handler = FileHandler()
log_file_handler.set_write_strategy(TxWriteFileStrategy)

def func_factory(processor: Processor, data: None) -> str:
    """Generate a function name based on the processor class name."""

    name = "unknown"
    in_data = "Error"
    
    if isinstance(processor, JoinLinesProcessor):
        name = "join_lines"
        in_data = "\n".join(data)
    elif isinstance(processor, MakeArrayProcessor):
        name = "make_array"
        in_data = "\n".join(data)
    elif isinstance(processor, MakeJsonProcessor):
        name = "make_json"
        in_data = "\n".join(data)
    elif isinstance(processor, GetKeysAndValuesProcessor):
        name = "get_keys_and_values"
        in_data = json.dumps(data, indent=4)
    elif isinstance(processor, EpochIsoConverterProcessor):
        name = "epoch_iso_converter"
        in_data = "\n".join(data)
    
    return name, in_data

def executor(file_handler: FileHandler, processor: Processor, debug: bool = False):
    """Generalized function to run a processor with given input and output paths."""
    try:
        data = file_handler.read()

        # Dependecy Injection of Processor Function
        proc = processor()
        proc_data = proc.process(data)

        # Write to Logs if Debug is Enabled
        if debug:
            # Fuck Our In Data Needs to Align With our Function
            func_name, in_data = func_factory(proc, data)
            file_name = datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"

            # Create Folder if it does not exists
            os.makedirs(os.path.join("logs", func_name), exist_ok=True)

            # Set Output Data
            log_file_handler.output = os.path.join("logs", func_name, file_name)

            # Write Input File
            log_file_handler.write(in_data)
    
        # Write Output to File
        file_handler.write(proc_data)
    except Exception as ex:
        logger.error(f"Exception: {ex}")

def make_file_handler(input: str, output: str, read_strategy: InFileStrategy, write_strategy: OutFileStrategy) -> FileHandler:
    """Helper function to create and configure a FileHandler."""
    file_handler = FileHandler(input=input, output=output)
    file_handler.set_read_strategy(read_strategy)
    file_handler.set_write_strategy(write_strategy)
    return file_handler
#endregion
        
@app.command()
def join_lines(input: str = "", output: str = ""):
    """Join all lines into a single line."""
    file_handler = make_file_handler(input, output, TxReadFileStrategy, TxWriteFileStrategy)
    executor(file_handler, JoinLinesProcessor, debug=DEBUG)


@app.command()
def make_array(input: str = "", output: str = ""):
    """Convert lines into a JSON array."""
    file_handler = make_file_handler(input, output, TxReadFileStrategy, JsonWriteFileStrategy)
    executor(file_handler, MakeArrayProcessor, debug=DEBUG)

@app.command()
def make_json(input: str = "", output: str = ""):
    """Convert data into structured JSON."""
    # Set File Handler
    file_handler = make_file_handler(input, output, TxReadFileStrategy, JsonWriteFileStrategy)
    executor(file_handler, MakeJsonProcessor, debug=DEBUG)

@app.command()
def get_keys_and_values(input: str = "", output: str = ""):
    """Convert JSON data into key-value pairs"""
    # Set File Handler
    file_handler = make_file_handler(input, output, JsonReadFileStrategy, TxWriteFileStrategy)
    executor(file_handler, GetKeysAndValuesProcessor, debug=DEBUG)

@app.command()
def epoch_iso_converter(input: str = "", output: str = ""):
    """Convert JSON data into key-value pairs"""
    # Set File Handler
    file_handler = make_file_handler(input, output, TxReadFileStrategy, TxWriteFileStrategy)
    executor(file_handler, EpochIsoConverterProcessor, debug=DEBUG)

@app.command()
def health():
    """Check if the CLI is functioning properly."""
    logger.info("Status: Healthy")

if __name__ == "__main__":
    app()
