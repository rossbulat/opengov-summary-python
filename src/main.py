from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as package_version

import typer
from dotenv import load_dotenv
from typing_extensions import Annotated

# Load API keys from .env file
load_dotenv()

# Create a Typer app instance
app = typer.Typer()


# Command to summarize a specific OpenGov proposal
@app.command()
def referendum(ref: Annotated[int, typer.Option()]):
    """Provides tooling to inspect and generate summaries for OpenGov referenda.."""

    # Print ref
    print(f"Dealing with Referendum ID: {ref}")


# Command to display the OpenGov Summary Python package version
@app.command()
def version():
    """Prints the current version of the OpenGov Summary Python package."""
    try:
        version = package_version("opengov-summary")
    except PackageNotFoundError:
        version = "0.0.0-dev"
    print(f"{version}")


if __name__ == "__main__":
    app()
