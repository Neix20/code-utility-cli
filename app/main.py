import os
import json
from datetime import datetime
import typer

from utils import (
    FileHandler, logger
)

from processor import (
    Processor, JoinLinesProcessor, MakeArrayProcessor, MakeJsonProcessor
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

def func_name_factory(processor: Processor) -> str:
    """Generate a function name based on the processor class name."""
    
    if isinstance(processor, JoinLinesProcessor):
        return "join_lines"
    elif isinstance(processor, MakeArrayProcessor):
        return "make_array"
    elif isinstance(processor, MakeJsonProcessor):
        return "make_json"
    
    return "unknown"

def executor(file_handler: FileHandler, processor: Processor, debug: bool = False):
    """Generalized function to run a processor with given input and output paths."""
    try:
        data = file_handler.read()

        # Dependecy Injection of Processor Function
        proc = processor()
        proc_data = proc.process(data)

        # Write to Logs if Debug is Enabled
        if debug:
            func_name = func_name_factory(proc)
            file_name = datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"

            # Create Folder if it does not exists
            os.makedirs(os.path.join("logs", func_name), exist_ok=True)

            log_file_handler.output = os.path.join("logs", func_name, file_name)

            in_data = "\n".join(data) if isinstance(data, list) else json.loads(data)
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
def health():
    """Check if the CLI is functioning properly."""
    logger.info("Status: Healthy")

if __name__ == "__main__":
    app()
