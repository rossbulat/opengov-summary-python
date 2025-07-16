# OpenGov Summary CLI

OpenGov Summary CLI is a CLI tool using Polkassembly and OpenAI APIs to fetch proposal descriptions and provide a summary to users.

### Required API Keys
The application requires an OpenAI API key for AI summary generation functionality:

1. **Get an OpenAI API Key**:
   - Visit [OpenAI's website](https://openai.com/)
   - Sign up or log in to your account
   - Navigate to the API section
   - Generate a new API key

2. **Set up your environment**:
   ```bash
   # Create a .env file in the project root
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

   Or set it as an environment variable:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key_here
   ```

## Dependencies

### Main Tools
- **CLI Framework** - `typer`, `inquirerpy`, `rich` for building interactive command-line interface with beautiful formatting
- **API Communication** - `httpx` for HTTP requests to PolkAssembly and `openai` for AI summary generation
- **Configuration** - `python-dotenv` for environment variable management and API key handling
- **Data Processing** - `pydantic` for data validation and type safety

### Supporting Libraries
- **Network & Security** - Standard HTTP/SSL libraries for secure API communication
- **Terminal Enhancement** - Libraries for interactive prompts, shell detection, and text formatting
- **Utilities** - JSON parsing, progress indicators, and system compatibility tools

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Install Dependencies
```bash
# Clone the repository
git clone <repository-url>
cd opengov-summary-python

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### Development Dependencies
For development and testing, install additional packages:
```bash
pip install pytest pytest-mock
```

## Usage

### Basic Commands
```bash
# Check version
python src/main.py version

# Analyze a referendum (interactive mode)
python src/main.py referendum --ref 123
```

### Interactive Workflow
When you run the referendum command, you'll see an interactive menu:
```
Ready to work with Referendum ID: 123
? Choose an action: 
❯ Display Referendum Metadata
  Generate AI Summary  
  Help
  Exit
```

**Options:**
- **Display Referendum Metadata** - Shows referendum details (title, status, tags, comments)
- **Generate AI Summary** - Creates an AI-powered summary of the referendum content
- **Help** - Displays command help information
- **Exit** - Closes the application

## Testing

The project includes a comprehensive test suite with 22 test cases covering all functionality.

### Run Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/test_referenda.py -v      # Unit tests
python -m pytest tests/test_main_cli.py -v         # CLI tests

# Run test demo
python demo_tests.py
```

### Test Coverage
- **Unit Tests** - API communication and core functionality
- **Integration Tests** - Complete user workflows
- **CLI Tests** - Interactive interface and command handling
- **Edge Cases** - Error handling and boundary conditions

For detailed testing information, see [TEST_DOCUMENTATION.md](TEST_DOCUMENTATION.md).

## APIs Used

- [Polkassembly](https://documenter.getpostman.com/view/764953/2s93JxqLoH#intro): For fetching referendum data from Polkadot OpenGov
- [OpenAI API](https://platform.openai.com/docs/api-reference): For generating AI-powered summaries of proposals
