import typer

from utils import (
    FileHandler, logger
)

from processor import (
    Processor, JoinLinesProcessor, MakeArrayProcessor, MakeJsonProcessor
)

app = typer.Typer()

def executor(processor: Processor, input: str = "", output: str = "", is_json: bool = False):
    """
    Generalized function to run a processor with given input and output paths.
    """
    config = FileHandler(input=input, output=output)
    data = config.read()

    # Dependecy Injection of Processor Function
    proc = processor()
    processed_data = proc.process(data)

    # Write Output to File
    config.write(processed_data, is_json=is_json)
        
@app.command()
def join_lines(input: str = "", output: str = ""):
    """Join all lines into a single line."""
    executor(JoinLinesProcessor, input=input, output=output)


@app.command()
def make_array(input: str = "", output: str = ""):
    """Convert lines into a JSON array."""
    executor(MakeArrayProcessor, input=input, output=output, is_json=True)


@app.command()
def make_json(input: str = "", output: str = ""):
    """Convert data into structured JSON."""
    executor(MakeJsonProcessor, input=input, output=output, is_json=True)

@app.command()
def health():
    """Check if the CLI is functioning properly."""
    logger.info("Status: Healthy")

if __name__ == "__main__":
    app()
