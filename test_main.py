"""
Pytest tests for the FastAPI summaries endpoint.

This module contains tests that verify:
- Endpoint returns exactly 10 words when input has more than 10 words
- Timestamp field is present in the response
- Additional edge cases and error handling
"""

import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_summary_with_more_than_10_words():
    """
    Test that endpoint returns exactly 10 words when input has more than 10 words.

    This test:
    1. Sends a request with text containing more than 10 words
    2. Verifies the response contains exactly 10 words in the summary
    """
    # Text with 15 words
    text = "This is a test sentence with exactly fifteen words in total for testing purposes"
    response = client.post(
        "/summaries",
        json={"text": text},
    )

    assert response.status_code == 200

    data = response.json()
    assert "summary" in data
    assert "timestamp" in data

    # Verify exactly 10 words are returned
    summary_words = data["summary"].split()
    assert len(summary_words) == 10, f"Expected 10 words, got {len(summary_words)}"

    # Verify the summary contains the first 10 words
    expected_words = text.split()[:10]
    assert summary_words == expected_words


def test_timestamp_field_present():
    """
    Test that timestamp field is present and valid.

    This test:
    1. Sends a request to the endpoint
    2. Verifies timestamp field exists
    3. Verifies timestamp is a valid ISO format string
    """
    response = client.post(
        "/summaries",
        json={"text": "Hello world"},
    )

    assert response.status_code == 200

    data = response.json()
    assert "timestamp" in data

    # Verify timestamp is a string
    assert isinstance(data["timestamp"], str)

    # Verify timestamp is valid ISO format (can be parsed)
    try:
        datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
    except ValueError:
        pytest.fail(f"Timestamp '{data['timestamp']}' is not in valid ISO format")


def test_summary_with_exactly_10_words():
    """Test endpoint with exactly 10 words."""
    text = "one two three four five six seven eight nine ten"
    response = client.post(
        "/summaries",
        json={"text": text},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["summary"].split()) == 10


def test_summary_with_less_than_10_words():
    """Test endpoint with less than 10 words."""
    text = "Hello world"
    response = client.post(
        "/summaries",
        json={"text": text},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["summary"].split()) == 2
    assert data["summary"] == "Hello world"


def test_summary_with_whitespace():
    """Test endpoint handles multiple whitespaces correctly."""
    text = "  word1   word2    word3  word4  word5  word6  word7  word8  word9  word10  word11  "
    response = client.post(
        "/summaries",
        json={"text": text},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["summary"].split()) == 10


def test_summary_with_empty_text():
    """Test endpoint rejects empty text."""
    response = client.post(
        "/summaries",
        json={"text": ""},
    )

    assert response.status_code == 422  # Validation error


def test_summary_with_only_whitespace():
    """Test endpoint rejects text with only whitespace."""
    response = client.post(
        "/summaries",
        json={"text": "   \n\t  "},
    )

    assert response.status_code == 422  # Validation error


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"

