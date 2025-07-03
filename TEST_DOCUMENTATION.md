# OpenGov Summary CLI - Test Documentation

This document provides information about the comprehensive test suite for the OpenGov Summary CLI application.

## Test Overview

The test suite includes **22 test cases** covering all aspects of the application:

### 🔧 Unit Tests (`test_referendums.py`)
- **5 tests** for core functionality
- API communication with PolkAssembly
- OpenAI integration for AI summaries
- Error handling for network issues
- Data parsing and validation

### 🖥️ CLI Handler Tests (`test_main_cli.py - TestMainCLI`)
- **8 tests** for individual CLI handlers
- Metadata display functionality
- AI summary generation
- Help command handling
- Error scenarios and recovery

### 🔄 Integration Tests (`test_main_cli.py - TestCLIIntegration`)
- **5 tests** for complete user workflows
- Interactive menu navigation
- End-to-end command execution
- User choice handling
- Exit scenarios

### ⚠️ Edge Case Tests (`test_main_cli.py - TestEdgeCases`)
- **4 tests** for edge cases and error conditions
- Empty and None responses
- Invalid input handling
- Malformed data handling

## Running Tests

### Prerequisites
```bash
# Install test dependencies
pip install pytest pytest-mock

# Or install all requirements
pip install -r requirements.txt
```

### Run All Tests
```bash
# Run complete test suite
python -m pytest tests/ -v

# Run with short traceback
python -m pytest tests/ --tb=short

# Run specific test files
python -m pytest tests/test_referendums.py -v
python -m pytest tests/test_main_cli.py -v
```

### Run Test Categories
```bash
# Unit tests only
python -m pytest tests/test_referendums.py -v

# CLI handler tests
python -m pytest tests/test_main_cli.py::TestMainCLI -v

# Integration tests
python -m pytest tests/test_main_cli.py::TestCLIIntegration -v

# Edge case tests
python -m pytest tests/test_main_cli.py::TestEdgeCases -v
```

## Test Demo

Run the comprehensive test demo:
```bash
python demo_tests.py
```

This demo script:
- Shows test coverage overview
- Runs all test categories
- Demonstrates CLI usage examples
- Provides setup instructions

## Test Features

### 🎭 Mocking Strategy
- **External API calls** are mocked for reliability and speed
- **User input** is simulated for automated testing
- **Error conditions** are artificially created to test error handling
- **Network dependencies** are eliminated for consistent testing

### 📊 Test Coverage
The tests cover:
- ✅ **Happy path scenarios** - Normal operations work correctly
- ✅ **Error handling** - Application handles errors gracefully
- ✅ **Edge cases** - Unusual inputs and conditions are handled
- ✅ **Integration flows** - Complete user workflows function properly
- ✅ **API interactions** - External service calls work as expected

### 🔍 Test Scenarios

#### Referendum Data Fetching
- Successful API responses
- HTTP errors (404, 500, etc.)
- Network timeouts
- Malformed JSON responses
- Empty data handling

#### AI Summary Generation
- Successful OpenAI API calls
- API errors and rate limiting
- Empty content handling
- Large content processing

#### CLI Interface
- Interactive menu navigation
- User input validation
- Command-line argument parsing
- Help system functionality
- Graceful exit handling

#### Error Recovery
- Network connection issues
- Invalid referendum IDs
- Missing configuration
- API key validation

## Continuous Testing

### Development Workflow
```bash
# Run tests after code changes
python -m pytest tests/ -v

# Run specific tests during development
python -m pytest tests/test_main_cli.py::TestMainCLI::test_version_command -v

# Watch for changes (if using pytest-watch)
ptw tests/
```

### Test Configuration
The tests use `pytest.ini` for configuration:
- Verbose output by default
- Short tracebacks for readability
- Colored output for better visualization
- Proper test discovery patterns

## Mock Data Examples

The tests use realistic mock data:

```python
# Example referendum data
{
    "title": "Treasury Proposal: Fund Developer Tools",
    "status": "voting",
    "content": "Detailed proposal content...",
    "tags": ["treasury", "development", "tools"],
    "comments_count": 12
}

# Example AI summary
"This proposal seeks funding for ecosystem development tools. 
The requested amount is justified by the scope and potential impact..."
```

## Test Utilities

### Test Fixtures
- `sample_referendum_data` - Realistic referendum data
- `mock_referendum_response` - HTTP response mock
- `complex_referendum_data` - Edge case data
- `mock_openai_summary` - AI summary mock

### Helper Functions
- `setup_method()` - Test environment setup
- `print_section()` - Demo output formatting
- `run_command()` - Demo command execution

## Best Practices

### Writing Tests
1. **Use descriptive test names** that explain what is being tested
2. **Mock external dependencies** to ensure tests are fast and reliable
3. **Test both success and failure scenarios**
4. **Include edge cases** and boundary conditions
5. **Keep tests independent** - each test should work in isolation

### Maintaining Tests
1. **Update tests when features change**
2. **Add tests for new functionality**
3. **Remove or update tests for deprecated features**
4. **Keep mock data realistic and up-to-date**

## Troubleshooting

### Common Issues
1. **Import errors** - Ensure Python path includes src directory
2. **Mock failures** - Check that mocked functions match actual signatures
3. **Test failures** - Run tests individually to isolate issues
4. **Environment issues** - Ensure virtual environment is activated

### Debug Tips
```bash
# Run tests with more verbose output
python -m pytest tests/ -vvv

# Stop on first failure
python -m pytest tests/ -x

# Run only failed tests from last run
python -m pytest tests/ --lf

# Show local variables in tracebacks
python -m pytest tests/ --tb=long -l
```

## Contributing

When adding new functionality:
1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Add integration tests for new CLI features
4. Update this documentation

The comprehensive test suite ensures the OpenGov Summary CLI application is reliable, maintainable, and ready for production use.
