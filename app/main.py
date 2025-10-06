import os
import json
from datetime import datetime
import typer

from utils import FileHandler, logger

from processor import (
    Processor,
    JoinLinesProcessor,
    MakeArrayProcessor,
    MakeJsonProcessor,
    GetKeysAndValuesProcessor,
    EpochIsoConverterProcessor,
    YamlConverterProcessor,
    CsvConverterProcessor,
    SqlConverterProcessor
)

from strategy.base import InFileStrategy, OutFileStrategy

from strategy import (
    JsonReadFileStrategy, 
    JsonWriteFileStrategy,
    TxReadFileStrategy, 
    TxWriteFileStrategy
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
        in_data = json.dumps(data, indent=2)
    elif isinstance(processor, EpochIsoConverterProcessor):
        name = "epoch_iso_converter"
        in_data = "\n".join(data)
    elif isinstance(processor, YamlConverterProcessor):
        name = "yaml_converter"
        in_data = "\n".join(data)
    elif isinstance(processor, CsvConverterProcessor):
        name = "csv_converter"
        in_data = "\n".join(data)
    elif isinstance(processor, SqlConverterProcessor):
        name = "csv_converter"
        in_data = "\n".join(data)
    
    return name, in_data

def executor(file_handler: FileHandler, processor: Processor, debug: bool = False):
    """Generalized function to run a processor with given input and output paths."""
    try:
        data = file_handler.read()

        # Dependecy Injection of Processor Function
        proc = processor.process(data)

        # Write to Logs if Debug is Enabled
        if debug:
            # Fuck Our In Data Needs to Align With our Function
            func_name, in_data = func_factory(processor, data)
            file_name = datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"

            # Create Folder if it does not exists
            os.makedirs(os.path.join("logs", func_name), exist_ok=True)

            # Set Output Data
            log_file_handler.output = os.path.join("logs", func_name, file_name)

            # Write Input File
            log_file_handler.write(in_data)
    
        # Write Output to File
        file_handler.write(proc)
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
    # Set File Handler
    file_handler = make_file_handler(input, output, TxReadFileStrategy, TxWriteFileStrategy)

    # Initialize Processor
    processor = JoinLinesProcessor()

    executor(file_handler, processor, debug=DEBUG)


@app.command()
def make_array(input: str = "", output: str = ""):
    """Convert lines into a JSON array."""

    # Set File Handler
    file_handler = make_file_handler(input, output, TxReadFileStrategy, JsonWriteFileStrategy)
    
    # Initialize Processor
    processor = MakeArrayProcessor()

    executor(file_handler, processor, debug=DEBUG)

@app.command()
def make_json(input: str = "", output: str = ""):
    """Convert data into structured JSON."""
    # Set File Handler
    file_handler = make_file_handler(input, output, TxReadFileStrategy, JsonWriteFileStrategy)
    
    # Initialize Processor
    processor = MakeJsonProcessor()

    executor(file_handler, processor, debug=DEBUG)

@app.command()
def get_keys_and_values(input: str = "", output: str = ""):
    """Convert JSON data into key-value pairs"""
    # Set File Handler
    file_handler = make_file_handler(input, output, JsonReadFileStrategy, TxWriteFileStrategy)
    
    # Initialize Processor
    processor = GetKeysAndValuesProcessor()

    executor(file_handler, processor, debug=DEBUG)

@app.command()
def epoch_iso_converter(input: str = "", output: str = ""):
    """Convert JSON data into key-value pairs"""
    # Set File Handler
    file_handler = make_file_handler(input, output, TxReadFileStrategy, TxWriteFileStrategy)
    
    # Initialize Processor
    processor = EpochIsoConverterProcessor()

    executor(file_handler, processor, debug=DEBUG)

@app.command()
def yaml_converter(type: str, input: str = "", output: str = ""):
    """Convert JSON data into key-value pairs"""
    # Set File Handler
    file_handler = make_file_handler(input, output, TxReadFileStrategy, TxWriteFileStrategy)
    
    # Initialize Processor
    processor = YamlConverterProcessor(type)

    executor(file_handler, processor, debug=DEBUG)

@app.command()
def csv_converter(type: str, input: str = "", output: str = ""):
    """Convert JSON data into key-value pairs"""
    # Set File Handler
    file_handler = make_file_handler(input, output, TxReadFileStrategy, TxWriteFileStrategy)
    
    # Initialize Processor
    processor = CsvConverterProcessor(type)

    executor(file_handler, processor, debug=DEBUG)

@app.command()
def sql_converter(type: str, tbl_name: str = "tbl_name", input: str = "", output: str = ""):
    """Convert JSON data into key-value pairs"""
    # Set File Handler
    file_handler = make_file_handler(input, output, TxReadFileStrategy, TxWriteFileStrategy)
    
    # Initialize Processor
    processor = SqlConverterProcessor(type, tbl_name)

    executor(file_handler, processor, debug=DEBUG)

@app.command()
def health():
    """Check if the CLI is functioning properly."""
    logger.info("Status: Healthy")

if __name__ == "__main__":
    app()
