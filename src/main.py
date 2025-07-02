from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()


def hello_world():
    """Print a greeting."""
    print("Hello, world!")


if __name__ == "__main__":
    hello_world()
