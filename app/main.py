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
def executor(file_handler: FileHandler, processor: Processor):
    """Generalized function to run a processor with given input and output paths."""
    data = file_handler.read()

    # Dependecy Injection of Processor Function
    proc = processor()
    data = proc.process(data)

    # Write Output to File
    file_handler.write(data)

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
    executor(file_handler, JoinLinesProcessor)


@app.command()
def make_array(input: str = "", output: str = ""):
    """Convert lines into a JSON array."""
    file_handler = make_file_handler(input, output, TxReadFileStrategy, JsonWriteFileStrategy)
    executor(file_handler, MakeArrayProcessor)

@app.command()
def make_json(input: str = "", output: str = ""):
    """Convert data into structured JSON."""
    # Set File Handler
    file_handler = make_file_handler(input, output, TxReadFileStrategy, JsonWriteFileStrategy)
    executor(file_handler, MakeJsonProcessor)

@app.command()
def health():
    """Check if the CLI is functioning properly."""
    logger.info("Status: Healthy")

if __name__ == "__main__":
    app()
