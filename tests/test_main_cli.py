from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from src.main import app, handle_display_ai_summary, handle_display_metadata, handle_help


class TestMainCLI:
    """Test cases for the main CLI application."""

    def setup_method(self):
        """Setup test runner."""
        self.runner = CliRunner()

    def test_version_command(self):
        """Test the version command."""
        result = self.runner.invoke(app, ["version"])
        assert result.exit_code == 0
        # Should contain a version number (either from package or dev)
        assert "." in result.stdout or "dev" in result.stdout

    @patch("src.main.get_referendum")
    def test_handle_display_metadata_success(self, mock_get_referendum, capsys):
        """Test successful metadata display."""
        # Mock referendum data
        mock_data = {
            "title": "Test Referendum Title",
            "status": "voting",
            "tags": ["treasury", "bounty"],
            "comments_count": 10,
        }
        mock_get_referendum.return_value = mock_data

        # Execute function
        handle_display_metadata(123)

        # Capture output
        captured = capsys.readouterr()

        # Assertions
        assert "Fetching metadata for Referendum ID: $123" in captured.out
        assert "Referendum ID: 123" in captured.out
        assert "Title: Test Referendum Title" in captured.out
        assert "Status: voting" in captured.out
        assert "Tags: treasury, bounty" in captured.out
        assert "Comments Count: 10" in captured.out
        mock_get_referendum.assert_called_once_with(123)

    @patch("src.main.get_referendum")
    def test_handle_display_metadata_error(self, mock_get_referendum, capsys):
        """Test metadata display with API error."""
        # Mock API error
        mock_get_referendum.side_effect = Exception("API Error")

        # Execute function
        handle_display_metadata(123)

        # Capture output
        captured = capsys.readouterr()

        # Assertions
        assert "Unexpected error: API Error" in captured.out

    @patch("src.main.get_referendum")
    def test_handle_display_metadata_missing_fields(self, mock_get_referendum, capsys):
        """Test metadata display with missing fields."""
        # Mock referendum data with missing fields
        mock_data = {
            "title": "Test Title"
            # Missing status, tags, comments_count
        }
        mock_get_referendum.return_value = mock_data

        # Execute function
        handle_display_metadata(456)

        # Capture output
        captured = capsys.readouterr()

        # Assertions
        assert "Title: Test Title" in captured.out
        assert "Status: Unknown" in captured.out
        assert "Tags: " in captured.out  # Empty tags
        assert "Comments Count: 0" in captured.out

    @patch("src.main.summarise_referendum")
    @patch("src.main.get_referendum")
    def test_handle_display_ai_summary_success(self, mock_get_referendum, mock_summarise, capsys):
        """Test successful AI summary generation."""
        # Mock data
        mock_data = {"content": "This is referendum content to be summarized."}
        mock_get_referendum.return_value = mock_data
        mock_summarise.return_value = "This is a test AI summary of the referendum."

        # Execute function
        handle_display_ai_summary(789)

        # Capture output
        captured = capsys.readouterr()

        # Assertions
        assert "This is a test AI summary of the referendum." in captured.out
        assert "------ Summary generated successfully ---" in captured.out
        mock_get_referendum.assert_called_once_with(789)
        mock_summarise.assert_called_once_with("This is referendum content to be summarized.")

    @patch("src.main.get_referendum")
    def test_handle_display_ai_summary_no_content(self, mock_get_referendum, capsys):
        """Test AI summary with no content available."""
        # Mock data without content
        mock_data = {
            "title": "Test Referendum",
            "content": False,  # No content available
        }
        mock_get_referendum.return_value = mock_data

        # Execute function
        handle_display_ai_summary(999)

        # Capture output
        captured = capsys.readouterr()

        # Assertions
        assert "No content available for this referendum." in captured.out
        assert "Summary generated successfully" not in captured.out

    @patch("src.main.get_referendum")
    def test_handle_display_ai_summary_api_error(self, mock_get_referendum, capsys):
        """Test AI summary with API error."""
        # Mock API error
        mock_get_referendum.side_effect = Exception("Network error")

        # Execute function
        result = handle_display_ai_summary(404)

        # Capture output
        captured = capsys.readouterr()

        # Assertions
        assert result is False
        assert "Unexpected error: Network error" in captured.out

    def test_handle_help(self, capsys):
        """Test help command handler."""
        # Create a mock context
        mock_ctx = Mock()
        mock_ctx.get_help.return_value = "Test help message"

        # Execute function
        handle_help(mock_ctx)

        # Capture output
        captured = capsys.readouterr()

        # Assertions - typer.echo outputs to stdout
        assert "Test help message" in captured.out


