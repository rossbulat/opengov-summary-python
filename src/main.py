from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as package_version

import typer
from dotenv import load_dotenv
from InquirerPy.resolver import prompt
from typing_extensions import Annotated

from referendums import get_referendum, summarise_referendum

# Load API keys from .env file
load_dotenv()

# Create a Typer app instance
app = typer.Typer()


def handle_display_ai_summary(ref: int):
    """Handles the generation of AI summary for a referendum."""
    try:
        # Fetch referendum data
        result = get_referendum(ref)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    content = result.get("content", False)

    if not content:
        print("No content available for this referendum.")
        return

    response = summarise_referendum(content)
    print(response)
    print("------ Summary generated successfully ---")


def handle_display_metadata(ref: int):
    """Handles the display of referendum metadata."""
    print(f"Fetching metadata for Referendum ID: ${ref}")

    try:
        # Fetch referendum data
        result = get_referendum(ref)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

    print(f"Referendum ID: {ref}")
    print(f"Title: {result.get('title', 'Unknown')}")
    print(f"Status: {result.get('status', 'Unknown')}")
    print(f"Tags: {', '.join(result.get('tags', []))}")
    print(f"Comments Count: {result.get('comments_count', 0)}")


def handle_help(ctx: typer.Context):
    """Handles the help command."""
    typer.echo(ctx.get_help())


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
            print(f"Fetching metadata for Referendum ID: ${ref}")
            handle_display_metadata(ref)

        elif choice == "Generate AI Summary":
            handle_display_ai_summary(ref)
        elif choice == "Help":
            handle_help(ctx)
        elif choice == "Exit":
            print("Exiting...")
            # Important: Break the loop to exit the command
            break


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
