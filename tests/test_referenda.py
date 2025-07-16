from unittest.mock import Mock, patch

import httpx
import pytest

from referendum import get_referendum, summarise_referendum


class TestReferendums:
    """Test cases for referendum-related functions."""

    @patch("src.referendums.httpx.Client")
    def test_get_referendum_success(self, mock_client):
        """Test successful referendum data fetching."""
        # Mock response data
        expected_data = {
            "title": "Test Referendum",
            "status": "voting",
            "content": "This is a test referendum content",
            "tags": ["treasury", "bounty"],
            "comments_count": 5,
        }

        # Setup mock
        mock_response = Mock()
        mock_response.json.return_value = expected_data
        mock_response.raise_for_status.return_value = None

        mock_client_instance = Mock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance
        mock_client.return_value.__exit__.return_value = None

        # Execute test
        result = get_referendum(123)

        # Assertions
        assert result == expected_data
        mock_client.assert_called_once_with(
            base_url="https://api.polkassembly.io/api/v1", timeout=None
        )
        mock_client_instance.get.assert_called_once_with(
            "/posts/on-chain-post",
            params={"postId": 123, "proposalType": "referendums_v2"},
            headers={"x-network": "polkadot"},
        )

    @patch("src.referendums.httpx.Client")
    def test_get_referendum_http_error(self, mock_client):
        """Test referendum fetching with HTTP error."""
        # Setup mock to raise HTTP error
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=Mock(), response=Mock()
        )

        mock_client_instance = Mock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance
        mock_client.return_value.__exit__.return_value = None

        # Execute test and expect exception
        with pytest.raises(httpx.HTTPStatusError):
            get_referendum(999)

    @patch("src.referendums.openai.responses.create")
    def test_summarise_referendum_success(self, mock_openai):
        """Test successful referendum summarization."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.output_text = "This is a test summary of the referendum content."
        mock_openai.return_value = mock_response

        # Test data
        test_content = "This is a detailed referendum proposal about treasury funding."

        # Execute test
        result = summarise_referendum(test_content)

        # Assertions
        assert result == "This is a test summary of the referendum content."
        mock_openai.assert_called_once()

        # Verify the call arguments
        call_args = mock_openai.call_args
        assert call_args[1]["model"] == "gpt-4.1"
        assert len(call_args[1]["input"]) == 2
        assert call_args[1]["input"][1]["role"] == "user"
        assert call_args[1]["input"][1]["content"] == test_content

    @patch("src.referendums.openai.responses.create")
    def test_summarise_referendum_empty_content(self, mock_openai):
        """Test referendum summarization with empty content."""
        mock_response = Mock()
        mock_response.output_text = "No content provided for summarization."
        mock_openai.return_value = mock_response

        result = summarise_referendum("")

        assert result == "No content provided for summarization."
        mock_openai.assert_called_once()

    @patch("src.referendums.openai.responses.create")
    def test_summarise_referendum_openai_error(self, mock_openai):
        """Test referendum summarization with OpenAI API error."""
        # Setup mock to raise an exception
        mock_openai.side_effect = Exception("OpenAI API Error")

        # Execute test and expect exception
        with pytest.raises(Exception, match="OpenAI API Error"):
            summarise_referendum("Test content")


# Test fixtures for reusable test data
@pytest.fixture
def sample_referendum_data():
    """Sample referendum data for testing."""
    return {
        "title": "Treasury Proposal: Fund Developer Tools",
        "status": "voting",
        "content": (
            "This proposal requests funding for developing new tools that will benefit "
            "the Polkadot ecosystem. The requested amount is 1000 DOT for a 6-month "
            "development period."
        ),
        "tags": ["treasury", "development", "tools"],
        "comments_count": 12,
        "created_at": "2025-07-01T10:00:00Z",
    }


@pytest.fixture
def mock_referendum_response(sample_referendum_data):
    """Mock HTTP response for referendum data."""
    mock_response = Mock()
    mock_response.json.return_value = sample_referendum_data
    mock_response.raise_for_status.return_value = None
    return mock_response