class TestCLIIntegration:
    """Integration tests for the CLI application."""

    def setup_method(self):
        """Setup test runner."""
        self.runner = CliRunner()

    @patch("src.main.prompt")
    @patch("src.main.get_referendum")
    def test_referendum_command_metadata_flow(self, mock_get_referendum, mock_prompt):
        """Test the complete referendum command flow for metadata display."""
        # Mock referendum data
        mock_data = {
            "title": "Integration Test Referendum",
            "status": "active",
            "tags": ["test"],
            "comments_count": 5,
        }
        mock_get_referendum.return_value = mock_data

        # Mock user choices: first metadata, then exit
        mock_prompt.side_effect = [{"choice": "Display Referendum Metadata"}, {"choice": "Exit"}]

        # Execute command
        result = self.runner.invoke(app, ["referendum", "--ref", "123"])

        # Assertions
        assert result.exit_code == 0
        assert "Ready to work with Referendum ID: 123" in result.stdout
        assert "Integration Test Referendum" in result.stdout
        assert "Exiting..." in result.stdout

    @patch("src.main.prompt")
    @patch("src.main.summarise_referendum")
    @patch("src.main.get_referendum")
    def test_referendum_command_ai_summary_flow(
        self, mock_get_referendum, mock_summarise, mock_prompt
    ):
        """Test the complete referendum command flow for AI summary."""
        # Mock data
        mock_data = {"content": "Test referendum content for AI processing."}
        mock_get_referendum.return_value = mock_data
        mock_summarise.return_value = "AI generated summary for testing."

        # Mock user choices: first AI summary, then exit
        mock_prompt.side_effect = [{"choice": "Generate AI Summary"}, {"choice": "Exit"}]

        # Execute command
        result = self.runner.invoke(app, ["referendum", "--ref", "456"])

        # Assertions
        assert result.exit_code == 0
        assert "Ready to work with Referendum ID: 456" in result.stdout
        assert "AI generated summary for testing." in result.stdout
        assert "Summary generated successfully" in result.stdout

    @patch("src.main.prompt")
    def test_referendum_command_help_flow(self, mock_prompt):
        """Test the help command flow."""
        # Mock user choices: help, then exit
        mock_prompt.side_effect = [{"choice": "Help"}, {"choice": "Exit"}]

        # Execute command
        result = self.runner.invoke(app, ["referendum", "--ref", "789"])

        # Assertions
        assert result.exit_code == 0
        assert "Ready to work with Referendum ID: 789" in result.stdout
        # Help output contains usage information
        assert "Usage:" in result.stdout or "referendum" in result.stdout

    @patch("src.main.prompt")
    def test_referendum_command_immediate_exit(self, mock_prompt):
        """Test immediate exit from referendum command."""
        # Mock user choice: immediate exit
        mock_prompt.return_value = {"choice": "Exit"}

        # Execute command
        result = self.runner.invoke(app, ["referendum", "--ref", "999"])

        # Assertions
        assert result.exit_code == 0
        assert "Ready to work with Referendum ID: 999" in result.stdout
        assert "Exiting..." in result.stdout

    def test_referendum_command_without_ref_option(self):
        """Test referendum command without required --ref option."""
        result = self.runner.invoke(app, ["referendum"])

        # Should fail due to missing required option
        assert result.exit_code != 0
        # Check stderr for error message since typer usually writes to stderr
        assert (
            "Missing option" in str(result.output)
            or "Error" in str(result.output)
            or "required" in str(result.output)
            or result.exit_code == 2
        )  # Exit code 2 typically indicates argument error


# Test fixtures for complex scenarios
@pytest.fixture
def complex_referendum_data():
    """Complex referendum data for testing edge cases."""
    return {
        "title": "Complex Treasury Proposal with Multiple Components",
        "status": "passed",
        "content": (
            "This is a comprehensive proposal that includes multiple funding requests "
            "for different aspects of ecosystem development. The proposal covers "
            "infrastructure improvements, developer tooling, and community initiatives."
        ),
        "tags": ["treasury", "infrastructure", "development", "community"],
        "comments_count": 25,
        "created_at": "2025-06-15T14:30:00Z",
        "voting_end": "2025-07-01T14:30:00Z",
    }


@pytest.fixture
def mock_openai_summary():
    """Mock OpenAI summary response."""
    return (
        "This proposal seeks comprehensive funding for ecosystem development across "
        "multiple areas. Key components include infrastructure upgrades (40% of budget), "
        "developer tooling improvements (35%), and community initiatives (25%). "
        "The total requested amount is significant but justified by the scope. "
        "No major controversial points identified, though some discussion around "
        "budget allocation ratios exists in the community."
    )


class TestEdgeCases:
    """Test edge cases and error scenarios."""

    def setup_method(self):
        """Setup test runner."""
        self.runner = CliRunner()

    @patch("src.main.get_referendum")
    def test_empty_referendum_response(self, mock_get_referendum, capsys):
        """Test handling of empty referendum response."""
        mock_get_referendum.return_value = {}

        handle_display_metadata(1)

        captured = capsys.readouterr()
        assert "Title: Unknown" in captured.out
        assert "Status: Unknown" in captured.out

    @patch("src.main.get_referendum")
    def test_none_referendum_response(self, mock_get_referendum, capsys):
        """Test handling of None referendum response."""
        mock_get_referendum.return_value = None

        # This should raise an AttributeError when trying to call .get() on None
        with pytest.raises(AttributeError):
            handle_display_metadata(1)

    @patch("src.main.summarise_referendum")
    @patch("src.main.get_referendum")
    def test_ai_summary_with_empty_string_content(
        self, mock_get_referendum, mock_summarise, capsys
    ):
        """Test AI summary with empty string content."""
        mock_data = {"content": ""}
        mock_get_referendum.return_value = mock_data
        # Since empty string is falsy, the function should return early
        # and not call mock_summarise

        handle_display_ai_summary(1)

        captured = capsys.readouterr()
        # The actual behavior is to show "No content available" for empty/falsy content
        assert "No content available for this referendum." in captured.out

    def test_invalid_referendum_id_types(self):
        """Test CLI with invalid referendum ID types."""
        # Test with string instead of integer
        result = self.runner.invoke(app, ["referendum", "--ref", "abc"])
        assert result.exit_code != 0

        # Test with negative number
        result = self.runner.invoke(app, ["referendum", "--ref", "-1"])
        # This might actually work depending on validation, but worth testing
        # The behavior depends on whether negative IDs are valid in your system
