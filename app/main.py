import typer

from utils.logger import logger
from utils.file_handler import FileHandler

from processor.processor import Processor, JoinLinesProcessor, MakeArrayProcessor, MakeJsonProcessor

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
    executor(JoinLinesProcessor, input=input, output=output)

@app.command()
def make_array(input: str = "", output: str = ""):
    executor(MakeArrayProcessor, input=input, output=output, is_json=True)

@app.command()
def make_json(input: str = "", output: str = ""):
    executor(MakeJsonProcessor, input=input, output=output, is_json=True)
    
@app.command()
def health():
    logger.info("Status: Healthy")

if __name__ == "__main__":
    app()
