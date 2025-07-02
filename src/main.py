from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as package_version

import typer
from dotenv import load_dotenv
from InquirerPy.resolver import prompt
from typing_extensions import Annotated

# Load API keys from .env file
load_dotenv()

# Create a Typer app instance
app = typer.Typer()


# Command to summarize a specific OpenGov proposal
@app.command()
def referendum(ref: Annotated[int, typer.Option()], ctx: typer.Context):
    """Provides tooling to inspect and generate summaries for OpenGov referenda."""

    # Print ref
    print(f"Ready to work with Referendum ID: {ref}")

    while True:
        # Prompt user for action
        questions = [
            {
                "type": "list",
                "name": "choice",
                "message": "Choose an action:",
                "choices": [
                    "Display Referendum Metadata",
                    "Generate AI Summary",
                    "Help",
                    "Exit",
                ],
            },
        ]
        result = prompt(questions)
        choice = result["choice"]

        if choice == "Display Referendum Metadata":
            # Placeholder for displaying referendum metadata
            typer.echo(f"Displaying metadata for Referendum ID: {ref}")
        elif choice == "Generate AI Summary":
            # Placeholder for generating AI summary
            typer.echo(f"Generating AI summary for Referendum ID: {ref}")
        elif choice == "Help":
            typer.echo(ctx.get_help())
        elif choice == "Exit":
            # Important: Break the loop to exit the command
            break


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
